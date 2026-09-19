"""
train_yolo_obb.py

Trains a YOLO26 OBB (Oriented Bounding Box) model on a dataset prepared by
collect_yolo_training_data.py.

YOLO26 improvements relevant to Mothbox data:
  - STAL: Small-Target-Aware Label Assignment — guarantees tiny objects
    (like 20px creatures) always get positive label assignments during training
  - Refined OBB decoding: specialized angle loss, better than YOLO11 for rotation
  - NMS-free inference: faster and simpler deployment

Device priority (auto-detected):
  1. NVIDIA GPU with CUDA  — fastest, ideal for local PC training
  2. Apple Silicon MPS     — fast on M1/M2/M3/M4 Macs
  3. CPU                   — slow but universally works
  4. Cloud / multi-GPU     — enabled via --device flag (e.g. "0,1" or "cuda:0")

Requirements:
    pip install ultralytics

RESUME vs WEIGHTS — important distinction:
    --resume  : continues an interrupted run. Epoch counter, learning-rate
                schedule, optimizer momentum and EMA all carry over.
                Ultralytics restores hyperparameters from the checkpoint, so
                flags like --batch/--epochs/--imgsz are IGNORED when resuming.
    --weights : starts a brand-new run whose weights are initialised from a
                previous model. Epoch counter restarts at 1 and the LR
                schedule restarts from lr0. Use this to fine-tune on new data.

Usage examples:
    # Fresh training run
    python3 train_yolo_obb.py --data /path/to/yolo_dataset/data.yaml

    # Specify model size (n=nano, s=small, m=medium, l=large, x=xlarge)
    python3 train_yolo_obb.py --data /path/to/data.yaml --model m

    # List all available checkpoints and exit (no training)
    python3 train_yolo_obb.py --data /path/to/data.yaml --list-runs

    # TRUE resume — auto-detects the MOST RECENT run's last.pt
    python3 train_yolo_obb.py --data /path/to/data.yaml --resume

    # TRUE resume from a specific checkpoint
    python3 train_yolo_obb.py --data /path/to/data.yaml \
        --resume runs/obb/train-5/weights/last.pt

    # Start a NEW run but initialise weights from a previous model
    python3 train_yolo_obb.py --data /path/to/data.yaml \
        --weights runs/obb/train-5/weights/best.pt
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
# Checkpoint discovery
# ---------------------------------------------------------------------------

def read_checkpoint_epoch(ckpt_path):
    """
    Read the stored epoch number from a checkpoint without fully loading
    the model. Returns a human-readable string, or "?" on any failure.

    Ultralytics stores 'epoch' as the last completed epoch index (0-based),
    and sets it to -1 in a finished run's checkpoint.
    """
    try:
        import torch
        ck = torch.load(str(ckpt_path), map_location="cpu", weights_only=False)
        ep = ck.get("epoch", None)
        targs = ck.get("train_args", {}) or {}
        total = targs.get("epochs", None)
        if ep is None:
            return "?"
        if ep == -1:
            return f"COMPLETED ({total} epochs)" if total else "COMPLETED"
        return f"epoch {ep + 1}/{total}" if total else f"epoch {ep + 1}"
    except Exception:
        return "?"


def find_checkpoints(project_dir):
    """
    Find every last.pt under <project>/*/weights/, newest first.
    Returns a list of (checkpoint_path, mtime, epoch_info) tuples.
    """
    project = Path(project_dir)
    if not project.is_dir():
        return []

    ckpts = sorted(
        project.glob("*/weights/last.pt"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    results = []
    for ck in ckpts:
        results.append((ck, ck.stat().st_mtime, read_checkpoint_epoch(ck)))
    return results


