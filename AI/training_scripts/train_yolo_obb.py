"""
train_yolo_obb.py

Trains a YOLO26 OBB (Oriented Bounding Box) model on a dataset prepared by
collect_yolo_training_data.py.

YOLO26 improvements relevant to Mothbox data:
  - STAL: Small-Target-Aware Label Assignment — guarantees tiny objects
    (like 26px creatures) always get positive label assignments during training
  - Refined OBB decoding: specialized angle loss, better than YOLO11 for rotation
  - NMS-free inference: faster and simpler deployment
  - +3.4 mAP over YOLO11 on oriented detection benchmarks

Device priority (auto-detected):
  1. NVIDIA GPU with CUDA  — fastest, ideal for local PC training
  2. Apple Silicon MPS     — fast on M1/M2/M3/M4 Macs
  3. CPU                   — slow but universally works
  4. Cloud / multi-GPU     — enabled via --device flag (e.g. "0,1" or "cuda:0")

Requirements:
    pip install ultralytics

Usage examples:
    # Auto-detect best device, use defaults
    python3 train_yolo_obb.py --data /path/to/yolo_dataset/data.yaml
python3 train_yolo_obb.py --data /Users/automeris/Desktop/2026_MOTHBOTYOLO/data.yaml
    # Specify model size (n=nano, s=small, m=medium, l=large, x=xlarge)
    python3 train_yolo_obb.py --data /path/to/data.yaml --model m

    # Override epochs and image size
    python3 train_yolo_obb.py --data /path/to/data.yaml --epochs 200 --imgsz 1600

    # Resume interrupted training
    python3 train_yolo_obb.py --data /path/to/data.yaml --resume

    # Force a specific device (cloud / multi-GPU)
    python3 train_yolo_obb.py --data /path/to/data.yaml --device 0,1
"""

import argparse
import shutil
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Device detection
# ---------------------------------------------------------------------------

def detect_device():
    """
    Return the best available device string for YOLO training.
    Priority: CUDA > MPS > CPU
    """
    try:
        import torch
    except ImportError:
        print("[WARN] PyTorch not found — falling back to CPU.")
        print("       Install PyTorch from https://pytorch.org/get-started/locally/")
        return "cpu"

    if torch.cuda.is_available():
        n = torch.cuda.device_count()
        name = torch.cuda.get_device_name(0)
        print(f"[INFO] CUDA detected — {n} GPU(s) available")
        print(f"       Using: {name}")
        return "0" if n == 1 else ",".join(str(i) for i in range(n))

    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        print("[INFO] Apple Silicon MPS detected")
        return "mps"

    print("[INFO] No GPU detected — using CPU (training will be slow)")
    print("       Consider reducing --imgsz and --batch for faster iteration")
    return "cpu"


# ---------------------------------------------------------------------------
# Dataset integrity scan
# ---------------------------------------------------------------------------

