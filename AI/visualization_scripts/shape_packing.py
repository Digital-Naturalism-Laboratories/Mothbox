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
scale_factor = 0.2        # scale factor for all shapes
animate = True            # step-by-step animation
bg_color = None           # None = transparent, or (R,G,B)
random_rotate = True      # rotate shapes randomly
max_rotation = 360        # max random rotation (degrees)
debug_view = True        # if True, show outlines instead of images
padding = 10               # extra padding around each shape (in pixels)


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

    # Compute centroid
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
def pack_shapes(shapes, spacing=5, animate=False,
                random_rotate=False, max_rotation=360,
                padding=0):
    placed = []
    center = (0, 0)

    if animate:
        plt.ion()
        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.axis("off")

    for shape in shapes:
        # Random rotation
        rotated_img = shape["img"]
        rotated_poly = shape["poly"]

        if random_rotate:
            angle_deg = random.uniform(0, max_rotation)
            h, w = shape["h"], shape["w"]

            # Rotate image
            M = cv2.getRotationMatrix2D((w/2, h/2), angle_deg, 1.0)
            rotated_img = cv2.warpAffine(
                rotated_img, M, (w, h),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(0, 0, 0, 0)
            )

            # Rotate polygon
            rotated_poly = affinity.rotate(rotated_poly, angle_deg, origin=shape["anchor"])

        # Apply padding
        if padding > 0:
            padded_poly = rotated_poly.buffer(padding)
        else:
            padded_poly = rotated_poly

        # Spiral placement
        angle = 0
        radius = 50
        placed_successfully = False

        while not placed_successfully:
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)

            dx = x - shape["anchor"][0]
            dy = y - shape["anchor"][1]
            moved_poly = affinity.translate(padded_poly, xoff=dx, yoff=dy)

            # Collision check
            if not any(
                moved_poly.intersects(
                    affinity.translate(
                        p["poly"],
                        xoff=px - p["anchor"][0],
                        yoff=py - p["anchor"][1]
                    )
                )
                for p, (px, py) in placed
            ):
                new_shape = shape.copy()
                new_shape["img"] = rotated_img
                new_shape["poly"] = padded_poly  # store padded version
                placed.append((new_shape, (x, y)))
                placed_successfully = True

                if animate:
                    canvas = visualize(placed, bg_color=bg_color, debug=debug_view)
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
def visualize(placed, out_size=(1500, 1500), bg_color=None, debug=False):
    if bg_color is None:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)
    else:
        canvas = np.zeros((out_size[1], out_size[0], 4), dtype=np.uint8)
        canvas[:, :, :3] = bg_color
        canvas[:, :, 3] = 255

    cx, cy = out_size[0] // 2, out_size[1] // 2

    for shape, (x, y) in placed:
        if debug:
            moved_poly = affinity.translate(
                shape["poly"], xoff=x - shape["anchor"][0], yoff=y - shape["anchor"][1]
            )
            pts = np.array(moved_poly.exterior.coords, dtype=np.int32)
            pts[:, 0] += cx
            pts[:, 1] += cy
            cv2.polylines(canvas, [pts], isClosed=True,
                          color=(0, 255, 0, 255), thickness=2)
        else:
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

    placed = pack_shapes(shapes, animate=animate,
                         random_rotate=random_rotate,
                         max_rotation=max_rotation,
                         padding=padding)

    result = visualize(placed, bg_color=bg_color, debug=debug_view)

    cv2.imwrite("packed_result.png", result)
    print("✅ Saved result as packed_result.png")

    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    plt.axis("off")
    plt.show()
