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
folder = r"D:\x-anylabeling-matting\onlybig\*.png"

scale_factor = 0.2         # global scale factor (applied to all images first)

# 🔀 NEW: random scaling options
random_scale = False       # enable per-image random scale
min_scale = 0.1            # min relative scale factor
max_scale = 2.5            # max relative scale factor

animate = True             # step-by-step animation
bg_color = None            # None = transparent, or (R,G,B)
random_rotate = True       # rotate shapes randomly
max_rotation = 360         # max random rotation (degrees)
debug_view = False          # outline view instead of images
padding = 10                # polygon padding (collision spacing)
out_size = (1500, 1500)    # output canvas size


# ----------------------------
# 1. Load + preprocess image
# ----------------------------
def get_shape(path, scale_factor=1.0):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # RGBA expected
    if img is None or img.shape[2] < 4:
        raise ValueError(f"Image {path} missing alpha channel")

    # Global scale first
    if scale_factor != 1.0:
        img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor,
                         interpolation=cv2.INTER_AREA)

    # Random per-image scaling (applied AFTER global scaling)
    if random_scale:
        factor = random.uniform(min_scale, max_scale)
        img = cv2.resize(img, None, fx=factor, fy=factor,
                         interpolation=cv2.INTER_AREA)

    alpha = img[:, :, 3]
    mask = (alpha > 0).astype(np.uint8) * 255

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)

    # Simplify contour
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
# 2. Packing algorithm
# ----------------------------
def pack_shapes(shapes,
                padding=0,
                random_rotate=False,
                max_rotation=360,
                animate=False):
    placed = []
    center = (0, 0)

    if animate:
        plt.ion()
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect("equal")
        ax.axis("off")

    for shape in shapes:
        rot_img = shape["img"]
        rot_poly = shape["poly"]

        if random_rotate:
            angle_deg = random.uniform(0, max_rotation)
            cx, cy = shape["anchor"]

            # Rotate polygon
            rot_poly = affinity.rotate(rot_poly, angle_deg, origin=shape["anchor"])

            # Rotate image
            M = cv2.getRotationMatrix2D((cx, cy), angle_deg, 1.0)
            rot_img = cv2.warpAffine(
                shape["img"], M, (shape["w"], shape["h"]),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(0, 0, 0, 0)
            )

        padded_local = rot_poly.buffer(padding) if padding > 0 else rot_poly

        theta, radius = 0.0, 50.0
        while True:
            x = center[0] + radius * math.cos(theta)
            y = center[1] + radius * math.sin(theta)

            dx, dy = x - shape["anchor"][0], y - shape["anchor"][1]
            cand_padded_world = affinity.translate(padded_local, xoff=dx, yoff=dy)

            # check collisions
            collision = False
            for placed_shape, (px, py) in placed:
                placed_padded_world = affinity.translate(
                    placed_shape["padded_local"],
                    xoff=px - placed_shape["anchor"][0],
                    yoff=py - placed_shape["anchor"][1]
                )
                if cand_padded_world.intersects(placed_padded_world):
                    collision = True
                    break

            if not collision:
                new_shape = {
                    "poly": rot_poly,
                    "padded_local": padded_local,
                    "img": rot_img,
                    "anchor": shape["anchor"],
                    "w": shape["w"],
                    "h": shape["h"],
                    "path": shape["path"],
                }
                placed.append((new_shape, (x, y)))

                if animate:
                    canvas = visualize(placed, out_size=out_size, bg_color=bg_color, debug=debug_view)
                    ax.clear()
                    ax.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
                    ax.axis("off")
                    plt.pause(0.15)
                break
            else:
                theta += 0.25
                radius += 0.7

    if animate:
        plt.ioff()
        plt.show()

    return placed


# ----------------------------
# 3. Rendering
# ----------------------------
def visualize(placed, out_size=(1500, 1500), bg_color=None, debug=False):
    if bg_color is None:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)
    else:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)
        canvas[:, :, :3] = bg_color
        canvas[:, :, 3] = 255

    cx, cy = out_size[0] // 2, out_size[1] // 2

    for shape, (x, y) in placed:
        px = cx + int(x - shape["anchor"][0])
        py = cy + int(y - shape["anchor"][1])

        if debug:
            moved_pad = affinity.translate(shape["padded_local"], xoff=x - shape["anchor"][0], yoff=y - shape["anchor"][1])
            pts_pad = np.array(moved_pad.exterior.coords, dtype=np.int32)
            pts_pad[:, 0] += cx
            pts_pad[:, 1] += cy
            cv2.polylines(canvas, [pts_pad], True, (0, 0, 255, 255), 1)

            moved_true = affinity.translate(shape["poly"], xoff=x - shape["anchor"][0], yoff=y - shape["anchor"][1])
            pts_true = np.array(moved_true.exterior.coords, dtype=np.int32)
            pts_true[:, 0] += cx
            pts_true[:, 1] += cy
            cv2.polylines(canvas, [pts_true], True, (0, 255, 0, 255), 2)
        else:
            img = shape["img"]
            h, w = img.shape[:2]
            if px < 0 or py < 0 or px + w > out_size[0] or py + h > out_size[1]:
                continue
            roi = canvas[py:py + h, px:px + w]
            alpha = img[:, :, 3:] / 255.0
            roi[:, :, :3] = (1 - alpha) * roi[:, :, :3] + alpha * img[:, :, :3]
            roi[:, :, 3:] = np.clip(roi[:, :, 3:] + img[:, :, 3:], 0, 255)

    return canvas


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    paths = glob.glob(folder)

    # Choose how to sort
    sort_mode = "reverse"       # options: "alphabetical", "reverse", "none"

    if sort_mode == "alphabetical":
        paths = sorted(paths)
    elif sort_mode == "reverse":
        paths = sorted(paths, reverse=True)
    elif sort_mode == "none":
        pass  # keep as returned by glob
    else:
        raise ValueError(f"Unknown sort_mode: {sort_mode}")




    if not paths:
        raise RuntimeError(f"No PNGs found at {folder}")

    shapes = [get_shape(p, scale_factor) for p in paths]

    placed = pack_shapes(shapes,
                         padding=padding,
                         random_rotate=random_rotate,
                         max_rotation=max_rotation,
                         animate=animate)

    result = visualize(placed, out_size=out_size, bg_color=bg_color, debug=debug_view)
    cv2.imwrite("packed_result.png", result)
    print("✅ Saved packed_result.png")

    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    plt.axis("off")
    plt.show()
