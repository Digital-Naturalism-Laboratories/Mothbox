"""
collect_yolo_training_data.py

Recursively searches one or more source directories for:
  1. Images with matching x-anylabeling JSON ground truth files  → converted to YOLO OBB format
  2. Folders already in YOLO format (images/ + labels/ structure) → copied directly
     (detection-format labels with 5 values are auto-converted to OBB 9-value format)

All data is merged and organized into a single YOLO-compatible dataset folder,
then split into train/val/test with a data.yaml generated automatically.

Optionally exports a TIGHTLY-ROTATED patch crop of every OBB annotation to a
patches/ folder for quick visual false-positive auditing before training.
This uses the same cv2.minAreaRect + warpAffine technique as detect.py's
crop_rect(), so patches look consistent with the bot-detection thumbnails
reviewers already use.

Usage:
    # Single source (original behaviour)
    python3 collect_yolo_training_data.py \
        --source /path/to/your/data \
        --output /path/to/yolo_dataset

    # Multiple sources — just repeat --source (or -s) for each folder
    python3 collect_yolo_training_data.py \
        --source /Users/automeris/Desktop/TrainingMac \
        --source '/Users/automeris/Desktop/MB Projects' \
        --source /home/user/extra_moths \
        --output /Users/automeris/Desktop/2026_MOTHBOTYOLO \
        --patches

    # With patch export for visual audit
    python3 collect_yolo_training_data.py -s /data -o /out --patches

    # Custom split
    python3 collect_yolo_training_data.py -s /data -o /out --split 0.8 0.1 0.1

    # Override class list (default is just "creature")
    python3 collect_yolo_training_data.py -s /data -o /out --classes creature moth beetle
"""

import json
import shutil
import random
import argparse
import time
from pathlib import Path
from collections import defaultdict

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
DEFAULT_CLASSES  = ["creature"]


# ---------------------------------------------------------------------------
# Image validity check
# ---------------------------------------------------------------------------

def is_valid_image(img_path):
    """
    Check whether an image file is readable and not corrupt/truncated.

    Uses PIL's im.load() (full pixel decode), NOT just im.verify() or
    cv2.imread(). Both of those are unreliable for this: verify() only
    checks file structure without decoding pixels, and cv2.imread() will
    silently "succeed" on a truncated JPEG — filling missing data with
    zeros and only printing a libjpeg warning rather than failing — which
    is exactly the false-negative case that slipped through originally.
    load() is the only check that reliably catches mid-scan truncation
    ("premature end of data segment").

    Falls back to a basic cv2.imread check if PIL is unavailable (less
    reliable, but better than no check at all).

    Returns True if the image is valid, False if corrupt/unreadable/empty.
    """
    p = Path(img_path)
    if not p.is_file() or p.stat().st_size == 0:
        return False

    if PIL_AVAILABLE:
        try:
            with Image.open(img_path) as im:
                im.load()
            return True
        except Exception:
            return False

    if CV2_AVAILABLE:
        try:
            img = cv2.imread(str(img_path))
            return img is not None and img.size > 0
        except Exception:
            return False

    # Neither PIL nor cv2 available — can't check, assume valid
    return True


def filter_valid_images(img_paths, max_workers=8):
    """
    Check a list of image paths for validity in parallel using a thread pool.
    PIL's im.load() releases the GIL during JPEG decoding, so threading gives
    a real speedup here despite Python's GIL (this is the same reason
    threading works well for other C-extension-heavy decode/IO workloads).

    Returns (valid_paths_set, corrupt_count).
    """
    from concurrent.futures import ThreadPoolExecutor

    valid = set()
    corrupt_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(is_valid_image, img_paths)
        for img_path, ok in zip(img_paths, results):
            if ok:
                valid.add(img_path)
            else:
                corrupt_count += 1

    return valid, corrupt_count


# ---------------------------------------------------------------------------
# Detection: find existing YOLO-format dataset roots
# ---------------------------------------------------------------------------

