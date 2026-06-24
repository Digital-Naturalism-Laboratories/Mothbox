"""
collect_yolo_training_data.py

Recursively searches a source directory for:
  1. Images with matching x-anylabeling JSON ground truth files  → converted to YOLO format
  2. Folders already in YOLO format (images/ + labels/ structure) → copied directly

All data is merged and organized into a single YOLO-compatible dataset folder,
then split into train/val/test with a data.yaml generated automatically.

Usage:
    python collect_yolo_training_data.py \
        --source /path/to/your/data \
        --output /path/to/yolo_dataset

    # Custom split
    python collect_yolo_training_data.py -s /data -o /out --split 0.8 0.1 0.1

    # Override class list (default is just "creature")
    python collect_yolo_training_data.py -s /data -o /out --classes creature moth beetle

X-AnyLabeling JSON format expected:
    {
        "shapes": [
            {
                "label": "creature",
                "shape_type": "rectangle",   # or "polygon"
                "points": [[x1, y1], [x2, y2]]
            },
            ...
        ],
        "imageWidth": 1920,
        "imageHeight": 1080
    }

Existing YOLO folders are detected by the presence of sibling
"images/" and "labels/" subdirectories (standard YOLO layout).
"""

import json
import shutil
import random
import argparse
import yaml
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}

DEFAULT_CLASSES = ["creature"]


# ---------------------------------------------------------------------------
# Detection: find existing YOLO-format dataset roots
# ---------------------------------------------------------------------------

def find_yolo_dataset_roots(source_dir):
    """
    Walk source_dir and identify subdirectories that already contain YOLO-
    formatted data, i.e. they have both an 'images' and a 'labels' child
    directory with matching files.

    Returns a list of Path objects, each being a YOLO dataset root
    (the parent of images/ and labels/).

    We deliberately avoid descending *into* detected YOLO roots so their
    internal train/val/test sub-splits don't get double-counted.
    """
    source_dir = Path(source_dir)
    yolo_roots = []
    yolo_root_set = set()

    for candidate in sorted(source_dir.rglob("images")):
        if not candidate.is_dir():
            continue
        labels_dir = candidate.parent / "labels"
        if not labels_dir.is_dir():
            continue

        # Make sure there are actually matching image+label pairs
        img_stems = {p.stem for p in candidate.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS}
        lbl_stems = {p.stem for p in labels_dir.rglob("*.txt")}
        if not (img_stems & lbl_stems):
            continue

        root = candidate.parent
        # Avoid nested roots (keep outermost)
        if any(str(root).startswith(str(r)) for r in yolo_root_set):
            continue
        yolo_roots.append(root)
        yolo_root_set.add(root)

    return yolo_roots


def collect_yolo_pairs_from_root(yolo_root):
    """
    From a YOLO dataset root (contains images/ and labels/ dirs, possibly
    with train/val/test sub-splits), collect all (image_path, label_path) pairs.

    Returns list of (image_path, label_path) tuples.
    """
    images_dir = yolo_root / "images"
    labels_dir = yolo_root / "labels"
    pairs = []

    for img_path in images_dir.rglob("*"):
        if img_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        # Mirror the sub-path structure to find the label file
        rel = img_path.relative_to(images_dir)
        label_path = labels_dir / rel.with_suffix(".txt")
        if label_path.exists():
            pairs.append((img_path, label_path))

    return pairs


# ---------------------------------------------------------------------------
# Detection: find x-anylabeling JSON pairs
# ---------------------------------------------------------------------------

def find_anylabeling_pairs(source_dir, skip_dirs):
    """
    Recursively walk source_dir (excluding skip_dirs) for images that have
    a sibling x-anylabeling .json file with at least one shape annotation.

    skip_dirs: set of Path objects to exclude (i.e. detected YOLO roots).

    Returns list of (image_path, json_path) tuples.
    """
    source_dir = Path(source_dir)
    pairs = []
    skipped_no_json = 0
    skipped_in_yolo = 0

    for img_path in source_dir.rglob("*"):
        if img_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        # Skip files that live inside an already-detected YOLO root
        if any(str(img_path).startswith(str(d)) for d in skip_dirs):
            skipped_in_yolo += 1
            continue

        # Skip inference output files
        if "_botdetection" in img_path.stem:
            continue

        json_path = img_path.with_suffix(".json")
        if not json_path.exists() or "_botdetection" in json_path.stem:
            skipped_no_json += 1
            continue

        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            # Empty shapes = intentional background image, still include it
        except (json.JSONDecodeError, KeyError):
            print(f"  [WARN] Could not parse JSON: {json_path}")
            continue

        pairs.append((img_path, json_path))

    print(f"  Found {len(pairs)} x-anylabeling labeled pairs (includes background images)")
    print(f"  Skipped {skipped_no_json} images with no JSON")
    if skipped_in_yolo:
        print(f"  Skipped {skipped_in_yolo} images already inside YOLO folders")
    return pairs


