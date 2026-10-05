#!/usr/bin/env python3
"""
Split a YOLO OBB training dataset into several smaller zip files for Zenodo.

Every zip keeps the dataset's folder structure, so unzipping all of them into
the same folder rebuilds the original dataset:

    data.yaml              (written next to the zips as a plain file)
    images/{train,val,test}/...
    labels/{train,val,test}/...
    patches/...            (optional)

Each image is zipped together with its own label file, so every "part" zip
is self-contained. Large splits (train) are broken into multiple parts no
bigger than --max-gb each.

Zips are written as STORED (no compression) because JPEGs don't compress
further, so this is fast and is limited only by disk speed.

Skipped: .DS_Store files and YOLO *.cache files.
data.yaml is rewritten with `path: .` so it works on other people's machines.

Resumable: each zip is written to a .partial file and renamed when complete;
re-running skips zips that already exist.

Usage:
    python3 make_zenodo_zips.py /path/to/dataset
    python3 make_zenodo_zips.py /path/to/dataset --out /path/to/out --max-gb 4
    python3 make_zenodo_zips.py /path/to/dataset --dry-run
"""

import argparse
import os
import re
import sys
import time
import zipfile
from pathlib import Path

SPLITS = ["train", "val", "test"]
SKIP_NAMES = {".DS_Store"}


def human(nbytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if nbytes < 1024 or unit == "TB":
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024


def skip(path):
    return path.name in SKIP_NAMES or path.suffix == ".cache" or path.name.startswith("._")


def split_items(root, split):
    """Return a sorted list of (image, label_or_None) pairs for one split."""
    img_dir = root / "images" / split
    lbl_dir = root / "labels" / split
    if not img_dir.is_dir():
        return []
    items = []
    for img in sorted(img_dir.iterdir()):
        if not img.is_file() or skip(img):
            continue
        lbl = lbl_dir / (img.stem + ".txt")
        items.append((img, lbl if lbl.is_file() else None))
    return items


def chunk(items, max_bytes):
    """Group (image, label) pairs into chunks of at most max_bytes."""
    chunks, current, size = [], [], 0
    for img, lbl in items:
        item_size = img.stat().st_size + (lbl.stat().st_size if lbl else 0)
        if current and size + item_size > max_bytes:
            chunks.append(current)
            current, size = [], 0
        current.append((img, lbl))
        size += item_size
    if current:
        chunks.append(current)
    return chunks


def portable_yaml(root):
    text = (root / "data.yaml").read_text()
    return re.sub(r"(?m)^path:.*$", "path: .", text)


def write_zip(zip_path, files, root, extra_text=None):
    """
    files: list of Paths under root. extra_text: dict of arcname -> str.
    Writes to <zip>.partial then renames, so an interrupted run is redone.
    """
    if zip_path.exists():
        print(f"  [SKIP] {zip_path.name} already exists")
        return
    partial = zip_path.with_name(zip_path.name + ".partial")
    total = sum(f.stat().st_size for f in files)
    done, start, last = 0, time.time(), 0.0
    with zipfile.ZipFile(partial, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as zf:
        for arcname, text in (extra_text or {}).items():
            zf.writestr(arcname, text)
        for i, f in enumerate(files, 1):
            zf.write(f, f.relative_to(root).as_posix())
            done += f.stat().st_size
            now = time.time()
            if now - last > 2 or i == len(files):
                last = now
                elapsed = now - start
                rate = done / elapsed if elapsed > 0 else 0
                eta = (total - done) / rate if rate > 0 else 0
                pct = 100 * done / total if total else 100
                sys.stdout.write(
                    f"\r  {zip_path.name}: {pct:5.1f}%  {human(done)} / {human(total)}"
                    f"  ETA {int(eta // 60)}m{int(eta % 60):02d}s   "
                )
                sys.stdout.flush()
    print()
    partial.rename(zip_path)
    print(f"  [DONE] {zip_path.name} ({human(zip_path.stat().st_size)})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dataset", type=Path, help="Dataset root (contains data.yaml, images/, labels/)")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output folder (default: <dataset>_zenodo next to the dataset)")
    ap.add_argument("--max-gb", type=float, default=4.0,
                    help="Maximum size of each zip in GB (default: 4)")
    ap.add_argument("--prefix", default="Mothbox_Training_Dataset_1-1",
                    help="Filename prefix for the zips")
    ap.add_argument("--no-patches", action="store_true", help="Don't make a patches zip")
    ap.add_argument("--dry-run", action="store_true", help="Show the plan without writing anything")
    args = ap.parse_args()

    root = args.dataset.resolve()
    if not (root / "data.yaml").is_file():
        sys.exit(f"No data.yaml in {root}; is this the dataset root?")
    out = (args.out or root.with_name(root.name + "_zenodo")).resolve()
    if out == root or root in out.parents:
        sys.exit("Output folder must be outside the dataset folder.")
    max_bytes = int(args.max_gb * 1024**3)

    # Build the plan: (zip filename, files, extra_text)
    plan = []
    missing_labels = 0
    for split in SPLITS:
        items = split_items(root, split)
        missing_labels += sum(1 for _, lbl in items if lbl is None)
        parts = chunk(items, max_bytes)
        for n, part in enumerate(parts, 1):
            suffix = f"_part{n:02d}of{len(parts):02d}" if len(parts) > 1 else ""
            files = [f for img, lbl in part for f in (img, lbl) if f]
            plan.append((f"{args.prefix}_{split}{suffix}.zip", files, None))

    patches_dir = root / "patches"
    if patches_dir.is_dir() and not args.no_patches:
        patches = sorted(p for p in patches_dir.iterdir() if p.is_file() and not skip(p))
        plan.append((f"{args.prefix}_patches.zip", patches, None))

    print(f"Dataset: {root}")
    print(f"Output:  {out}")
    if missing_labels:
        print(f"[WARN] {missing_labels} image(s) have no label file (zipped anyway)")
    grand = 0
    for name, files, _ in plan:
        size = sum(f.stat().st_size for f in files)
        grand += size
        print(f"  {name:60s} {len(files):6d} files  {human(size):>10s}")
    print(f"  {'data.yaml':60s} {'(plain file, path: .)':>27s}")
    print(f"  {'TOTAL':60s} {sum(len(f) for _, f, _ in plan):6d} files  {human(grand):>10s}")

    if args.dry_run:
        print("\nDry run; nothing written.")
        return

    out.mkdir(parents=True, exist_ok=True)
    free = os.statvfs(out).f_bavail * os.statvfs(out).f_frsize
    if free < grand * 1.02:
        sys.exit(f"Not enough free space at {out}: need ~{human(grand)}, have {human(free)}")

    (out / "data.yaml").write_text(portable_yaml(root))
    print("\n  [DONE] data.yaml (path rewritten to '.'; upload it as its own file)")
    for name, files, extra in plan:
        write_zip(out / name, files, root, extra)
    print(f"\nAll zips written to {out}")
    print("Unzip them all into one folder to rebuild the dataset.")


if __name__ == "__main__":
    main()