def find_yolo_dataset_roots(source_dir):
    """
    Walk source_dir and identify subdirectories that already contain YOLO-
    formatted data, i.e. they have both an 'images' and a 'labels' child
    directory with matching files.

    Returns a list of Path objects (the parent of images/ and labels/).
    We avoid descending into detected roots so sub-splits aren't double-counted.
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

        img_stems = {p.stem for p in candidate.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS}
        lbl_stems = {p.stem for p in labels_dir.rglob("*.txt")}
        if not (img_stems & lbl_stems):
            continue

        root = candidate.parent
        if any(str(root).startswith(str(r)) for r in yolo_root_set):
            continue
        yolo_roots.append(root)
        yolo_root_set.add(root)

    return yolo_roots


def collect_yolo_pairs_from_root(yolo_root):
    """
    From a YOLO dataset root collect all (image_path, label_path) pairs,
    flattening any train/val/test sub-splits.

    Corrupt/unreadable images are detected (in parallel) and excluded.
    """
    images_dir = yolo_root / "images"
    labels_dir = yolo_root / "labels"

    candidates = []
    for img_path in images_dir.rglob("*"):
        if img_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        rel = img_path.relative_to(images_dir)
        label_path = labels_dir / rel.with_suffix(".txt")
        if label_path.exists():
            candidates.append((img_path, label_path))

    if not candidates:
        return []

    valid_imgs, skipped_corrupt = filter_valid_images([c[0] for c in candidates])
    pairs = [(img, lbl) for img, lbl in candidates if img in valid_imgs]

    if skipped_corrupt:
        print(f"  [WARN] Skipped {skipped_corrupt} corrupt/unreadable image(s) in {yolo_root.name}/")

    return pairs


# ---------------------------------------------------------------------------
# Detection: find x-anylabeling JSON pairs
# ---------------------------------------------------------------------------

def find_anylabeling_pairs(source_dir, skip_dirs):
    """
    Recursively walk source_dir (excluding skip_dirs) for images that have
    a sibling x-anylabeling .json file.
    Empty-annotation JSONs are included as intentional background images.
    _botdetection.json files are ignored.
    Corrupt/unreadable images are detected (in parallel) and excluded.
    """
    source_dir = Path(source_dir)
    candidates = []
    skipped_no_json  = 0
    skipped_in_yolo  = 0

    for img_path in source_dir.rglob("*"):
        if img_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        # Skip files inside already-detected YOLO roots
        if any(str(img_path).startswith(str(d)) for d in skip_dirs):
            skipped_in_yolo += 1
            continue

        # Skip inference output images
        if "_botdetection" in img_path.stem:
            continue

        json_path = img_path.with_suffix(".json")
        if not json_path.exists() or "_botdetection" in json_path.stem:
            skipped_no_json += 1
            continue

        try:
            with open(json_path, "r") as f:
                json.load(f)   # validate it parses; empty shapes is fine
        except (json.JSONDecodeError, KeyError):
            print(f"  [WARN] Could not parse JSON: {json_path}")
            continue

        candidates.append((img_path, json_path))

    skipped_corrupt = 0
    pairs = candidates
    if candidates:
        valid_imgs, skipped_corrupt = filter_valid_images([c[0] for c in candidates])
        pairs = [(img, j) for img, j in candidates if img in valid_imgs]

    print(f"  Found {len(pairs)} x-anylabeling labeled pairs (includes background images)")
    print(f"  Skipped {skipped_no_json} images with no JSON")
    if skipped_in_yolo:
        print(f"  Skipped {skipped_in_yolo} images already inside YOLO folders")
    if skipped_corrupt:
        print(f"  [WARN] Skipped {skipped_corrupt} corrupt/unreadable image(s)")
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
# Conversion: x-anylabeling → YOLO OBB
# ---------------------------------------------------------------------------

def shape_to_yolo_line(shape, img_width, img_height, class_map):
    """
    Convert one x-anylabeling shape to a YOLO OBB label line.

    YOLO OBB format: class_id x1 y1 x2 y2 x3 y3 x4 y4  (normalized 0-1)

    x-anylabeling "rotation" shapes provide 4 corner points directly —
    we normalize each point and write all 8 coordinates.

    Shapes with != 4 points fall back to their axis-aligned bounding box
    corners (valid 0°-rotation OBB).
    """
    label = shape.get("label", "").strip()
    if label not in class_map:
        return None

    points = shape.get("points", [])
    if not points:
        return None

    try:
        if len(points) == 4:
            coords = []
            for px, py in points:
                coords.extend([
                    max(0.0, min(1.0, px / img_width)),
                    max(0.0, min(1.0, py / img_height)),
                ])
        else:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            x1, x2 = min(xs), max(xs)
            y1, y2 = min(ys), max(ys)
            if (x2 - x1) <= 0 or (y2 - y1) <= 0:
                return None
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
    """Convert an x-anylabeling JSON to a list of YOLO OBB label strings."""
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
# Conversion: detection format → OBB format
# ---------------------------------------------------------------------------

def detect_label_to_obb(line):
    """
    Convert a 5-value regular YOLO detection line (class cx cy w h)
    to a 9-value YOLO OBB line (class x1 y1 x2 y2 x3 y3 x4 y4)
    by expanding the box into 4 axis-aligned corners.
    No rotation information is lost because detection format has none.
    """
    parts = line.split()
    cls = parts[0]
    cx, cy, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
    hw, hh = w / 2, h / 2
    corners = [
        cx - hw, cy - hh,  # top-left
        cx + hw, cy - hh,  # top-right
        cx + hw, cy + hh,  # bottom-right
        cx - hw, cy + hh,  # bottom-left
    ]
    coords = [max(0.0, min(1.0, v)) for v in corners]
    return f"{cls} " + " ".join(f"{v:.6f}" for v in coords)


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
# Near-duplicate detection (perceptual hashing)
# ---------------------------------------------------------------------------

def get_image_path_from_pair(pair):
    """
    Pairs come in two shapes depending on source:
      x-anylabeling pairs: (img_path, json_path)
      existing YOLO pairs: (img_path, label_path)
    In both cases the image is element 0.
    """
    return pair[0]


def compute_phash(img_path, hash_size=8):
    """
    Compute a perceptual hash (pHash) for an image using OpenCV + numpy,
    avoiding a dependency on the `imagehash` package.

    Algorithm (standard pHash):
      1. Resize to (hash_size*4) x (hash_size*4), grayscale
      2. Compute 2D DCT
      3. Keep the top-left hash_size x hash_size low-frequency coefficients
      4. Threshold against the median to get a binary hash

    Returns a numpy boolean array of shape (hash_size*hash_size,), or None
    if the image can't be read, is corrupt/truncated, or any other error
    occurs while processing it. Corrupt images are never fatal — the caller
    treats a None hash as "always keep this image" so a bad JPEG just gets
    skipped from dedup rather than crashing the run.
    """
    try:
        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
        if img is None or img.size == 0:
            return None

        size = hash_size * 4
        img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA).astype(np.float32)

        dct = cv2.dct(img)
        dct_low = dct[:hash_size, :hash_size]

        median = np.median(dct_low)
        return (dct_low > median).flatten()

    except Exception:
        # Any decode error (truncated/corrupt JPEG, unreadable file, etc.)
        # — treat as un-hashable rather than letting it kill the whole run.
        return None


def hamming_distance(hash_a, hash_b):
    """Number of differing bits between two boolean hash arrays."""
    return int(np.count_nonzero(hash_a != hash_b))


def _format_eta(seconds):
    """Human-readable ETA string, e.g. '2h 4m', '3m 12s', '45s'."""
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m}m"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def compute_phashes_parallel(img_paths, hash_size=8, max_workers=8, report_every=200):
    """
    Compute perceptual hashes for a list of images in parallel, printing
    periodic progress (count, rate, ETA) since hashing thousands of
    full-resolution field photos can take several minutes.

    Like filter_valid_images, this uses a thread pool — cv2's image decode
    releases the GIL, so threading gives a real speedup despite Python's GIL.

    Returns a list of hashes (or None for unhashable images) in the same
    order as img_paths.
    """
    from concurrent.futures import ThreadPoolExecutor

    n = len(img_paths)
    hashes = [None] * n
    start = time.monotonic()
    done = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        from concurrent.futures import as_completed
        futures = {executor.submit(compute_phash, p, hash_size): i for i, p in enumerate(img_paths)}
        for future in as_completed(futures):
            idx = futures[future]
            try:
                hashes[idx] = future.result()
            except Exception:
                hashes[idx] = None
            done += 1
            if done % report_every == 0 or done == n:
                elapsed = time.monotonic() - start
                rate = done / elapsed if elapsed > 0 else 0
                remaining = n - done
                eta = remaining / rate if rate > 0 else 0
                print(f"    Hashed {done}/{n} ({rate:.0f} img/s, ETA {_format_eta(eta)})")

    return hashes


def deduplicate_pairs(pairs, source_label, threshold=5, hash_size=8, max_workers=8):
    """
    Cluster near-identical images using perceptual hashing and keep only one
    representative per cluster.

    threshold: max Hamming distance (out of hash_size^2 bits) for two images
               to be considered near-duplicates. Lower = stricter (only near-
               exact matches merge). 5 is a reasonable starting point for an
               8x8 hash (64 bits total) — catches near-identical frames from
               burst/sequence shots while leaving genuinely different scenes
               untouched.

    Clustering approach: images are compared against cluster representatives
    only (not all-pairs), so this runs in O(n * num_clusters) rather than
    O(n^2). Within a folder of mostly-similar sequential shots this stays fast.

    The single image with the LOWEST index (i.e. encountered first — typically
    alphabetical/timestamp order) is kept as the cluster representative, since
    the first image in a burst is usually as representative as any other.

    Hashing runs in parallel with periodic progress output, since this step
    can take several minutes on large datasets.

    Returns (kept_pairs, num_removed).
    """
    if not CV2_AVAILABLE:
        print(f"  [WARN] --dedupe requested but opencv-python is not installed; skipping dedup for {source_label}.")
        return pairs, 0

    if not pairs:
        return pairs, 0

    print(f"  Hashing {len(pairs)} images for dedup ({source_label})...")

    img_paths = [get_image_path_from_pair(pair) for pair in pairs]
    hashes = compute_phashes_parallel(img_paths, hash_size=hash_size, max_workers=max_workers)
    valid_pairs = pairs

    corrupt_count = sum(1 for h in hashes if h is None)
    if corrupt_count:
        print(f"  [WARN] {corrupt_count} image(s) could not be hashed (corrupt/unreadable) "
              f"and were kept unconditionally (no dedup applied to them).")

    # Cluster: compare each image against existing cluster representatives only
    cluster_reps = []       # list of (hash, kept_pair_index_in_kept_list)
    kept_pairs = []
    removed = 0

    for pair, h in zip(valid_pairs, hashes):
        if h is None:
            # Could not hash — always keep
            kept_pairs.append(pair)
            continue

        matched = False
        for rep_hash in cluster_reps:
            if hamming_distance(h, rep_hash) <= threshold:
                matched = True
                break

        if matched:
            removed += 1
        else:
            cluster_reps.append(h)
            kept_pairs.append(pair)

    if removed:
        print(f"  [DEDUPE] {source_label}: removed {removed} near-duplicate image(s), kept {len(kept_pairs)}")
    else:
        print(f"  [DEDUPE] {source_label}: no near-duplicates found ({len(kept_pairs)} images kept)")

    return kept_pairs, removed


# ---------------------------------------------------------------------------
# Copying helpers
# ---------------------------------------------------------------------------

def safe_dest_name(filename, dest_dir, parent_name):
    """Return a destination Path that doesn't collide with existing files."""
    dest = dest_dir / filename
    if dest.exists():
        dest = dest_dir / f"{parent_name}__{filename}"
    return dest