# ---------------------------------------------------------------------------
# Class name collection
# ---------------------------------------------------------------------------

def collect_class_names_from_json(pairs):
    """Scan all x-anylabeling JSONs and return sorted unique label names."""
    class_names = set()
    for _, json_path in pairs:
        with open(json_path, "r") as f:
            data = json.load(f)
        for shape in data.get("shapes", []):
            label = shape.get("label", "").strip()
            if label:
                class_names.add(label)
    return sorted(class_names)


# ---------------------------------------------------------------------------
# Conversion: x-anylabeling → YOLO
# ---------------------------------------------------------------------------

def shape_to_yolo_line(shape, img_width, img_height, class_map):
    """
    Convert one x-anylabeling shape to a YOLO OBB label line.

    YOLO OBB format:  class_id x1 y1 x2 y2 x3 y3 x4 y4  (all normalized 0-1)

    x-anylabeling "rotation" shapes already provide 4 corner points in order,
    so we normalize each point directly — no bounding-box collapsing needed.

    For "rectangle" shapes (axis-aligned, 4 points) we do the same: the 4
    corners are already correct OBB corners with 0° rotation.

    Any shape with exactly 4 points is handled this way.
    Shapes with != 4 points (rare polygons, etc.) fall back to computing
    the 4 corners of their axis-aligned bounding box, which gives a valid
    but unrotated OBB — still better than discarding the annotation.

    Returns None if the shape is invalid or label is not in class_map.
    """
    label = shape.get("label", "").strip()
    if label not in class_map:
        return None

    points = shape.get("points", [])
    if not points:
        return None

    try:
        if len(points) == 4:
            # Direct OBB: normalize the 4 corners as-is
            coords = []
            for px, py in points:
                nx = max(0.0, min(1.0, px / img_width))
                ny = max(0.0, min(1.0, py / img_height))
                coords.extend([nx, ny])

        else:
            # Fallback: compute axis-aligned bounding box corners
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            x1, x2 = min(xs), max(xs)
            y1, y2 = min(ys), max(ys)
            if (x2 - x1) <= 0 or (y2 - y1) <= 0:
                return None
            # 4 corners in order: top-left, top-right, bottom-right, bottom-left
            corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            coords = []
            for px, py in corners:
                coords.extend([
                    max(0.0, min(1.0, px / img_width)),
                    max(0.0, min(1.0, py / img_height)),
                ])

        coord_str = " ".join(f"{v:.6f}" for v in coords)
        return f"{class_map[label]} {coord_str}"

    except (IndexError, TypeError, ZeroDivisionError):
        return None


def json_to_yolo_lines(json_path, class_map):
    """Convert an x-anylabeling JSON to a list of YOLO label strings."""
    with open(json_path, "r") as f:
        data = json.load(f)

    img_width  = data.get("imageWidth")
    img_height = data.get("imageHeight")

    if not img_width or not img_height:
        print(f"  [WARN] Missing image dimensions in {json_path}")
        return []

    return [
        line for shape in data.get("shapes", [])
        if (line := shape_to_yolo_line(shape, img_width, img_height, class_map))
    ]


# ---------------------------------------------------------------------------
# Splitting
# ---------------------------------------------------------------------------

def split_items(items, train_ratio, val_ratio, test_ratio, seed):
    """Shuffle and split a list into (train, val, test)."""
    random.seed(seed)
    shuffled = items[:]
    random.shuffle(shuffled)

    n = len(shuffled)
    n_train = int(n * train_ratio)
    n_val   = int(n * val_ratio)

    return (
        shuffled[:n_train],
        shuffled[n_train:n_train + n_val],
        shuffled[n_train + n_val:],
    )


# ---------------------------------------------------------------------------
# Copying helpers
# ---------------------------------------------------------------------------

def safe_dest_name(filename, dest_dir, parent_name):
    """
    Return a destination Path that doesn't collide with existing files.
    If filename already exists, prefix with parent folder name.
    """
    dest = dest_dir / filename
    if dest.exists():
        dest = dest_dir / f"{parent_name}__{filename}"
    return dest


