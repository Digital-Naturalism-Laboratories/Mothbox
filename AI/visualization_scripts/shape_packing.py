import cv2
import numpy as np
import glob
import math
import random
from shapely.geometry import Polygon
from shapely import affinity
import matplotlib.pyplot as plt

# ----------------------------
# CONFIG
# ----------------------------
folder = r"D:\x-anylabeling-matting\onlybig\test\*.png"
scale_factor = 0.2        # set to 1.0 for no scaling
animate = True            # show placement step-by-step
bg_color = (255,240,10)           # None = transparent, or (R,G,B) tuple like (255,255,255)
random_rotate = True      # rotate shapes randomly before placement
max_rotation = 360        # degrees
debug_view = False         # show polygon outlines instead of images (also shows padded)
padding = 10               # padding (pixels) used for collision test
out_size = (1500, 1500)   # canvas size


# ----------------------------
# 1. Load image + extract contour
# ----------------------------
def get_shape(path, scale_factor=1.0):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # RGBA expected
    if img is None or img.shape[2] < 4:
        raise ValueError(f"Image {path} missing an alpha channel")

    # Optionally scale image
    if scale_factor != 1.0:
        img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor,
                         interpolation=cv2.INTER_AREA)

    alpha = img[:, :, 3]
    mask = (alpha > 0).astype(np.uint8) * 255

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)

    # Simplify contour
    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Polygon in image-local coordinates
    poly_local = Polygon(approx.reshape(-1, 2))

    # Anchor is centroid (in local coords)
    cx, cy = poly_local.centroid.coords[0]

    return {
        "poly": poly_local,      # polygon in local coords (not translated)
        "img": img,              # image (may be rotated later)
        "anchor": (cx, cy),      # anchor in local image coords
        "w": img.shape[1],
        "h": img.shape[0],
        "path": path,
    }


# ----------------------------
# 2. Packing algorithm (fixed)
# ----------------------------
def pack_shapes(shapes,
                padding=0,
                random_rotate=False,
                max_rotation=360,
                animate=False):
    placed = []             # will contain tuples (shape_dict, (x,y))
    center = (0, 0)         # cluster center (world coords)

    # Setup interactive plot if animating
    if animate:
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect("equal")
        ax.axis("off")

    for shape in shapes:
        # Make local rotated copies (still in local image coordinates)
        rot_img = shape["img"]
        rot_poly = shape["poly"]

        if random_rotate:
            angle_deg = random.uniform(0, max_rotation)
            cx, cy = shape["anchor"]  # rotation center in image-local coords

            # Rotate polygon about the anchor
            rot_poly = affinity.rotate(rot_poly, angle_deg, origin=shape["anchor"])

            # Rotate image around the same anchor, so pixels align with polygon
            # Use same image canvas size (w,h). borderValue keeps RGBA transparent.
            M = cv2.getRotationMatrix2D((cx, cy), angle_deg, 1.0)
            rot_img = cv2.warpAffine(
                shape["img"], M, (shape["w"], shape["h"]),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(0, 0, 0, 0)
            )

        # Create padded polygon (still local coords)
        if padding and padding > 0:
            padded_local = rot_poly.buffer(padding)
        else:
            padded_local = rot_poly

        # Spiral search for placement
        theta = 0.0
        radius = 50.0
        placed_successfully = False

        while not placed_successfully:
            x = center[0] + radius * math.cos(theta)
            y = center[1] + radius * math.sin(theta)

            # Candidate polygon in world coords (translate by x - anchor.x, y - anchor.y)
            dx = x - shape["anchor"][0]
            dy = y - shape["anchor"][1]
            cand_padded_world = affinity.translate(padded_local, xoff=dx, yoff=dy)

            # Collision check against already-placed shapes (they have local padded polygons)
            collision = False
            for placed_shape, (px, py) in placed:
                # translate that placed shape's padded_local to world coords
                placed_padded_world = affinity.translate(placed_shape["padded_local"],
                                                        xoff=px - placed_shape["anchor"][0],
                                                        yoff=py - placed_shape["anchor"][1])
                if cand_padded_world.intersects(placed_padded_world):
                    collision = True
                    break

            if not collision:
                # Accept placement. Store rot_img and the local rot_poly/padded_local (still local coords)
                new_shape = {
                    "poly": rot_poly,                # rotated true polygon (local coords)
                    "padded_local": padded_local,    # padded polygon (local coords)
                    "img": rot_img,
                    "anchor": shape["anchor"],       # anchor remains in local coords
                    "w": shape["w"],
                    "h": shape["h"],
                    "path": shape["path"],
                }
                placed.append((new_shape, (x, y)))
                placed_successfully = True

                # animate if enabled
                if animate:
                    canvas = visualize(placed, out_size=out_size, bg_color=bg_color, debug=debug_view)
                    ax.clear()
                    ax.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
                    ax.axis("off")
                    plt.pause(0.15)
            else:
                # step along the spiral
                theta += 0.25
                radius += 0.7

    if animate:
        plt.ioff()
        plt.show()

    return placed