def copy_anylabeling_pair(img_path, json_path, img_out_dir, label_out_dir, class_map, counts, bg_counts):
    """Convert x-anylabeling JSON → YOLO OBB txt and copy image."""
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

    return dest_img, label_path


def copy_yolo_pair(img_path, label_path, img_out_dir, label_out_dir, counts, bg_counts):
    """
    Copy one existing YOLO pair, auto-converting any detection-format
    (5-value) lines to OBB format (9-value).
    """
    dest_img = safe_dest_name(img_path.name, img_out_dir, img_path.parent.name)
    shutil.copy2(img_path, dest_img)

    dest_lbl = label_out_dir / (dest_img.stem + ".txt")
    converted_count = 0
    out_lines = []

    try:
        with open(label_path, "r") as f:
            raw_lines = f.readlines()

        for raw in raw_lines:
            line = raw.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 5:
                line = detect_label_to_obb(line)
                converted_count += 1
            elif len(parts) == 9:
                pass  # already OBB
            else:
                print(f"  [WARN] Skipping unexpected label ({len(parts)} values): {label_path.name}")
                continue
            out_lines.append(line)
            counts[int(line.split()[0])] += 1

        if converted_count:
            print(f"  [CONV] {label_path.name}: converted {converted_count} detection→OBB labels")

    except (ValueError, IndexError) as e:
        print(f"  [WARN] Could not read label file {label_path}: {e}")

    with open(dest_lbl, "w") as f:
        f.write("\n".join(out_lines))

    if not out_lines:
        bg_counts["background"] += 1

    return dest_img, dest_lbl


