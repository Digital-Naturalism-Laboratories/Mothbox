import cv2
import numpy as np
import glob
import math
import random
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely import affinity
import matplotlib.pyplot as plt
from collections import defaultdict
from shapely.ops import unary_union

# ----------------------------
# CONFIG
# ----------------------------
folder = r"D:\x-anylabeling-matting\onlybig\*.png"
base_image_path = r"c:\Users\andre\Documents\GitHub\Mothbox\Firmware\graphics\croptext_6200px.png"  # input base mask

# Packing modes
pack_mode = "edge"   # options: "spiral", "random", "edge"
max_random_tries = 500  # for mode B
edge_step = 10          # inward step size for mode C

scale_factor = 0.3
random_scale = False
min_scale = 0.1
max_scale = 2.5

# for base image
base_scale = 2  # 50% size, for example

animate = True
bg_color = None
random_rotate = True
max_rotation = 360
debug_view = False
debug_mask = False

padding = 10
out_size = (5000, 5000)




# ----------------------------
# Candidate generators
# ----------------------------
def spiral_candidates(center, max_radius=5000, step_theta=0.25, step_r=0.7):
    theta, radius = 0.0, 20.0
    while radius < max_radius:
        yield (center[0] + radius * math.cos(theta),
               center[1] + radius * math.sin(theta))
        theta += step_theta
        radius += step_r


def random_candidates(base_poly, n=500):
    minx, miny, maxx, maxy = base_poly.bounds
    for _ in range(n):
        rx = random.uniform(minx, maxx)
        ry = random.uniform(miny, maxy)
        if base_poly.contains(Polygon([(rx, ry), (rx+1, ry), (rx, ry+1)])):  # cheap point-in-poly
            yield (rx, ry)