# ----------------------------
# 3. Render composite + debug outlines
# ----------------------------
def visualize(placed, out_size=(1500, 1500), bg_color=None, debug=False):
    if bg_color is None:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)  # RGBA transparent
    else:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)
        canvas[:, :, :3] = bg_color
        canvas[:, :, 3] = 255

    cx, cy = out_size[0] // 2, out_size[1] // 2

    for shape, (x, y) in placed:
        # world translation to top-left: px = cx + (x - anchor.x)
        px = cx + int(x - shape["anchor"][0])
        py = cy + int(y - shape["anchor"][1])

        if debug:
            # draw padded polygon in red (if present)
            if "padded_local" in shape and shape["padded_local"] is not None:
                moved_pad = affinity.translate(shape["padded_local"],
                                               xoff=x - shape["anchor"][0],
                                               yoff=y - shape["anchor"][1])
                pts_pad = np.array(moved_pad.exterior.coords, dtype=np.int32)
                pts_pad[:, 0] += cx
                pts_pad[:, 1] += cy
                cv2.polylines(canvas, [pts_pad], isClosed=True, color=(0, 0, 255, 255), thickness=1)

            # draw true polygon in green
            moved_true = affinity.translate(shape["poly"],
                                            xoff=x - shape["anchor"][0],
                                            yoff=y - shape["anchor"][1])
            pts_true = np.array(moved_true.exterior.coords, dtype=np.int32)
            pts_true[:, 0] += cx
            pts_true[:, 1] += cy
            cv2.polylines(canvas, [pts_true], isClosed=True, color=(0, 255, 0, 255), thickness=2)
        else:
            # composite image
            img = shape["img"]
            h, w = shape["h"], shape["w"]

            # skip if outside canvas
            if px < 0 or py < 0 or px + w > out_size[0] or py + h > out_size[1]:
                continue

            roi = canvas[py:py + h, px:px + w]
            alpha = img[:, :, 3:] / 255.0
            # blend RGB
            roi[:, :, :3] = (1 - alpha) * roi[:, :, :3] + alpha * img[:, :, :3]
            # accumulate alpha
            roi[:, :, 3:] = np.clip(roi[:, :, 3:] + img[:, :, 3:], 0, 255)

    return canvas


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    # load all shapes
    paths = sorted(glob.glob(folder))
    if not paths:
        raise RuntimeError(f"No PNGs found at: {folder}")

    shapes = [get_shape(p, scale_factor) for p in paths]

    # pack shapes
    placed = pack_shapes(shapes,
                         padding=padding,
                         random_rotate=random_rotate,
                         max_rotation=max_rotation,
                         animate=animate)

    # final render
    result = visualize(placed, out_size=out_size, bg_color=bg_color, debug=debug_view)

    # save + show
    cv2.imwrite("packed_result.png", result)
    print("✅ Saved packed_result.png")
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    plt.axis("off")
    plt.show()