def print_checkpoint_table(project_dir):
    """Print all discovered checkpoints with their epoch and modification time."""
    import datetime

    ckpts = find_checkpoints(project_dir)
    if not ckpts:
        print(f"\n[INFO] No checkpoints found under: {Path(project_dir).resolve()}")
        return ckpts

    print("\n" + "=" * 80)
    print(f"AVAILABLE CHECKPOINTS in {Path(project_dir).resolve()}")
    print("=" * 80)
    print(f"{'#':<4}{'RUN':<22}{'PROGRESS':<26}{'LAST MODIFIED':<22}")
    print("-" * 80)
    for i, (ck, mtime, epoch_info) in enumerate(ckpts, 1):
        run_name = ck.parent.parent.name
        when = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        marker = "  <- newest" if i == 1 else ""
        print(f"{i:<4}{run_name:<22}{epoch_info:<26}{when:<22}{marker}")
    print("=" * 80)
    print("\nTo resume a specific run:")
    print(f"  python3 train_yolo_obb.py --data <data.yaml> \\")
    print(f"      --resume {ckpts[0][0]}")
    print()
    return ckpts


def resolve_resume_checkpoint(args):
    """
    Work out which checkpoint to resume from.

    - Explicit path given: validate and use it.
    - No path: auto-detect the MOST RECENT last.pt under the project dir.
      (The original code hardcoded "runs/obb/train/weights/last.pt", which
      silently resumed the wrong — often much older — run, because real runs
      land in train-2/, train-3/, and so on.)
    """
    if isinstance(args.resume, str) and args.resume is not True:
        ckpt = Path(args.resume).expanduser()
        if not ckpt.is_file():
            print(f"\n[ERROR] Checkpoint not found: {ckpt}")
            print_checkpoint_table(args.project)
            sys.exit(1)
        return ckpt.resolve()

    ckpts = find_checkpoints(args.project)
    if not ckpts:
        print(f"\n[ERROR] --resume given but no checkpoints found under "
              f"{Path(args.project).resolve()}")
        print("        Start a fresh run (drop --resume), or pass an explicit path:")
        print("        --resume /path/to/runs/obb/train-N/weights/last.pt")
        sys.exit(1)

    newest, mtime, epoch_info = ckpts[0]
    print(f"\n[INFO] --resume with no path given; auto-detected NEWEST checkpoint:")
    print(f"       {newest}")
    print(f"       Progress: {epoch_info}")
    if len(ckpts) > 1:
        print(f"\n       {len(ckpts) - 1} other checkpoint(s) exist — run with "
              f"--list-runs to see them all,")
        print(f"       or pass an explicit --resume <path> to choose a different one.")
    return newest.resolve()


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
    folder, mirroring the original directory structure. Returns the count.
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

    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
    image_paths = []
    for split_path in splits.values():
        img_dir = dataset_root / split_path
        if img_dir.is_dir():
            # BUGFIX: the original used glob() with both "*.jpg" and "*.JPG"
            # patterns. glob() is non-recursive, and on macOS/Windows (which
            # have case-insensitive filesystems) both patterns match the SAME
            # files — so every image was scanned twice. rglob + a lowercase
            # suffix check fixes both issues.
            for p in img_dir.rglob("*"):
                if p.is_file() and p.suffix.lower() in exts:
                    image_paths.append(p)
        else:
            print(f"[WARN] Image directory not found: {img_dir}")

    # De-dupe defensively in case splits point at overlapping directories
    image_paths = sorted(set(image_paths))

    if not image_paths:
        print("[INFO] No images found to scan.")
        return 0

    print(f"\n[INFO] Pre-scanning {len(image_paths)} images for corruption "
          f"(using cv2 + libjpeg stderr capture)...")

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".txt")
    os.close(tmp_fd)

    corrupt = []
    try:
        for i, path in enumerate(image_paths, 1):
            if i % 200 == 0 or i == len(image_paths):
                print(f"  Scanned {i}/{len(image_paths)}...{' ' * 10}", end="\r")

            cap_fd = os.open(tmp_path, os.O_WRONLY | os.O_TRUNC)
            old_stderr = os.dup(2)
            os.dup2(cap_fd, 2)
            os.close(cap_fd)

            try:
                img = cv2.imread(str(path))
            finally:
                sys.stdout.flush()
                sys.stderr.flush()
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
        # BUGFIX: the original moved images and labels into the SAME flat
        # folder, so files from different splits could collide and restoring
        # was ambiguous. Mirror the original tree instead.
        try:
            rel = img_path.relative_to(dataset_root)
        except ValueError:
            rel = Path(img_path.name)
        img_dest = quarantine_dir / rel
        img_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(img_path), str(img_dest))

        # BUGFIX: the original located the label via a naive string replace of
        # "/images/", which breaks on Windows paths and misfires if the dataset
        # root itself contains "/images/". Operate on path parts instead.
        parts = list(img_path.parts)
        if "images" in parts:
            idx = len(parts) - 1 - parts[::-1].index("images")
            parts[idx] = "labels"
            label_path = Path(*parts).with_suffix(".txt")
            if label_path.exists():
                try:
                    lrel = label_path.relative_to(dataset_root)
                except ValueError:
                    lrel = Path(label_path.name)
                lbl_dest = quarantine_dir / lrel
                lbl_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(label_path), str(lbl_dest))

        print(f"  Quarantined: {img_path.name}  — {reason[:100]}")

    print(f"\n[INFO] {len(corrupt)} file(s) quarantined. Training will skip them.")
    print(f"       To restore, copy the images/ and labels/ trees back from:")
    print(f"       {quarantine_dir}")
    return len(corrupt)


