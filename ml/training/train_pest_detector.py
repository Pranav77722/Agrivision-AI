"""
Training Script: YOLOv8 / YOLO11 Pest Detector for Agrivision AI+.

Fine-tunes Ultralytics YOLO models on agricultural pest datasets (e.g. IP102 or custom annotated pests).

Dataset Requirement:
- Dataset directory structured in standard YOLO format:
    dataset/
      ├── data.yaml
      ├── images/
      │     ├── train/
      │     └── val/
      └── labels/
            ├── train/
            └── val/

- Label annotation format (one row per bounding box):
    `<class_id> <x_center> <y_center> <width> <height>` (normalized between 0.0 and 1.0)

Usage:
    python ml/training/train_pest_detector.py --data ml/datasets/ip102_yolo/data.yaml --epochs 50 --model yolov8n.pt
    python ml/training/train_pest_detector.py --dry-run
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np
import yaml
from ultralytics import YOLO

from backend.app.ml.pest.detector import AGRICULTURAL_PESTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_pest_detector")


def generate_sample_pest_dataset(dest_dir: Path) -> Path:
    """Create a minimal valid YOLO dataset for sanity testing and pipeline dry-runs."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    images_train = dest_dir / "images" / "train"
    images_val = dest_dir / "images" / "val"
    labels_train = dest_dir / "labels" / "train"
    labels_val = dest_dir / "labels" / "val"

    for d in [images_train, images_val, labels_train, labels_val]:
        d.mkdir(parents=True, exist_ok=True)

    # Generate synthetic images with colored circles mimicking pests
    for split_img, split_lbl, count in [(images_train, labels_train, 8), (images_val, labels_val, 2)]:
        for i in range(count):
            img = np.full((640, 640, 3), 120, dtype=np.uint8)  # gray background
            # Draw leaf green patch
            cv2.ellipse(img, (320, 320), (220, 150), 30, 0, 360, (40, 160, 40), -1)
            # Draw synthetic pest
            px, py, pr = 300 + (i * 10), 300 + (i * 5), 25
            cv2.circle(img, (px, py), pr, (20, 20, 180), -1)

            img_name = f"sample_pest_{i}.jpg"
            lbl_name = f"sample_pest_{i}.txt"

            cv2.imwrite(str(split_img / img_name), img)

            # YOLO format: cls_id x_center y_center w h
            x_c, y_c = px / 640.0, py / 640.0
            w_box, h_box = (pr * 2) / 640.0, (pr * 2) / 640.0
            cls_id = i % len(AGRICULTURAL_PESTS)
            with open(split_lbl / lbl_name, "w", encoding="utf-8") as f:
                f.write(f"{cls_id} {x_c:.4f} {y_c:.4f} {w_box:.4f} {h_box:.4f}\n")

    yaml_data = {
        "path": str(dest_dir.resolve()),
        "train": "images/train",
        "val": "images/val",
        "names": {i: name for i, name in enumerate(AGRICULTURAL_PESTS)},
    }

    yaml_file = dest_dir / "data.yaml"
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, default_flow_style=False)

    logger.info("Generated sample YOLO pest dataset at %s", yaml_file)
    return yaml_file


def train_pest_detector(
    data_yaml: Path,
    output_weights_path: Path,
    base_model: str = "yolov8n.pt",
    epochs: int = 50,
    imgsz: int = 640,
    batch_size: int = 16,
    dry_run: bool = False,
) -> Path:
    """Train YOLO pest detection model."""
    logger.info("Initializing YOLO pest detector training with %s...", base_model)

    if dry_run or not data_yaml.is_file():
        if not dry_run:
            logger.warning("data.yaml not found at %s. Creating sample dataset for dry run.", data_yaml)
        sample_dir = PROJECT_ROOT / "ml" / "datasets" / "sample_pest_yolo"
        data_yaml = generate_sample_pest_dataset(sample_dir)
        epochs = 1
        batch_size = 4

    model = YOLO(base_model)

    output_weights_path.parent.mkdir(parents=True, exist_ok=True)
    project_run_dir = output_weights_path.parent / "yolo_runs"

    logger.info("Starting training on %s for %d epochs...", data_yaml, epochs)
    results = model.train(
        data=str(data_yaml),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch_size,
        project=str(project_run_dir),
        name="agrivision_pest",
        exist_ok=True,
        verbose=True,
    )

    # Copy best weights to target location
    best_pt = project_run_dir / "agrivision_pest" / "weights" / "best.pt"
    if best_pt.is_file():
        shutil.copy(best_pt, output_weights_path)
        logger.info("Copied best model weights to: %s", output_weights_path)
    else:
        # Save model directly
        model.save(str(output_weights_path))
        logger.info("Saved trained YOLO model to: %s", output_weights_path)

    return output_weights_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8 Agricultural Pest Detector")
    parser.add_argument("--data", type=str, default="ml/datasets/ip102_yolo/data.yaml")
    parser.add_argument("--weights-out", type=str, default="ml/models/weights/yolov8_pest.pt")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Base model (yolov8n.pt, yolov8s.pt, yolo11n.pt)")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--dry-run", action="store_true", help="Quick 1-epoch sanity test with synthetic sample data")

    args = parser.parse_args()

    data_file = Path(args.data)
    if not data_file.is_absolute():
        data_file = PROJECT_ROOT / data_file

    out_weights = Path(args.weights_out)
    if not out_weights.is_absolute():
        out_weights = PROJECT_ROOT / out_weights

    train_pest_detector(
        data_yaml=data_file,
        output_weights_path=out_weights,
        base_model=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch_size=args.batch,
        dry_run=args.dry_run,
    )
