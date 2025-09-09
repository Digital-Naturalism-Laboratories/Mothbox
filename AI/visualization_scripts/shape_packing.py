import cv2
import numpy as np
import glob
import math
from shapely.geometry import Polygon
from shapely import affinity
import matplotlib.pyplot as plt

# ----------------------------
# CONFIG
# ----------------------------
folder = r"D:\x-anylabeling-matting\onlybig\*.png"  # default folder
scale_factor = 0.2       # set to 1.0 for no scaling
animate = True           # set False to skip animation
bg_color = (255,240,50)          # e.g., (255, 255, 255) for white, None = transparent


# ----------------------------
# 1. Load image + extract contour
# ----------------------------
def get_shape(path, scale_factor=1.0):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # RGBA
    if img is None or img.shape[2] < 4:
        raise ValueError(f"Image {path} is missing an alpha channel")

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

    # Polygon in image coords
    poly = Polygon(approx.reshape(-1, 2))

    # Compute centroid (to use as anchor point)
    cx, cy = poly.centroid.coords[0]

    return {
        "poly": poly,
        "img": img,
        "anchor": (cx, cy),
        "w": img.shape[1],
        "h": img.shape[0],
    }


# ----------------------------
# 2. Packing algorithm
# ----------------------------
def pack_shapes(shapes, spacing=5, animate=False):
    placed = []
    center = (0, 0)

    # Prepare matplotlib live plot if animating
    if animate:
        plt.ion()
        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.axis("off")

    # Place first shape
    first = shapes[0]
    placed.append((first, (0, 0)))

    if animate:
        canvas = visualize(placed, bg_color=bg_color)
        ax.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
        plt.pause(0.5)

    for shape in shapes[1:]:
        angle = 0
        radius = 50
        placed_successfully = False

        while not placed_successfully:
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)

            dx = x - shape["anchor"][0]
            dy = y - shape["anchor"][1]
            moved_poly = affinity.translate(shape["poly"], xoff=dx, yoff=dy)

            if not any(moved_poly.intersects(
                        affinity.translate(p["poly"],
                                           xoff=px - p["anchor"][0],
                                           yoff=py - p["anchor"][1]).buffer(spacing))
                       for p, (px, py) in placed):
                placed.append((shape, (x, y)))
                placed_successfully = True

                if animate:
                    canvas = visualize(placed, bg_color=bg_color)
                    ax.clear()
                    ax.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGRA2RGBA))
                    ax.axis("off")
                    plt.pause(0.2)
            else:
                angle += 0.2
                radius += 0.5

    if animate:
        plt.ioff()
        plt.show()

    return placed


# ----------------------------
# 3. Render composite
# ----------------------------
def visualize(placed, out_size=(1500, 1500), bg_color=None):
    # Create canvas with optional background color
    if bg_color is None:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)  # transparent
    else:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)
        canvas[:, :, :3] = bg_color
        canvas[:, :, 3] = 255  # opaque

    cx, cy = out_size[0] // 2, out_size[1] // 2

    for shape, (x, y) in placed:
        img = shape["img"]
        h, w = shape["h"], shape["w"]

        px = cx + int(x - shape["anchor"][0])
        py = cy + int(y - shape["anchor"][1])

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
    shapes = [get_shape(path, scale_factor) for path in glob.glob(folder)]
    if not shapes:
        raise RuntimeError("No PNGs found!")

    placed = pack_shapes(shapes, animate=animate)

    result = visualize(placed, bg_color=bg_color)

    cv2.imwrite("packed_result.png", result)
    print("✅ Saved result as packed_result.png")

    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    plt.axis("off")
    plt.show()