def scan_dataset_for_corrupt_images(data_yaml: Path) -> int:
    """
    Decode every image using cv2 (the same loader YOLO uses internally).
    Libjpeg writes "Corrupt JPEG data" warnings directly to C-level stderr,
    not Python exceptions — so we redirect fd 2 to a temp file per image to
    catch them. PIL misses these because it tolerates truncated scans that
    libjpeg only warns about.
    Corrupt images and their paired label files are moved to a quarantine
    folder. Returns the number moved.
    """
    import os
    import tempfile
    import yaml

    try:
        import cv2
    except ImportError:
        print("[WARN] opencv-python (cv2) not found — skipping corruption scan.")
        return 0

    with open(data_yaml) as f:
        cfg = yaml.safe_load(f)

    dataset_root = data_yaml.parent
    if "path" in cfg:
        dataset_root = Path(cfg["path"])

    splits = {k: cfg[k] for k in ("train", "val", "test") if k in cfg}
    if not splits:
        print("[WARN] No train/val/test splits found in data.yaml — skipping scan.")
        return 0

    image_paths = []
    for split_path in splits.values():
        img_dir = dataset_root / split_path
        if img_dir.is_dir():
            for ext in ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"):
                image_paths.extend(img_dir.glob(ext))
        else:
            print(f"[WARN] Image directory not found: {img_dir}")

    if not image_paths:
        print("[INFO] No images found to scan.")
        return 0

    print(f"\n[INFO] Pre-scanning {len(image_paths)} images for corruption "
          f"(using cv2 + libjpeg stderr capture)...")

    # Reuse a single temp file; redirect C-level stderr into it per image
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".txt")
    os.close(tmp_fd)

    corrupt = []
    try:
        for i, path in enumerate(image_paths, 1):
            if i % 200 == 0 or i == len(image_paths):
                print(f"  Scanned {i}/{len(image_paths)}...{' ' * 10}", end="\r")

            # Truncate the capture file
            cap_fd = os.open(tmp_path, os.O_WRONLY | os.O_TRUNC)
            old_stderr = os.dup(2)
            os.dup2(cap_fd, 2)
            os.close(cap_fd)

            try:
                img = cv2.imread(str(path))
            finally:
                sys.stdout.flush()
                os.dup2(old_stderr, 2)
                os.close(old_stderr)

            with open(tmp_path) as f:
                stderr_out = f.read().strip()

            if img is None:
                corrupt.append((path, "cv2 failed to decode (returned None)"))
            elif stderr_out:
                corrupt.append((path, stderr_out[:120]))
    finally:
        os.unlink(tmp_path)

    print(f"  Scanned {len(image_paths)} images.{' ' * 30}")

    if not corrupt:
        print("[INFO] All images OK — dataset looks clean.")
        return 0

    quarantine_dir = dataset_root / "quarantine"
    quarantine_dir.mkdir(exist_ok=True)
    print(f"\n[WARN] Found {len(corrupt)} corrupt image(s). Moving to: {quarantine_dir}")

    for img_path, reason in corrupt:
        shutil.move(str(img_path), str(quarantine_dir / img_path.name))

        # Labels mirror the images/ directory structure
        label_path = Path(str(img_path).replace("/images/", "/labels/")).with_suffix(".txt")
        if label_path.exists():
            shutil.move(str(label_path), str(quarantine_dir / label_path.name))

        print(f"  Quarantined: {img_path.name}  — {reason[:100]}")

    print(f"\n[INFO] {len(corrupt)} file(s) quarantined. Training will skip them.")
    print(f"       To restore, move files back from: {quarantine_dir}")
    return len(corrupt)


# ---------------------------------------------------------------------------
# Sensible defaults per device
# ---------------------------------------------------------------------------

def device_defaults(device: str) -> dict:
    """
    Conservative starting-point batch sizes per device type.
    Tune upward if your machine handles it without OOM errors.
    Note: at imgsz=1600 these are intentionally conservative.
    """
    if device == "cpu":
        return {"batch": 2, "workers": 2}
    elif device == "mps":
        return {"batch": 4, "workers": 4}
    else:
        # CUDA — 1600px images are large; start at 8 and increase if VRAM allows
        return {"batch": 8, "workers": 8}


# ---------------------------------------------------------------------------
# Model selection
# ---------------------------------------------------------------------------