def edge_inward_candidates(base_poly, step=10):
    # start along polygon boundary and move inward
    boundary = np.array(base_poly.exterior.coords)
    centroid = np.array(base_poly.centroid.coords[0])
    for pt in boundary[::max(1, len(boundary)//200)]:  # subsample boundary
        pt = np.array(pt)
        vec = centroid - pt
        dist = np.linalg.norm(vec)
        if dist == 0: continue
        dir_vec = vec / dist
        steps = int(dist // step)
        for i in range(steps):
            candidate = pt + dir_vec * (i * step)
            yield (candidate[0], candidate[1])


# ----------------------------
# Load base mask -> polygon
# ----------------------------
def load_base_shape(mask_path, threshold=127):
    """
    Load a base mask image and return a Shapely Polygon or MultiPolygon in pixel coordinates.
    Supports:
      - Transparent PNG: nonzero alpha is filled area
      - Black-and-white image: black pixels are filled area
    """
    # Try to read alpha channel first
    mask_img = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    if mask_img is None:
        raise ValueError(f"Could not load mask image: {mask_path}")


    if base_scale != 1.0:
        mask_img = cv2.resize(mask_img, None, fx=base_scale, fy=base_scale, interpolation=cv2.INTER_AREA)

    # Determine which channel to use for mask
    if mask_img.shape[2] == 4:
        # PNG with alpha channel
        alpha = mask_img[:, :, 3]
        mask_bin = (alpha > 0).astype(np.uint8) * 255
    else:
        # Grayscale or B/W: assume black = filled
        if len(mask_img.shape) == 3:
            gray = cv2.cvtColor(mask_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = mask_img
        mask_bin = (gray < threshold).astype(np.uint8) * 255  # black pixels = filled

    # Find contours (external only)
    contours, _ = cv2.findContours(mask_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    polys = []
    for cnt in contours:
        if len(cnt) >= 3:
            coords = cnt[:, 0, :].astype(float)
            poly = Polygon(coords)
            if poly.is_valid and poly.area > 0:
                polys.append(poly)

    if not polys:
        raise ValueError("No valid polygons found in mask image")

    # Merge polygons if multiple
    base_poly = unary_union(polys)
    H, W = mask_bin.shape
    return base_poly, (W, H)


# ----------------------------
# 1. Load + preprocess image
# ----------------------------
def get_shape(path, scale_factor=1.0):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None or img.shape[2] < 4:
        raise ValueError(f"Image {path} missing alpha channel")

    if scale_factor != 1.0:
        img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor,
                         interpolation=cv2.INTER_AREA)

    if random_scale:
        factor = random.uniform(min_scale, max_scale)
        img = cv2.resize(img, None, fx=factor, fy=factor,
                         interpolation=cv2.INTER_AREA)

    alpha = img[:, :, 3]
    mask = (alpha > 10).astype(np.uint8) * 255 #set a little above 0 so it does catch big clear regions

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)

    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    poly_local = Polygon(approx.reshape(-1, 2))
    cx, cy = poly_local.centroid.coords[0]

    return {
        "poly": poly_local,
        "img": img,
        "anchor": (cx, cy),
        "w": img.shape[1],
        "h": img.shape[0],
        "path": path,
    }


# ----------------------------
# Spatial grid (same as before)
# ----------------------------
class SpatialGrid:
    def __init__(self, cell_size=300):
        self.cell_size = cell_size
        self.cells = defaultdict(list)

    def _cell_coords(self, x, y):
        return int(math.floor(x / self.cell_size)), int(math.floor(y / self.cell_size))

    def insert(self, shape, x, y):
        minx, miny, maxx, maxy = shape["padded_local"].bounds
        minx += x - shape["anchor"][0]
        maxx += x - shape["anchor"][0]
        miny += y - shape["anchor"][1]
        maxy += y - shape["anchor"][1]

        col1, row1 = self._cell_coords(minx, miny)
        col2, row2 = self._cell_coords(maxx, maxy)

        for col in range(col1, col2 + 1):
            for row in range(row1, row2 + 1):
                self.cells[(col, row)].append((shape, (x, y)))

    def nearby(self, shape, x, y):
        minx, miny, maxx, maxy = shape["padded_local"].bounds
        minx += x - shape["anchor"][0]
        maxx += x - shape["anchor"][0]
        miny += y - shape["anchor"][1]
        maxy += y - shape["anchor"][1]

        col1, row1 = self._cell_coords(minx, miny)
        col2, row2 = self._cell_coords(maxx, maxy)

        neighbors = []
        for col in range(col1 - 1, col2 + 2):
            for row in range(row1 - 1, row2 + 2):
                neighbors.extend(self.cells.get((col, row), []))

        seen = set()
        unique = []
        for sh, pos in neighbors:
            sid = id(sh)
            if sid not in seen:
                seen.add(sid)
                unique.append((sh, pos))
        return unique


# ----------------------------
# 2. Packing algorithm
# ----------------------------
def pack_shapes(
    shapes,
    base_poly,
    out_size=None,
    padding=0,
    random_rotate=False,
    max_rotation=360,
    animate=False,
    pack_mode="spiral",
    max_random_tries=500,
    edge_step=10,
    debug_mask=False,
    bg_color=None,
    debug_view=False,
):
    """
    Pack shapes inside base_poly (pixel coordinates). Prevents overlaps using an occupancy mask.
    - shapes: list of dicts with keys: 'img'(RGBA numpy), 'poly'(local shapely polygon), 'anchor'(x,y), 'w','h','path'
    - base_poly: shapely Polygon or MultiPolygon in image pixel coords (top-left origin).
    - out_size: (W,H) optional; if None it's inferred from base_poly.bounds.
    - padding: pixels to pad around each shape (float allowed; we'll ceil it for pixel dilation).
    - pack_mode: "spiral" | "random" | "edge"
    """
    # ---- derive canvas and origin (handles masks that don't start at 0,0) ----
    minx, miny, maxx, maxy = base_poly.bounds
    origin_x = int(math.floor(minx))
    origin_y = int(math.floor(miny))
    if out_size is None:
        W = int(math.ceil(maxx - minx))
        H = int(math.ceil(maxy - miny))
    else:
        W, H = out_size

    # local poly (shifted so (0,0) maps to top-left of returned canvas)
    base_poly_local = affinity.translate(base_poly, xoff=-origin_x, yoff=-origin_y)

    # occupancy raster (H rows, W cols); 0 = free, 1 = occupied
    occupancy = np.zeros((H, W), dtype=np.uint8)

    placed = []

    # ---- animation setup ----
    if animate:
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect("equal")
        ax.axis("off")

    # ---- helper: pixel dilation for padding ----
    pad_px = int(math.ceil(max(0.0, padding)))

    def make_padded_mask(img_rgba):
        """Return boolean mask of same (h,w) with padding applied."""
        alpha = (img_rgba[:, :, 3] > 0).astype(np.uint8)  # 0/1
        if pad_px <= 0:
            return alpha.astype(bool)
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (pad_px * 2 + 1, pad_px * 2 + 1))
        dil = cv2.dilate(alpha, k, iterations=1)
        return (dil > 0)

    # ---- candidate generators (world coords) ----
    centroid = base_poly.centroid.coords[0]

    def spiral_candidates(center, max_radius=max(W, H) * 2, step_theta=0.25, step_r=0.7):
        theta, radius = 0.0, 20.0
        while radius < max_radius:
            yield (center[0] + radius * math.cos(theta),
                   center[1] + radius * math.sin(theta))
            theta += step_theta
            radius += step_r

    def random_candidates(base_poly, n=500):
        minx, miny, maxx, maxy = base_poly.bounds
        tries = 0
        while tries < n:
            rx = random.uniform(minx, maxx)
            ry = random.uniform(miny, maxy)
            if base_poly.contains(Point(rx, ry)):
                yield (rx, ry)
            tries += 1

    def edge_inward_candidates(base_poly, step=edge_step):
        # pick largest polygon if multipolygon
        poly = base_poly
        if isinstance(base_poly, MultiPolygon):
            poly = max(base_poly.geoms, key=lambda p: p.area)
        boundary = np.array(poly.exterior.coords)
        centroid_pt = np.array(poly.centroid.coords[0])
        subs = max(1, len(boundary) // 300)
        for pt in boundary[::subs]:
            pt = np.array(pt)
            vec = centroid_pt - pt
            dist = np.linalg.norm(vec)
            if dist == 0:
                continue
            dir_vec = vec / dist
            steps = max(1, int(dist // step))
            for i in range(steps):
                cand = pt + dir_vec * (i * step)
                yield (float(cand[0]), float(cand[1]))

    # ---- placement helpers using occupancy + polygon containment ----
    def can_place_at(shape, x, y, pad_mask_bool, padded_local):
        """Return True if shape (with pad_mask_bool) can be placed at world (x,y)."""
        w_s, h_s = shape["w"], shape["h"]
        # top-left in occupancy coords (subtract anchor and origin)
        px = int(round(x - shape["anchor"][0])) - origin_x
        py = int(round(y - shape["anchor"][1])) - origin_y

        # bounds check
        if px < 0 or py < 0 or px + w_s > W or py + h_s > H:
            return False

        # containment: candidate polygon must lie fully inside mask
        dx, dy = x - shape["anchor"][0], y - shape["anchor"][1]
        cand_padded_world = affinity.translate(padded_local, xoff=dx, yoff=dy)
        if not base_poly.contains(cand_padded_world):
            return False

        # occupancy collision (pixel-wise)
        roi = occupancy[py:py + h_s, px:px + w_s]
        # pad_mask_bool is boolean mask (h_s,w_s)
        if np.any(roi[pad_mask_bool]):
            return False

        return True

    def commit_place(shape, x, y, pad_mask_bool):
        """Mark occupancy and append to placed list."""
        w_s, h_s = shape["w"], shape["h"]
        px = int(round(x - shape["anchor"][0])) - origin_x
        py = int(round(y - shape["anchor"][1])) - origin_y
        roi = occupancy[py:py + h_s, px:px + w_s]
        roi = roi.copy()
        roi[pad_mask_bool] = 1
        occupancy[py:py + h_s, px:px + w_s] = roi
        placed.append((shape, (x, y)))

    # ---- main loop: iterate shapes in order ----
    for shape in shapes:
        # start with original image & polygon (local coords)
        rot_img = shape["img"].copy()
        rot_poly = shape["poly"]

        # optional random rotation (rotate both the polygon and the RGBA image)
        if random_rotate:
            angle_deg = random.uniform(0, max_rotation)
            cx, cy = shape["anchor"]
            rot_poly = affinity.rotate(rot_poly, angle_deg, origin=shape["anchor"])
            M = cv2.getRotationMatrix2D((cx, cy), -angle_deg, 1.0)
            rot_img = cv2.warpAffine(
                shape["img"], M, (shape["w"], shape["h"]),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(0, 0, 0, 0)
            )

        # padded polygon for containment tests
        padded_local = rot_poly.buffer(padding) if padding > 0 else rot_poly

        # pixel padded alpha mask for occupancy tests
        pad_mask_bool = make_padded_mask(rot_img)  # shape (h,w) boolean

        # pick candidate generator for this shape
        if pack_mode == "spiral":
            candidates = spiral_candidates(centroid)
        elif pack_mode == "random":
            candidates = random_candidates(base_poly, n=max_random_tries)
        elif pack_mode == "edge":
            candidates = edge_inward_candidates(base_poly, step=edge_step)
        else:
            raise ValueError(f"Unknown pack_mode: {pack_mode}")

        placed_flag = False
        for (x, y) in candidates:
            if can_place_at(shape, x, y, pad_mask_bool, padded_local):
                # create new_shape with rotated geometry & image for rendering
                new_shape = {
                    "poly": rot_poly,
                    "padded_local": padded_local,
                    "img": rot_img,
                    "anchor": shape["anchor"],
                    "w": shape["w"],
                    "h": shape["h"],
                    "path": shape.get("path", ""),
                }
                # commit to occupancy and list
                commit_place(new_shape, x, y, pad_mask_bool)
                placed_flag = True

                # animate preview
                if animate:
                    canvas = visualize(placed, base_poly=base_poly_local, out_size=(W, H),
                                       bg_color=bg_color, debug_shapes=debug_view, debug_mask=debug_mask)
                    ax.clear()
                    ax.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
                    ax.axis("off")
                    plt.pause(0.12)
                break

        if not placed_flag:
            print(f"⚠️ Could not place shape (skipped): {shape.get('path','<unknown>')}")

    if animate:
        plt.ioff()
        plt.show()

    return placed



# ----------------------------
# 3. Rendering (same as before)
# ----------------------------

def visualize(
    placed,
    base_poly=None,
    out_size=None,
    bg_color=None,
    debug_mask=False,
    debug_shapes=False,
    mask_color=(255, 0, 0, 128)
):
    """
    Visualize packed shapes on a canvas with optional overlays.
    - base_poly: Shapely polygon of mask in pixel coordinates
    - debug_mask: show mask overlay
    - debug_shapes: show polygons of placed shapes (true + padded)
    """
    W, H = out_size
    canvas = np.zeros((H, W, 4), dtype=np.uint8)

    # Fill background
    if bg_color is not None:
        rgb = tuple(bg_color[:3])
        canvas[:, :, :3] = rgb
        canvas[:, :, 3] = bg_color[3] if len(bg_color) >= 4 else 255

    # ---- Debug: base mask overlay ----
    if debug_mask and base_poly is not None:
        overlay = canvas.copy()
        alpha_val = mask_color[3] if len(mask_color) >= 4 else 128
        polys = list(base_poly.geoms) if isinstance(base_poly, MultiPolygon) else [base_poly]
        for poly in polys:
            coords = np.array(poly.exterior.coords, dtype=np.int32)
            pts = coords.reshape((-1, 1, 2))
            b, g, r = int(mask_color[2]), int(mask_color[1]), int(mask_color[0])
            cv2.fillPoly(overlay, [pts], color=(b, g, r, int(alpha_val)))

        # Blend overlay
        ov_a = (overlay[:, :, 3:4].astype(np.float32) / 255.0)
        canvas[:, :, :3] = (ov_a * overlay[:, :, :3].astype(np.float32) +
                             (1 - ov_a) * canvas[:, :, :3].astype(np.float32)).astype(np.uint8)
        canvas[:, :, 3] = np.clip(canvas[:, :, 3].astype(np.float32) + overlay[:, :, 3].astype(np.float32), 0, 255).astype(np.uint8)

    # ---- Draw packed shapes ----
    for shape, (x, y) in placed:
        px = int(round(x - shape["anchor"][0]))
        py = int(round(y - shape["anchor"][1]))
        img = shape["img"]
        h, w = img.shape[:2]

        # ---- safe ROI blending to prevent broadcasting errors ----
        px0 = max(px, 0)
        py0 = max(py, 0)
        px1 = min(px + w, W)
        py1 = min(py + h, H)

        x0 = px0 - px
        y0 = py0 - py
        x1 = x0 + (px1 - px0)
        y1 = y0 + (py1 - py0)

        roi = canvas[py0:py1, px0:px1].astype(np.float32)
        alpha_sub = img[y0:y1, x0:x1, 3:4].astype(np.float32) / 255.0
        img_sub = img[y0:y1, x0:x1, :3].astype(np.float32)

        roi[:, :, :3] = alpha_sub * img_sub + (1 - alpha_sub) * roi[:, :, :3]
        roi[:, :, 3:4] = np.clip(roi[:, :, 3:4] + img[y0:y1, x0:x1, 3:4].astype(np.float32), 0, 255)
        canvas[py0:py1, px0:px1] = roi.astype(np.uint8)

        # Debug: draw polygons of shapes
        if debug_shapes:
            # Padded polygon in red
            padded_poly = getattr(shape, "padded_local", shape["poly"])
            moved_pad = affinity.translate(padded_poly, xoff=x - shape["anchor"][0], yoff=y - shape["anchor"][1])
            coords_pad = np.array(moved_pad.exterior.coords, dtype=np.int32)
            cv2.polylines(canvas, [coords_pad], True, (0, 0, 255, 255), 1)

            # True polygon in green
            moved_true = affinity.translate(shape["poly"], xoff=x - shape["anchor"][0], yoff=y - shape["anchor"][1])
            coords_true = np.array(moved_true.exterior.coords, dtype=np.int32)
            cv2.polylines(canvas, [coords_true], True, (0, 255, 0, 255), 2)

    return canvas



# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    base_poly, out_size = load_base_shape(base_image_path)
    paths = glob.glob(folder)
    if not paths:
        raise RuntimeError(f"No PNGs found at {folder}")

    shapes = [get_shape(p, scale_factor) for p in paths]
    placed = pack_shapes(shapes, base_poly,
                        padding=padding,
                        random_rotate=random_rotate,
                        max_rotation=max_rotation,
                        animate=animate,
                        pack_mode="random", debug_mask=debug_mask, debug_view=debug_view)   # "spiral" | "random" | "edge"

    result = visualize(placed, base_poly=base_poly, out_size=out_size, bg_color=bg_color, debug_mask=debug_mask,debug_shapes=debug_view )
    cv2.imwrite("packed_into_shape.png", result)
    print("✅ Saved packed_into_shape.png")

    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    plt.axis("off")
    plt.show()
