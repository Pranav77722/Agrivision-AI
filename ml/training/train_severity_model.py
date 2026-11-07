"""
Training Script: U-Net Leaf Disease Severity Segmentation Model for Agrivision AI+.

Trains a U-Net semantic segmentation network on paired RGB leaf images and lesion masks.
Uses a combined loss function: Dice Loss + Binary Cross-Entropy Loss.

Dataset Requirement:
- Directory with images and corresponding ground truth segmentation masks:
    ml/datasets/leaf_segmentation/
      ├── images/
      │     ├── leaf_001.jpg
      │     └── ...
      └── masks/
            ├── leaf_001.png (values: 0 = background, 1 = healthy leaf, 2 = diseased lesion)
            └── ...

Usage:
    python ml/training/train_severity_model.py --data-dir ml/datasets/leaf_segmentation --epochs 25
    python ml/training/train_severity_model.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras import optimizers

from backend.app.ml.severity.estimator import build_unet_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_severity")


def dice_coef(y_true: tf.Tensor, y_pred: tf.Tensor, smooth: float = 1e-6) -> tf.Tensor:
    """Compute Sørensen–Dice coefficient."""
    y_true_f = K.flatten(K.cast(y_true, "float32"))
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2.0 * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_loss(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """Dice loss = 1 - Dice coefficient."""
    return 1.0 - dice_coef(y_true, y_pred)


def combo_bce_dice_loss(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """Combo loss: 0.5 * BCE + 0.5 * Dice Loss."""
    bce = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    d_loss = dice_loss(y_true, y_pred)
    return 0.5 * bce + 0.5 * d_loss


def generate_synthetic_segmentation_batch(
    num_samples: int = 16,
    img_size: Tuple[int, int] = (256, 256),
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic leaf images and 2-channel masks for smoke testing."""
    h, w = img_size
    images = np.zeros((num_samples, h, w, 3), dtype=np.float32)
    masks = np.zeros((num_samples, h, w, 2), dtype=np.float32)

    for i in range(num_samples):
        img = np.full((h, w, 3), 40, dtype=np.uint8)
        # Draw healthy leaf
        cv2.ellipse(img, (w // 2, h // 2), (w // 3, h // 4), 20, 0, 360, (34, 197, 94), -1)
        # Draw lesion
        lx, ly = w // 2 + (i * 2), h // 2 + (i * 2)
        cv2.circle(img, (lx, ly), 22, (239, 68, 68), -1)

        images[i] = img.astype(np.float32) / 255.0

        # Mask: channel 0 = healthy leaf, channel 1 = lesion
        m_leaf = (img[..., 1] > 100) & (img[..., 0] < 100)
        m_lesion = img[..., 0] > 180

        masks[i, :, :, 0] = m_leaf.astype(np.float32)
        masks[i, :, :, 1] = m_lesion.astype(np.float32)

    return images, masks


def train_severity_model(
    data_dir: Path,
    output_weights_path: Path,
    epochs: int = 25,
    batch_size: int = 16,
    input_size: Tuple[int, int] = (256, 256),
    dry_run: bool = False,
) -> Path:
    """Train U-Net on leaf disease segmentation."""
    logger.info("Initializing U-Net leaf severity segmentation model...")

    model = build_unet_model(input_size=input_size, num_classes=2)
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-4),
        loss=combo_bce_dice_loss,
        metrics=["accuracy", dice_coef],
    )

    if dry_run or not (data_dir / "images").is_dir():
        if not dry_run:
            logger.warning("Segmentation data not found at %s. Using synthetic batch for dry-run.", data_dir)
        X, Y = generate_synthetic_segmentation_batch(16, input_size)
        train_ds = tf.data.Dataset.from_tensor_slices((X, Y)).batch(4)
        val_ds = train_ds
        epochs = 1
    else:
        # Load from image & mask pairs
        img_files = sorted(list((data_dir / "images").glob("*.jpg")) + list((data_dir / "images").glob("*.png")))
        mask_files = sorted(list((data_dir / "masks").glob("*.png")))
        logger.info("Found %d images and %d masks in %s", len(img_files), len(mask_files), data_dir)

        def generator():
            for img_p, msk_p in zip(img_files, mask_files):
                img = cv2.imread(str(img_p))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, input_size) / 255.0

                msk = cv2.imread(str(msk_p), cv2.IMREAD_GRAYSCALE)
                msk = cv2.resize(msk, input_size, interpolation=cv2.INTER_NEAREST)

                mask_2ch = np.zeros((input_size[0], input_size[1], 2), dtype=np.float32)
                mask_2ch[..., 0] = (msk == 1).astype(np.float32)  # healthy
                mask_2ch[..., 1] = (msk == 2).astype(np.float32)  # diseased
                yield img.astype(np.float32), mask_2ch

        output_sig = (
            tf.TensorSpec(shape=(input_size[0], input_size[1], 3), dtype=tf.float32),
            tf.TensorSpec(shape=(input_size[0], input_size[1], 2), dtype=tf.float32),
        )
        ds = tf.data.Dataset.from_generator(generator, output_signature=output_sig)
        train_ds = ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
        val_ds = train_ds

    output_weights_path.parent.mkdir(parents=True, exist_ok=True)
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(output_weights_path),
            monitor="loss",
            mode="min",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(monitor="loss", patience=5, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="loss", factor=0.2, patience=3, min_lr=1e-6),
    ]

    logger.info("Starting U-Net training for %d epochs...", epochs)
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
    )

    model.save(str(output_weights_path))
    logger.info("Saved trained U-Net severity model to: %s", output_weights_path)

    metrics_file = output_weights_path.parent / "unet_severity_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump({k: [float(v) for v in vals] for k, vals in history.history.items()}, f, indent=2)

    return output_weights_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train U-Net Disease Severity Segmentation")
    parser.add_argument("--data-dir", type=str, default="ml/datasets/leaf_segmentation")
    parser.add_argument("--weights-out", type=str, default="ml/models/weights/unet_severity.h5")
    parser.add_argument("--epochs", type=int, default=25)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--dry-run", action="store_true", help="Quick sanity test with synthetic sample data")

    args = parser.parse_args()

    d_path = Path(args.data_dir)
    if not d_path.is_absolute():
        d_path = PROJECT_ROOT / d_path

    w_out = Path(args.weights_out)
    if not w_out.is_absolute():
        w_out = PROJECT_ROOT / w_out

    train_severity_model(
        data_dir=d_path,
        output_weights_path=w_out,
        epochs=args.epochs,
        batch_size=args.batch,
        dry_run=args.dry_run,
    )