YOLO26_OBB_MODELS = {
    "n": "yolo26n-obb.pt",   # nano   — 6 MB,  61.3 mAP — fastest, good for quick tests
    "s": "yolo26s-obb.pt",   # small  — 21 MB, 64.5 mAP — good balance, recommended start
    "m": "yolo26m-obb.pt",   # medium — 46 MB, 66.8 mAP — recommended for final training
    "l": "yolo26l-obb.pt",   # large  — 55 MB, 67.0 mAP — better accuracy, more VRAM
    "x": "yolo26x-obb.pt",   # xlarge — 121 MB,67.3 mAP — best accuracy, most demanding
}


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def run_training(args):
    try:
        from ultralytics import YOLO
    except ImportError:
        print("\n[ERROR] ultralytics is not installed.")
        print("        Run:  pip3 install ultralytics")
        sys.exit(1)

    data_yaml = Path(args.data).resolve()
    if not data_yaml.exists():
        print(f"\n[ERROR] data.yaml not found: {data_yaml}")
        print("        Run collect_yolo_training_data.py first to build your dataset.")
        sys.exit(1)

    # Corruption scan
    if not args.skip_scan:
        scan_dataset_for_corrupt_images(data_yaml)
    else:
        print("[INFO] Skipping image corruption scan (--skip-scan).")

    # Device
    device = args.device if args.device else detect_device()

    # Batch / workers defaults (overridden by explicit args)
    defaults = device_defaults(device)
    batch   = args.batch   if args.batch   is not None else defaults["batch"]
    workers = args.workers if args.workers is not None else defaults["workers"]

    # Model
    if args.resume:
        model_path = args.resume if isinstance(args.resume, str) and args.resume is not True \
                     else "runs/obb/train/weights/last.pt"
        print(f"\n[INFO] Resuming training from: {model_path}")
        model = YOLO(model_path)
        model_label = f"resumed ({model_path})"
    else:
        model_file = YOLO26_OBB_MODELS.get(args.model)
        if not model_file:
            print(f"\n[ERROR] Unknown model size '{args.model}'. Choose from: {list(YOLO26_OBB_MODELS.keys())}")
            sys.exit(1)
        print(f"\n[INFO] Loading pretrained YOLO26 OBB model: {model_file}")
        print("       (Weights download automatically on first use)")
        model = YOLO(model_file)
        model_label = f"{args.model.upper()} — {model_file}"

    # Print training config
    print("\n" + "=" * 60)
    print("YOLO26 OBB TRAINING CONFIGURATION")
    print("=" * 60)
    print(f"  data.yaml  : {data_yaml}")
    print(f"  model      : {model_label}")
    print(f"  device     : {device}")
    print(f"  epochs     : {args.epochs}")
    print(f"  image size : {args.imgsz}px")
    print(f"  batch size : {batch}")
    print(f"  workers    : {workers}")
    print(f"  patience   : {args.patience} epochs (early stopping)")
    print(f"  project    : {args.project}")
    print(f"  run name   : {args.name}")
    print(f"\n  Scale range note: YOLO26's STAL label assignment helps ensure")
    print(f"  small creatures (~26px) receive positive label coverage during")
    print(f"  training alongside large ones (1500px+).")
    print("=" * 60 + "\n")

    start = time.time()

    results = model.train(
        data        = str(data_yaml),
        epochs      = args.epochs,
        imgsz       = args.imgsz,
        batch       = batch,
        device      = device,
        workers     = workers,
        project     = args.project,
        name        = args.name,
        patience    = args.patience,
        save        = True,
        save_period = args.save_period,
        plots       = True,
        verbose     = True,

        # --- Augmentation tuned for Mothbox field photography ---
        # Full rotation: moths appear at any angle on the sheet
        degrees     = 180,
        # Aggressive scale augmentation: simulates both 26px and 1500px
        # creatures appearing at different zoom levels in the same training batch
        scale       = 0.9,
        # Flips: creatures appear upside-down and mirrored
        flipud      = 0.5,
        fliplr      = 0.5,
        # Colour/lighting variation: field photography has variable lighting
        hsv_h       = 0.015,
        hsv_s       = 0.7,
        hsv_v       = 0.4,
        # Mosaic combines 4 images — exposes the model to more scale combinations
        mosaic      = 1.0,
        translate   = 0.1,
    )

    elapsed = time.time() - start
    hours, rem = divmod(int(elapsed), 3600)
    mins, secs = divmod(rem, 60)

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"  Time elapsed : {hours}h {mins}m {secs}s")

    save_dir = Path(results.save_dir) if hasattr(results, "save_dir") else \
               Path(args.project) / args.name
    best_weights = save_dir / "weights" / "best.pt"
    last_weights = save_dir / "weights" / "last.pt"

    print(f"  Results saved: {save_dir}")
    print(f"  Best weights : {best_weights}")
    print(f"  Last weights : {last_weights}")

    # --- ONNX export ---
    if not args.no_export:
        print("\n[INFO] Exporting best.pt to ONNX...")
        try:
            export_model = YOLO(str(best_weights))
            onnx_path = export_model.export(
                format = "onnx",
                imgsz  = args.imgsz,
                # half=True would give FP16 ONNX (smaller/faster) but requires CUDA;
                # keeping FP32 here for maximum compatibility across platforms.
            )
            print(f"  ONNX model  : {onnx_path}")
        except Exception as e:
            print(f"  [WARN] ONNX export failed: {e}")
            print("         You can export manually later with:")
            print(f"         from ultralytics import YOLO")
            print(f"         YOLO('{best_weights}').export(format='onnx', imgsz={args.imgsz})")
    else:
        print("\n[INFO] Skipping ONNX export (--no-export flag set).")

    print("\nTo run inference with your trained model:")
    print(f"  from ultralytics import YOLO")
    print(f"  model = YOLO('{best_weights}')        # PyTorch")
    print(f"  model = YOLO('{best_weights.with_suffix('.onnx')}')  # ONNX")
    print(f"  results = model('your_image.jpg')")
    print("=" * 60)

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Train a YOLO26 OBB model on a Mothbox creature dataset.\n"
            "YOLO26 includes STAL (Small-Target-Aware Label Assignment) which\n"
            "specifically helps with the extreme scale variation in Mothbox images."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Required
    parser.add_argument(
        "--data", "-d", required=True,
        help="Path to data.yaml produced by collect_yolo_training_data.py"
    )

    # Model
    parser.add_argument(
        "--model", "-m", default="s",
        choices=list(YOLO26_OBB_MODELS.keys()),
        help=(
            "YOLO26 OBB model size. "
            "n=nano (6MB, fastest), s=small (21MB, recommended start), "
            "m=medium (46MB, recommended final), l=large, x=xlarge. "
            "Default: s"
        )
    )

    # Training hyperparameters
    parser.add_argument(
        "--epochs", "-e", type=int, default=100,
        help="Number of training epochs. 100 is a solid default; 150-200 for final runs."
    )
    parser.add_argument(
        "--imgsz", type=int, default=1600,
        help=(
            "Input image size (square, pixels). Default: 1600. "
            "Large imgsz preserves detail for small creatures. "
            "Reduce to 1280 or 960 if you run out of VRAM or RAM."
        )
    )
    parser.add_argument(
        "--batch", type=int, default=None,
        help=(
            "Batch size. Auto-set per device if not specified "
            "(2 for CPU, 4 for MPS, 8 for CUDA at imgsz=1600). "
            "Use -1 for AutoBatch (CUDA only)."
        )
    )
    parser.add_argument(
        "--patience", type=int, default=50,
        help="Early stopping: stop if no improvement for this many epochs."
    )
    parser.add_argument(
        "--save-period", type=int, default=10, dest="save_period",
        help="Save a checkpoint every N epochs (in addition to best and last)."
    )

    # Device
    parser.add_argument(
        "--device", type=str, default=None,
        help=(
            "Device override. Auto-detected if not set. "
            "Examples: '0' (first GPU), '0,1' (multi-GPU), 'cpu', 'mps'. "
            "Cloud users: specify GPU index(es) here."
        )
    )
    parser.add_argument(
        "--workers", type=int, default=None,
        help="DataLoader worker threads. Auto-set per device if not specified."
    )

    # Output
    parser.add_argument(
        "--project", type=str, default="runs/obb",
        help="Parent directory for training run output."
    )
    parser.add_argument(
        "--name", type=str, default="train",
        help="Name for this run (subfolder inside --project)."
    )

    # Resume
    parser.add_argument(
        "--resume", nargs="?", const=True, default=False,
        metavar="CHECKPOINT",
        help=(
            "Resume training. Without a path, resumes from "
            "runs/obb/train/weights/last.pt. "
            "Pass an explicit .pt path to resume from a specific checkpoint."
        )
    )

    # Scan
    parser.add_argument(
        "--skip-scan", action="store_true", dest="skip_scan",
        help=(
            "Skip the pre-training corruption scan. "
            "Use if your dataset is known-clean and you want to start immediately."
        )
    )

    # Export
    parser.add_argument(
        "--no-export", action="store_true", dest="no_export",
        help=(
            "Skip automatic ONNX export after training. "
            "By default the best.pt weights are exported to ONNX automatically."
        )
    )

    args = parser.parse_args()
    run_training(args)


if __name__ == "__main__":
    main()