def copy_anylabeling_pair(img_path, json_path, img_out_dir, label_out_dir, class_map, counts, bg_counts):
    """Copy one x-anylabeling pair: convert JSON → YOLO txt, copy image.
    Empty label files (background images) are counted separately in bg_counts."""
    dest_img = safe_dest_name(img_path.name, img_out_dir, img_path.parent.name)
    shutil.copy2(img_path, dest_img)

    lines = json_to_yolo_lines(json_path, class_map)
    label_path = label_out_dir / (dest_img.stem + ".txt")
    with open(label_path, "w") as f:
        f.write("\n".join(lines))

    if not lines:
        bg_counts["background"] += 1
    else:
        for line in lines:
            counts[int(line.split()[0])] += 1


def copy_yolo_pair(img_path, label_path, img_out_dir, label_out_dir, counts, bg_counts):
    """Copy one existing YOLO (image, label) pair directly.
    Empty label files (background images) are counted separately in bg_counts."""
    dest_img = safe_dest_name(img_path.name, img_out_dir, img_path.parent.name)
    shutil.copy2(img_path, dest_img)

    dest_lbl = label_out_dir / (dest_img.stem + ".txt")
    shutil.copy2(label_path, dest_lbl)

    # Count annotations from the existing label file
    has_annotations = False
    try:
        with open(label_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    counts[int(line.split()[0])] += 1
                    has_annotations = True
    except (ValueError, IndexError):
        pass

    if not has_annotations:
        bg_counts["background"] += 1


def populate_split(split_name, anylabeling_pairs, yolo_pairs, output_dir, class_map, stats):
    """
    Write all pairs for one split (train/val/test) to the output directory.
    anylabeling_pairs: list of (img_path, json_path)
    yolo_pairs:        list of (img_path, label_path)
    stats stores both annotation counts and background image counts per split.
    """
    img_out_dir   = Path(output_dir) / "images" / split_name
    label_out_dir = Path(output_dir) / "labels" / split_name
    img_out_dir.mkdir(parents=True, exist_ok=True)
    label_out_dir.mkdir(parents=True, exist_ok=True)

    counts    = defaultdict(int)
    bg_counts = defaultdict(int)

    for img_path, json_path in anylabeling_pairs:
        copy_anylabeling_pair(img_path, json_path, img_out_dir, label_out_dir, class_map, counts, bg_counts)

    for img_path, label_path in yolo_pairs:
        copy_yolo_pair(img_path, label_path, img_out_dir, label_out_dir, counts, bg_counts)

    stats[split_name] = {"annotations": dict(counts), "background": bg_counts["background"]}


# ---------------------------------------------------------------------------
# data.yaml
# ---------------------------------------------------------------------------

def write_data_yaml(output_dir, class_names, has_test):
    output_dir = Path(output_dir)
    yaml_data = {
        "path":  str(output_dir.resolve()),
        "train": "images/train",
        "val":   "images/val",
        "nc":    len(class_names),
        "names": class_names,
    }
    if has_test:
        yaml_data["test"] = "images/test"

    yaml_path = output_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
    print(f"\nWrote data.yaml → {yaml_path}")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_summary(output_dir, class_names, stats, yolo_roots, n_anylabeling):
    print("\n" + "=" * 55)
    print("DATASET COLLECTION SUMMARY")
    print("=" * 55)

    print(f"\nSources:")
    print(f"  x-anylabeling pairs converted : {n_anylabeling}")
    print(f"  Pre-existing YOLO folders used : {len(yolo_roots)}")
    for r in yolo_roots:
        print(f"    {r}")

    total_bg_all = sum(v["background"] for v in stats.values())
    print(f"  Background (empty label) images total: {total_bg_all}")

    for split, data in stats.items():
        counts = data["annotations"]
        n_bg   = data["background"]
        total_imgs = sum(1 for _ in (Path(output_dir) / "images" / split).iterdir())
        total_anns = sum(counts.values())
        print(f"\n{split.upper()}  ({total_imgs} images | {total_anns} annotations | {n_bg} background)")
        for class_id, count in sorted(counts.items()):
            name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"
            print(f"  {name}: {count}")
        if n_bg:
            print(f"  background (no annotations): {n_bg}")

    print(f"\nOutput: {output_dir}")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Collect x-anylabeling ground truth data AND existing YOLO datasets "
            "from a source directory, merge them, and output a single YOLO dataset."
        )
    )
    parser.add_argument("--source", "-s", required=True,
        help="Root directory to search (searched recursively)")
    parser.add_argument("--output", "-o", required=True,
        help="Output directory for the merged YOLO dataset")
    parser.add_argument("--split", nargs=3, type=float, default=[0.8, 0.1, 0.1],
        metavar=("TRAIN", "VAL", "TEST"),
        help="Train/val/test ratios (must sum to 1.0). Default: 0.8 0.1 0.1")
    parser.add_argument("--seed", type=int, default=42,
        help="Random seed for reproducible splits (default: 42)")
    parser.add_argument("--classes", nargs="+", default=None,
        help=(
            "Class names in order (determines class IDs). "
            f"Default: {DEFAULT_CLASSES}. "
            "Labels not in this list are skipped. "
            "Example: --classes creature moth beetle"
        ))
    args = parser.parse_args()

    train_r, val_r, test_r = args.split
    if abs(train_r + val_r + test_r - 1.0) > 1e-6:
        raise ValueError(f"Split ratios must sum to 1.0, got {train_r + val_r + test_r:.4f}")

    source_dir = Path(args.source)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Detect existing YOLO dataset roots
    # ------------------------------------------------------------------
    print(f"\n[1/5] Scanning for existing YOLO-format folders in: {source_dir}")
    yolo_roots = find_yolo_dataset_roots(source_dir)
    print(f"  Found {len(yolo_roots)} YOLO dataset root(s):")
    for r in yolo_roots:
        print(f"    {r}")

    all_yolo_pairs = []
    for root in yolo_roots:
        pairs = collect_yolo_pairs_from_root(root)
        print(f"  → {len(pairs)} labeled pairs from {root.name}/")
        all_yolo_pairs.extend(pairs)

    # ------------------------------------------------------------------
    # 2. Find x-anylabeling pairs (excluding YOLO roots)
    # ------------------------------------------------------------------
    print(f"\n[2/5] Scanning for x-anylabeling JSON pairs...")
    skip_dirs = {r for r in yolo_roots}
    anylabeling_pairs = find_anylabeling_pairs(source_dir, skip_dirs)

    # ------------------------------------------------------------------
    # 3. Resolve class names
    # ------------------------------------------------------------------
    print(f"\n[3/5] Resolving class names...")
    if args.classes:
        class_names = args.classes
        print(f"  Using manually specified classes: {class_names}")
    elif anylabeling_pairs:
        class_names = collect_class_names_from_json(anylabeling_pairs)
        if not class_names:
            class_names = DEFAULT_CLASSES
            print(f"  No labels found in JSONs, defaulting to: {class_names}")
        else:
            print(f"  Auto-detected classes: {class_names}")
    else:
        class_names = DEFAULT_CLASSES
        print(f"  No x-anylabeling data found, defaulting to: {class_names}")

    print(f"  Class map:")
    class_map = {name: i for i, name in enumerate(class_names)}
    for name, cid in class_map.items():
        print(f"    {cid}: {name}")

    # ------------------------------------------------------------------
    # 4. Split both pools and populate output
    # ------------------------------------------------------------------
    print(f"\n[4/5] Splitting and copying files...")

    al_train, al_val, al_test = split_items(anylabeling_pairs, train_r, val_r, test_r, args.seed)
    yl_train, yl_val, yl_test = split_items(all_yolo_pairs,    train_r, val_r, test_r, args.seed)

    total = len(anylabeling_pairs) + len(all_yolo_pairs)
    print(f"  Total images: {total}")
    print(f"    train: {len(al_train) + len(yl_train)}")
    print(f"    val:   {len(al_val)   + len(yl_val)}")
    print(f"    test:  {len(al_test)  + len(yl_test)}")

    stats = {}
    populate_split("train", al_train, yl_train, output_dir, class_map, stats)
    populate_split("val",   al_val,   yl_val,   output_dir, class_map, stats)
    if al_test or yl_test:
        populate_split("test", al_test, yl_test, output_dir, class_map, stats)

    # ------------------------------------------------------------------
    # 5. Write data.yaml
    # ------------------------------------------------------------------
    print(f"\n[5/5] Writing data.yaml...")
    write_data_yaml(output_dir, class_names, has_test=bool(al_test or yl_test))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print_summary(output_dir, class_names, stats, yolo_roots, len(anylabeling_pairs))


if __name__ == "__main__":
    main()