# ---------------------------------------------------------------------------
# OBB patch extraction for visual audit (TIGHTLY ROTATED crops)
# ---------------------------------------------------------------------------

def crop_rotated_rect(img, rect, interpolation=cv2.INTER_LINEAR):
    """
    Crop a tightly-rotated patch from img given an OpenCV minAreaRect.

    Matches the exact technique used in detect.py's crop_rect():
      1. Rotate the WHOLE image so the box becomes axis-aligned
         (cv2.getRotationMatrix2D + cv2.warpAffine)
      2. Crop precisely to the box size, no padding
         (cv2.getRectSubPix)

    This produces a tight rotated crop — the creature fills the patch
    with no extra background corners, matching what detect.py generates
    for bot-detection thumbnails.
    """
    center, size, angle = rect[0], rect[1], rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))
    height, width = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D(center, angle, 1)
    img_rot = cv2.warpAffine(img, M, (width, height), flags=interpolation)
    img_crop = cv2.getRectSubPix(img_rot, size, center)
    return img_crop


def extract_obb_patches(img_path, label_path, patches_dir, class_names):
    """
    Crop a tightly-ROTATED patch for every OBB annotation in label_path and
    save to patches_dir, using the same cv2.minAreaRect + warpAffine technique
    as detect.py's crop_rect(), so training-data patches look consistent with
    the bot-detection thumbnails reviewers already use.

    Patch filenames are prefixed with the patch width and the source image
    stem so any suspicious crop can be traced straight back to its origin
    file, and patches can be sorted/filtered by size:
        <patch_width>_<source_stem>__<index>_<classname>.jpg

    Requires opencv-python and numpy (pip install opencv-python numpy).
    """
    if not CV2_AVAILABLE:
        return

    try:
        with open(label_path, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
    except Exception:
        return

    if not lines:
        return  # background image, nothing to crop

    img = cv2.imread(str(img_path))
    if img is None:
        print(f"  [WARN] Could not open image for patching: {img_path.name}")
        return

    img_h, img_w = img.shape[0], img.shape[1]
    stem = img_path.stem

    for idx, line in enumerate(lines):
        parts = line.split()
        if len(parts) != 9:
            continue

        class_id   = int(parts[0])
        class_name = class_names[class_id] if class_id < len(class_names) else f"class{class_id}"

        # Denormalize the 4 corner points into pixel coordinates
        coords = [float(v) for v in parts[1:]]
        pts = np.array(
            [[coords[i] * img_w, coords[i + 1] * img_h] for i in range(0, 8, 2)],
            dtype=np.float32,
        ).reshape((-1, 1, 2))

        # Same approach as detect.py: minAreaRect -> rotate -> crop
        rect = cv2.minAreaRect(pts)
        size = rect[1]
        if size[0] <= 0 or size[1] <= 0:
            continue

        try:
            patch = crop_rotated_rect(img, rect)
        except Exception as e:
            print(f"  [WARN] Could not crop patch {idx} from {img_path.name}: {e}")
            continue

        if patch is None or patch.size == 0:
            continue

        patch_w = patch.shape[1]
        patch_name = f"{patch_w}_{stem}__{idx:04d}_{class_name}.jpg"
        cv2.imwrite(str(patches_dir / patch_name), patch, [cv2.IMWRITE_JPEG_QUALITY, 90])


# ---------------------------------------------------------------------------
# Populate one split
# ---------------------------------------------------------------------------

def populate_split(split_name, anylabeling_pairs, yolo_pairs, output_dir,
                   class_map, stats, patches_dir=None, class_names=None):
    """
    Write all pairs for one split (train/val/test) to the output directory.
    If patches_dir is given, OBB crops are saved there for visual audit.
    """
    img_out_dir   = Path(output_dir) / "images" / split_name
    label_out_dir = Path(output_dir) / "labels" / split_name
    img_out_dir.mkdir(parents=True, exist_ok=True)
    label_out_dir.mkdir(parents=True, exist_ok=True)

    counts    = defaultdict(int)
    bg_counts = defaultdict(int)

    for img_path, json_path in anylabeling_pairs:
        dest_img, dest_lbl = copy_anylabeling_pair(
            img_path, json_path, img_out_dir, label_out_dir, class_map, counts, bg_counts
        )
        if patches_dir is not None:
            extract_obb_patches(dest_img, dest_lbl, patches_dir, class_names or [])

    for img_path, label_path in yolo_pairs:
        dest_img, dest_lbl = copy_yolo_pair(
            img_path, label_path, img_out_dir, label_out_dir, counts, bg_counts
        )
        if patches_dir is not None:
            extract_obb_patches(dest_img, dest_lbl, patches_dir, class_names or [])

    stats[split_name] = {"annotations": dict(counts), "background": bg_counts["background"]}


# ---------------------------------------------------------------------------
# data.yaml
# ---------------------------------------------------------------------------

def write_data_yaml(output_dir, class_names, has_test):
    """
    Write data.yaml manually to guarantee correct YOLO OBB formatting.
    pyyaml with integer-keyed dicts produces malformed indentation, so we
    build the file as a plain string.
    """
    output_dir = Path(output_dir)
    lines = [
        f"path: {output_dir.resolve()}",
        "train: images/train",
        "val: images/val",
    ]
    if has_test:
        lines.append("test: images/test")
    lines.append(f"nc: {len(class_names)}")
    lines.append("names:")
    for i, name in enumerate(class_names):
        lines.append(f"  {i}: {name}")

    yaml_path = output_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nWrote data.yaml → {yaml_path}")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_summary(output_dir, class_names, stats, yolo_roots, n_anylabeling,
                  patches_dir, source_dirs):
    print("\n" + "=" * 55)
    print("DATASET COLLECTION SUMMARY")
    print("=" * 55)

    print(f"\nSource directories searched ({len(source_dirs)}):")
    for sd in source_dirs:
        print(f"  {sd}")

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
    if patches_dir and Path(patches_dir).exists():
        n_patches = len(list(Path(patches_dir).glob("*.jpg")))
        print(f"Patches: {patches_dir}")
        print(f"         {n_patches} crops saved — review before training to spot false positives!")
    print("=" * 55)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Collect x-anylabeling ground truth data AND existing YOLO datasets "
            "from one or more source directories, merge them, and output a single "
            "YOLO OBB dataset."
        )
    )
    parser.add_argument(
        "--source", "-s",
        required=True,
        action="append",       # ← each -s/--source adds to a list
        dest="sources",
        metavar="DIR",
        help=(
            "Directory to search (searched recursively). "
            "Repeat this flag for multiple source folders: "
            "-s /path/one -s /path/two -s /path/three"
        ),
    )
    parser.add_argument("--output", "-o", required=True,
        help="Output directory for the merged YOLO dataset")
    parser.add_argument("--split", nargs=3, type=float, default=[0.8, 0.1, 0.1],
        metavar=("TRAIN", "VAL", "TEST"),
        help="Train/val/test ratios (must sum to 1.0). Default: 0.8 0.1 0.1")
    parser.add_argument("--seed", type=int, default=42,
        help="Random seed for reproducible splits (default: 42)")
    parser.add_argument("--classes", nargs="+", default=None,
        help=(
            f"Class names in order. Default: {DEFAULT_CLASSES}. "
            "Example: --classes creature moth beetle"
        ))
    parser.add_argument("--patches", action="store_true", default=False,
        help=(
            "Export a tightly-ROTATED cropped patch image for every OBB "
            "annotation to <output>/patches/ for visual false-positive "
            "auditing. Patches are named "
            "<patch_width>_<source_stem>__<index>_<class>.jpg so any "
            "suspicious crop can be traced back to its source image and "
            "sorted/filtered by size. Uses the same cv2.minAreaRect + "
            "warpAffine technique as detect.py. "
            "Requires opencv-python and numpy (pip install opencv-python numpy)."
        ))
    parser.add_argument("--dedupe", action="store_true", default=False,
        help=(
            "Remove near-duplicate images using perceptual hashing before "
            "splitting into train/val/test. Useful when a source folder "
            "contains burst/sequence shots of the same creature in nearly "
            "the same position — keeping all of them both wastes training "
            "time and risks leaking near-identical images across the "
            "train/val split, which inflates validation metrics. "
            "Deduplication runs separately per source-and-type group (each "
            "x-anylabeling source folder, each YOLO root) so unrelated "
            "folders are never compared against each other. "
            "Requires opencv-python and numpy."
        ))
    parser.add_argument("--dedupe-threshold", type=int, default=5,
        help=(
            "Max perceptual-hash Hamming distance (0-64) for two images to "
            "be considered near-duplicates when --dedupe is set. Lower = "
            "stricter (only near-exact frames merge). Default: 5."
        ))
    args = parser.parse_args()

    train_r, val_r, test_r = args.split
    if abs(train_r + val_r + test_r - 1.0) > 1e-6:
        raise ValueError(f"Split ratios must sum to 1.0, got {train_r + val_r + test_r:.4f}")

    # Resolve and validate all source directories
    source_dirs = []
    for raw in args.sources:
        p = Path(raw)
        if not p.is_dir():
            raise ValueError(f"Source directory does not exist or is not a directory: {p}")
        source_dirs.append(p.resolve())

    # Deduplicate in case the user accidentally repeats a path
    seen = set()
    unique_source_dirs = []
    for p in source_dirs:
        if p not in seen:
            seen.add(p)
            unique_source_dirs.append(p)
    source_dirs = unique_source_dirs

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Detect existing YOLO dataset roots across ALL source directories
    # ------------------------------------------------------------------
    print(f"\n[1/5] Scanning for existing YOLO-format folders across {len(source_dirs)} source(s)...")
    all_yolo_roots = []
    for sd in source_dirs:
        print(f"  Searching: {sd}")
        roots = find_yolo_dataset_roots(sd)
        print(f"    Found {len(roots)} YOLO dataset root(s)")
        for r in roots:
            print(f"      {r}")
        all_yolo_roots.extend(roots)

    all_yolo_pairs = []
    for root in all_yolo_roots:
        pairs = collect_yolo_pairs_from_root(root)
        print(f"  → {len(pairs)} labeled pairs from {root.name}/")
        all_yolo_pairs.extend(pairs)

    # ------------------------------------------------------------------
    # 2. Find x-anylabeling pairs across ALL source directories
    # ------------------------------------------------------------------
    print(f"\n[2/5] Scanning for x-anylabeling JSON pairs across {len(source_dirs)} source(s)...")
    skip_dirs = set(all_yolo_roots)
    all_anylabeling_pairs = []
    for sd in source_dirs:
        print(f"  Searching: {sd}")
        pairs = find_anylabeling_pairs(sd, skip_dirs)
        all_anylabeling_pairs.extend(pairs)

    print(f"  Total x-anylabeling pairs across all sources: {len(all_anylabeling_pairs)}")

    # ------------------------------------------------------------------
    # 3. Resolve class names
    # ------------------------------------------------------------------
    print(f"\n[3/5] Resolving class names...")
    if args.classes:
        class_names = args.classes
        print(f"  Using manually specified classes: {class_names}")
    elif all_anylabeling_pairs:
        class_names = collect_class_names_from_json(all_anylabeling_pairs)
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
    # 3.5. Optional deduplication (per source group, BEFORE splitting)
    # ------------------------------------------------------------------
    if args.dedupe:
        print(f"\n[3.5/5] Deduplicating near-identical images (threshold={args.dedupe_threshold})...")
        print("  Note: dedup runs separately per source group so unrelated")
        print("        folders/datasets are never compared against each other.")

        total_removed = 0

        # Dedup YOLO pairs per-root (each pre-existing YOLO dataset is its own group)
        deduped_yolo_pairs = []
        pairs_by_root = defaultdict(list)
        for img_path, label_path in all_yolo_pairs:
            # Find which root this pair came from by matching the label_path prefix
            for root in all_yolo_roots:
                if str(label_path).startswith(str(root)):
                    pairs_by_root[root].append((img_path, label_path))
                    break
        for root, pairs in pairs_by_root.items():
            kept, removed = deduplicate_pairs(pairs, f"YOLO root: {root.name}", threshold=args.dedupe_threshold)
            deduped_yolo_pairs.extend(kept)
            total_removed += removed
        all_yolo_pairs = deduped_yolo_pairs

        # Dedup x-anylabeling pairs per top-level source directory
        deduped_anylabeling_pairs = []
        pairs_by_source = defaultdict(list)
        for img_path, json_path in all_anylabeling_pairs:
            for sd in source_dirs:
                if str(img_path).startswith(str(sd)):
                    pairs_by_source[sd].append((img_path, json_path))
                    break
        for sd, pairs in pairs_by_source.items():
            kept, removed = deduplicate_pairs(pairs, f"source: {sd.name}", threshold=args.dedupe_threshold)
            deduped_anylabeling_pairs.extend(kept)
            total_removed += removed
        all_anylabeling_pairs = deduped_anylabeling_pairs

        print(f"\n  Total removed across all groups: {total_removed}")
        print(f"  Remaining: {len(all_anylabeling_pairs) + len(all_yolo_pairs)} images")

    # ------------------------------------------------------------------
    # 4. Split, copy, and optionally extract patches
    # ------------------------------------------------------------------
    print(f"\n[4/5] Splitting and copying files...")

    al_train, al_val, al_test = split_items(all_anylabeling_pairs, train_r, val_r, test_r, args.seed)
    yl_train, yl_val, yl_test = split_items(all_yolo_pairs,        train_r, val_r, test_r, args.seed)

    total = len(all_anylabeling_pairs) + len(all_yolo_pairs)
    print(f"  Total images: {total}")
    print(f"    train: {len(al_train) + len(yl_train)}")
    print(f"    val:   {len(al_val)   + len(yl_val)}")
    print(f"    test:  {len(al_test)  + len(yl_test)}")

    patches_dir = None
    if args.patches:
        if not CV2_AVAILABLE:
            print("\n  [WARN] --patches requested but opencv-python is not installed.")
            print("         Run: pip3 install opencv-python numpy")
        else:
            patches_dir = output_dir / "patches"
            patches_dir.mkdir(parents=True, exist_ok=True)
            print(f"\n  Patch crops will be saved to: {patches_dir}")

    stats = {}
    populate_split("train", al_train, yl_train, output_dir, class_map, stats, patches_dir, class_names)
    populate_split("val",   al_val,   yl_val,   output_dir, class_map, stats, patches_dir, class_names)
    if al_test or yl_test:
        populate_split("test", al_test, yl_test, output_dir, class_map, stats, patches_dir, class_names)

    # ------------------------------------------------------------------
    # 5. Write data.yaml
    # ------------------------------------------------------------------
    print(f"\n[5/5] Writing data.yaml...")
    write_data_yaml(output_dir, class_names, has_test=bool(al_test or yl_test))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print_summary(output_dir, class_names, stats, all_yolo_roots,
                  len(all_anylabeling_pairs), patches_dir, source_dirs)


if __name__ == "__main__":
    main()