# ---------------------------------------------------------------------------
# Sensible defaults per device
# ---------------------------------------------------------------------------

def device_defaults(device: str) -> dict:
    """
    Conservative starting-point batch sizes per device at imgsz=1600.

    NOTE on MPS (Apple Silicon): unified memory is shared with the OS and all
    other apps, so the usable ceiling is well below nominal RAM. Dense images
    (1000+ objects) spike memory hard inside the label assigner, so the batch
    default is deliberately low.
    """
    if device == "cpu":
        return {"batch": 2, "workers": 2}
    elif device == "mps":
        # BUGFIX: was 4, which OOM'd on a 24 GB Mac at imgsz=1600 with dense
        # (1700+ object) images. 2 is the safe default.
        return {"batch": 2, "workers": 4}
    else:
        return {"batch": 8, "workers": 8}


# ---------------------------------------------------------------------------
# Model selection
# ---------------------------------------------------------------------------

YOLO26_OBB_MODELS = {
    "n": "yolo26n-obb.pt",   # nano   — fastest, good for quick tests
    "s": "yolo26s-obb.pt",   # small  — good balance, recommended start
    "m": "yolo26m-obb.pt",   # medium — recommended for final training
    "l": "yolo26l-obb.pt",   # large  — better accuracy, more memory
    "x": "yolo26x-obb.pt",   # xlarge — best accuracy, most demanding
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

    if not args.skip_scan:
        scan_dataset_for_corrupt_images(data_yaml)
    else:
        print("[INFO] Skipping image corruption scan (--skip-scan).")

    device = args.device if args.device else detect_device()

    defaults = device_defaults(device)
    batch   = args.batch   if args.batch   is not None else defaults["batch"]
    workers = args.workers if args.workers is not None else defaults["workers"]

    # ------------------------------------------------------------------
    # Model / checkpoint selection
    # ------------------------------------------------------------------
    resume_ckpt = None

    if args.resume:
        # TRUE RESUME. Two things were broken before:
        #   1. resume=True was never passed to model.train(), so Ultralytics
        #      started a brand-new run — epoch counter and LR schedule reset,
        #      throwing away the low fine-tuning LR the run had reached.
        #   2. The default path was hardcoded to
        #      "runs/obb/train/weights/last.pt", but real runs land in
        #      train-2/, train-3/, ... so it silently resumed the WRONG run.
        resume_ckpt = resolve_resume_checkpoint(args)
        model = YOLO(str(resume_ckpt))
        model_label = f"RESUME — {resume_ckpt}"

    elif args.weights:
        wpath = Path(args.weights).expanduser()
        if not wpath.is_file():
            print(f"\n[ERROR] --weights file not found: {wpath}")
            sys.exit(1)
        print(f"\n[INFO] Starting a NEW run with weights initialised from: {wpath}")
        print("       (Epoch counter and LR schedule start fresh — this is")
        print("        fine-tuning, not resuming. Use --resume to continue a run.)")
        model = YOLO(str(wpath.resolve()))
        model_label = f"fine-tune from {wpath.name}"

    else:
        model_file = YOLO26_OBB_MODELS.get(args.model)
        if not model_file:
            print(f"\n[ERROR] Unknown model size '{args.model}'. "
                  f"Choose from: {list(YOLO26_OBB_MODELS.keys())}")
            sys.exit(1)
        print(f"\n[INFO] Loading pretrained YOLO26 OBB model: {model_file}")
        print("       (Weights download automatically on first use)")
        model = YOLO(model_file)
        model_label = f"{args.model.upper()} — {model_file}"

    # ------------------------------------------------------------------
    # Print training config
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("YOLO26 OBB TRAINING CONFIGURATION")
    print("=" * 60)
    print(f"  data.yaml  : {data_yaml}")
    print(f"  model      : {model_label}")
    print(f"  device     : {device}")
    if resume_ckpt:
        print(f"  mode       : RESUME (continues epoch count + LR schedule)")
        print(f"\n  NOTE: when resuming, Ultralytics restores epochs, batch,")
        print(f"  imgsz, lr0 and augmentation settings from the checkpoint —")
        print(f"  command-line values for those flags are IGNORED.")
    else:
        print(f"  mode       : NEW RUN")
        print(f"  epochs     : {args.epochs}")
        print(f"  image size : {args.imgsz}px")
        print(f"  batch size : {batch}")
        print(f"  workers    : {workers}")
        print(f"  patience   : {args.patience} epochs (early stopping)")
        print(f"  lr0        : {args.lr0}")
        print(f"  max_det    : {args.max_det}")
        print(f"  mosaic     : {args.mosaic}")
        print(f"  AMP (FP16) : {'disabled (--no-amp)' if args.no_amp else 'enabled'}")
    print(f"  project    : {Path(args.project).resolve()}")
    print(f"  run name   : {args.name}")
    print(f"\n  Scale range note: YOLO26's STAL label assignment helps ensure")
    print(f"  small creatures (~20px) receive positive label coverage during")
    print(f"  training alongside very large ones (1500px+).")
    print("=" * 60 + "\n")

    start = time.time()

    if resume_ckpt:
        # When resuming, Ultralytics reads everything else from the checkpoint.
        # Passing extra args here can confuse it, so keep this minimal.
        train_kwargs = dict(
            data   = str(data_yaml),
            resume = True,
            device = device,
        )
    else:
        train_kwargs = dict(
            data        = str(data_yaml),
            epochs      = args.epochs,
            imgsz       = args.imgsz,
            batch       = batch,
            device      = device,
            workers     = workers,
            project     = str(Path(args.project).resolve()),
            name        = args.name,
            patience    = args.patience,
            save        = True,
            save_period = args.save_period,
            plots       = True,
            verbose     = True,

            # AMP (FP16 mixed precision). Disable if you see repeating NaN/Inf
            # loss warnings — FP16 overflow is the most common cause.
            amp         = not args.no_amp,

            # YOLO's default lr0=0.01 can spike into NaN with aggressive
            # augmentation; 0.005 is more stable.
            lr0         = args.lr0,

            # Max detections per image. Also baked into the ONNX export.
            max_det     = args.max_det,

            # --- Augmentation tuned for Mothbox field photography ---
            degrees     = 180,    # moths appear at any angle on the sheet
            scale       = 0.9,    # covers the huge natural scale range
            flipud      = 0.5,
            fliplr      = 0.5,
            hsv_h       = 0.015,  # variable field lighting
            hsv_s       = 0.7,
            hsv_v       = 0.4,
            # Mosaic stitches 4 images together, multiplying objects per batch
            # and spiking label-assigner memory — the usual cause of OOM on
            # dense datasets. Default 0.0 (off).
            mosaic      = args.mosaic,
            translate   = 0.1,
        )

    results = model.train(**train_kwargs)

    elapsed = time.time() - start
    hours, rem = divmod(int(elapsed), 3600)
    mins, secs = divmod(rem, 60)

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"  Time elapsed : {hours}h {mins}m {secs}s")

    # BUGFIX: the old fallback built save_dir from args.project/args.name,
    # which is wrong whenever Ultralytics auto-increments to train-2, train-3...
    # Prefer trainer.save_dir, then results.save_dir, and only guess last.
    save_dir = None
    trainer = getattr(model, "trainer", None)
    if trainer is not None and getattr(trainer, "save_dir", None):
        save_dir = Path(trainer.save_dir)
    elif getattr(results, "save_dir", None):
        save_dir = Path(results.save_dir)
    else:
        save_dir = Path(args.project).resolve() / args.name
        print(f"  [WARN] Could not read save_dir from trainer; guessing {save_dir}")

    best_weights = save_dir / "weights" / "best.pt"
    last_weights = save_dir / "weights" / "last.pt"

    print(f"  Results saved: {save_dir}")
    print(f"  Best weights : {best_weights}")
    print(f"  Last weights : {last_weights}")

    # --- ONNX export ---
    if not args.no_export:
        if not best_weights.is_file():
            print(f"\n[WARN] best.pt not found at {best_weights} — skipping ONNX export.")
        else:
            print("\n[INFO] Exporting best.pt to ONNX...")
            try:
                export_model = YOLO(str(best_weights))

                # BUGFIX: when resuming, args.imgsz / args.max_det are whatever
                # was typed on the command line, NOT what the model was actually
                # trained with. Read them back from the checkpoint so the export
                # matches the real model.
                exp_imgsz, exp_max_det = args.imgsz, args.max_det
                try:
                    ckpt_args = (getattr(export_model, "ckpt", {}) or {}).get("train_args", {}) or {}
                    exp_imgsz   = ckpt_args.get("imgsz", exp_imgsz)
                    exp_max_det = ckpt_args.get("max_det", exp_max_det)
                except Exception:
                    pass

                print(f"       imgsz={exp_imgsz}, max_det={exp_max_det}")
                onnx_path = export_model.export(
                    format  = "onnx",
                    imgsz   = exp_imgsz,
                    max_det = exp_max_det,
                    # half=True gives a smaller/faster FP16 ONNX but requires
                    # CUDA; FP32 keeps maximum cross-platform compatibility.
                )
                print(f"  ONNX model  : {onnx_path}")
            except Exception as e:
                print(f"  [WARN] ONNX export failed: {e}")
                print("         You can export manually later with:")
                print(f"         from ultralytics import YOLO")
                print(f"         YOLO('{best_weights}').export("
                      f"format='onnx', imgsz={args.imgsz}, max_det={args.max_det})")
    else:
        print("\n[INFO] Skipping ONNX export (--no-export flag set).")

    print("\nTo run inference with your trained model:")
    print(f"  from ultralytics import YOLO")
    print(f"  model = YOLO('{best_weights}')        # PyTorch")
    print(f"  model = YOLO('{best_weights.with_suffix('.onnx')}')  # ONNX")
    print(f"  # Remember to pass max_det at inference time too:")
    print(f"  results = model('img.jpg', max_det={args.max_det}, conf=0.1)")
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
            "specifically helps with the extreme scale variation in Mothbox images.\n\n"
            "IMPORTANT: --resume continues an interrupted run (epoch count and LR\n"
            "schedule carry over). --weights starts a NEW run initialised from an\n"
            "existing model (epoch count and LR restart). They are not the same."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--data", "-d", required=True,
        help="Path to data.yaml produced by collect_yolo_training_data.py"
    )

    parser.add_argument(
        "--model", "-m", default="s",
        choices=list(YOLO26_OBB_MODELS.keys()),
        help=(
            "YOLO26 OBB model size for a fresh run. n=nano (fastest), "
            "s=small (recommended start), m=medium (recommended final), "
            "l=large, x=xlarge. Default: s"
        )
    )
    parser.add_argument(
        "--weights", type=str, default=None,
        help=(
            "Start a NEW run with weights initialised from this .pt file "
            "(fine-tuning). Epoch counter and LR schedule restart. "
            "Use --resume instead to continue an interrupted run."
        )
    )

    parser.add_argument(
        "--epochs", "-e", type=int, default=100,
        help="Number of training epochs. 100 is a solid default; 150-200 for final runs."
    )
    parser.add_argument(
        "--imgsz", type=int, default=1600,
        help=(
            "Input image size (square, pixels). Default: 1600. Large imgsz "
            "preserves detail for small creatures. Reduce to 1280 or 960 if "
            "you run out of memory."
        )
    )
    parser.add_argument(
        "--batch", type=int, default=None,
        help=(
            "Batch size. Auto-set per device if not specified "
            "(2 for CPU, 2 for MPS, 8 for CUDA at imgsz=1600). "
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
    parser.add_argument(
        "--lr0", type=float, default=0.005,
        help=(
            "Initial learning rate. Default: 0.005 (half the YOLO default of "
            "0.01). Lower values reduce NaN/Inf loss spikes with aggressive "
            "augmentation."
        )
    )
    parser.add_argument(
        "--max-det", type=int, default=3000, dest="max_det",
        help=(
            "Maximum detections per image. Baked into the ONNX export, so set "
            "this high enough for your densest images — YOLO's default of 300 "
            "will permanently cap the exported model. Default: 3000."
        )
    )
    parser.add_argument(
        "--mosaic", type=float, default=0.0,
        help=(
            "Mosaic augmentation probability (0.0-1.0). Default: 0.0 (off). "
            "Mosaic stitches 4 images together, multiplying objects per batch "
            "and spiking label-assigner memory — it is the usual cause of OOM "
            "crashes on dense datasets and Apple Silicon. Raise to 0.5-1.0 "
            "only if you have memory headroom."
        )
    )
    parser.add_argument(
        "--no-amp", action="store_true", dest="no_amp",
        help=(
            "Disable FP16 automatic mixed precision and train in FP32. Use "
            "this if you see repeating 'Loss NaN/Inf detected' warnings."
        )
    )

    parser.add_argument(
        "--device", type=str, default=None,
        help=(
            "Device override. Auto-detected if not set. Examples: '0' (first "
            "GPU), '0,1' (multi-GPU), 'cpu', 'mps'."
        )
    )
    parser.add_argument(
        "--workers", type=int, default=None,
        help="DataLoader worker threads. Auto-set per device if not specified."
    )

    parser.add_argument(
        "--project", type=str, default="runs/obb",
        help="Parent directory for training run output. Default: runs/obb"
    )
    parser.add_argument(
        "--name", type=str, default="train",
        help="Name for this run (subfolder inside --project). Default: train"
    )

    parser.add_argument(
        "--resume", nargs="?", const=True, default=False,
        metavar="CHECKPOINT",
        help=(
            "TRUE resume of an interrupted run — epoch counter, LR schedule, "
            "optimizer state and EMA all carry over. With no path, auto-detects "
            "the MOST RECENTLY MODIFIED last.pt under --project. Pass an "
            "explicit path to choose a specific run. NOTE: hyperparameters are "
            "restored from the checkpoint, so --batch/--epochs/--imgsz/--lr0 "
            "are ignored when resuming."
        )
    )
    parser.add_argument(
        "--list-runs", action="store_true", dest="list_runs",
        help=(
            "List every checkpoint found under --project (with its epoch "
            "progress and timestamp) and exit without training. Useful for "
            "working out which run to resume."
        )
    )

    parser.add_argument(
        "--skip-scan", action="store_true", dest="skip_scan",
        help=(
            "Skip the pre-training corruption scan. Use if your dataset is "
            "known-clean and you want to start immediately."
        )
    )

    parser.add_argument(
        "--no-export", action="store_true", dest="no_export",
        help=(
            "Skip automatic ONNX export after training. By default the best.pt "
            "weights are exported to ONNX automatically."
        )
    )

    args = parser.parse_args()

    # --list-runs short-circuits everything else (no --data validation needed)
    if args.list_runs:
        print_checkpoint_table(args.project)
        return

    if args.resume and args.weights:
        print("\n[ERROR] --resume and --weights are mutually exclusive.")
        print("        --resume  continues an interrupted run (epoch/LR carry over)")
        print("        --weights starts a new run from existing weights (epoch/LR reset)")
        sys.exit(1)

    run_training(args)


if __name__ == "__main__":
    main()