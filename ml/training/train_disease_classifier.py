"""
Training Script: EfficientNetB3 Crop Disease Classifier for Agrivision AI+.

Trains an EfficientNetB3 neural network on the 38-class PlantVillage dataset
using a two-phase transfer learning and fine-tuning strategy with data augmentation.

Dataset Requirement:
- PlantVillage dataset extracted into `ml/datasets/plantvillage/`
- Download from: https://www.kaggle.com/datasets/emmarex/plantdisease

Usage:
    python ml/training/train_disease_classifier.py --data-dir ml/datasets/plantvillage --epochs 20
    python ml/training/train_disease_classifier.py --dry-run  # Smoke test with synthetic batch
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

from backend.app.ml.disease.classifier import (
    PLANT_VILLAGE_CLASSES,
    DiseaseClassifier,
)
from ml.training.dataset_utils import get_dataset_dir, get_weights_dir

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_disease_classifier")


def build_data_augmentation() -> tf.keras.Sequential:
    """Create data augmentation pipeline for plant leaves."""
    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal_and_vertical"),
            layers.RandomRotation(0.15),
            layers.RandomZoom(0.15),
            layers.RandomContrast(0.1),
            layers.RandomTranslation(0.08, 0.08),
        ],
        name="plant_data_augmentation",
    )


def train_classifier(
    data_dir: Path,
    output_weights_path: Path,
    batch_size: int = 32,
    phase1_epochs: int = 5,
    phase2_epochs: int = 15,
    img_size: int = 300,
    dry_run: bool = False,
) -> Path:
    """
    Execute two-phase transfer learning on PlantVillage.
    """
    num_classes = len(PLANT_VILLAGE_CLASSES)
    logger.info("Initializing EfficientNetB3 training pipeline for %d classes...", num_classes)

    if dry_run or not data_dir.is_dir():
        if not dry_run:
            logger.warning("PlantVillage folder not found at %s. Running synthetic dry-run smoke test.", data_dir)
        else:
            logger.info("Running synthetic dry-run test mode.")

        # Generate synthetic small dataset for smoke testing
        X_dummy = np.random.uniform(0, 255, size=(32, img_size, img_size, 3)).astype(np.float32)
        y_dummy = tf.keras.utils.to_categorical(np.random.randint(0, num_classes, size=(32,)), num_classes=num_classes)
        train_ds = tf.data.Dataset.from_tensor_slices((X_dummy, y_dummy)).batch(8)
        val_ds = train_ds
        phase1_epochs = 1
        phase2_epochs = 1
    else:
        logger.info("Loading images from %s...", data_dir)
        train_ds = tf.keras.utils.image_dataset_from_directory(
            str(data_dir),
            validation_split=0.2,
            subset="training",
            seed=42,
            image_size=(img_size, img_size),
            batch_size=batch_size,
            label_mode="categorical",
            class_names=PLANT_VILLAGE_CLASSES,
        )
        val_ds = tf.keras.utils.image_dataset_from_directory(
            str(data_dir),
            validation_split=0.2,
            subset="validation",
            seed=42,
            image_size=(img_size, img_size),
            batch_size=batch_size,
            label_mode="categorical",
            class_names=PLANT_VILLAGE_CLASSES,
        )

        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # Instantiate base model with ImageNet pretraining
    logger.info("Instantiating pretrained EfficientNetB3 backbone...")
    base_model = tf.keras.applications.EfficientNetB3(
        include_top=False,
        weights="imagenet",
        input_shape=(img_size, img_size, 3),
    )
    base_model.trainable = False  # Freeze backbone for Phase 1

    # Assemble complete model
    data_aug = build_data_augmentation()
    inputs = layers.Input(shape=(img_size, img_size, 3), name="leaf_image_input")
    x = data_aug(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D(name="avg_pool")(x)
    x = layers.BatchNormalization(name="batch_norm")(x)
    x = layers.Dropout(0.3, name="top_dropout_1")(x)
    x = layers.Dense(256, activation="relu", name="fc_256")(x)
    x = layers.Dropout(0.2, name="top_dropout_2")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="disease_prediction")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="Agrivision_EfficientNetB3_Disease")

    output_weights_path.parent.mkdir(parents=True, exist_ok=True)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(output_weights_path),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    # --- Phase 1: Train classification head ---
    logger.info("=== Phase 1: Training Classification Head (%d epochs) ===", phase1_epochs)
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_acc")],
    )

    h1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=phase1_epochs,
        callbacks=callbacks,
    )

    # --- Phase 2: Fine-tune top layers of backbone ---
    logger.info("=== Phase 2: Fine-Tuning Top Convolutional Layers (%d epochs) ===", phase2_epochs)
    base_model.trainable = True
    # Freeze the bottom layers and unfreeze the top ~40 layers
    for layer in base_model.layers[:-40]:
        layer.trainable = False

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_acc")],
    )

    h2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=phase2_epochs,
        callbacks=callbacks,
    )

    # Save final model
    logger.info("Saving trained model to %s...", output_weights_path)
    model.save(str(output_weights_path))

    # Save training history metrics
    metrics_path = output_weights_path.parent / "efficientnetb3_training_metrics.json"
    history_data = {
        "phase1": {k: [float(v) for v in vals] for k, vals in h1.history.items()},
        "phase2": {k: [float(v) for v in vals] for k, vals in h2.history.items()},
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)

    logger.info("Training complete. Best weights saved to: %s", output_weights_path)
    return output_weights_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train EfficientNetB3 Crop Disease Classifier")
    parser.add_argument("--data-dir", type=str, default="ml/datasets/plantvillage", help="PlantVillage data folder")
    parser.add_argument("--weights-out", type=str, default="ml/models/weights/efficientnetb3_disease.h5")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--phase1-epochs", type=int, default=5)
    parser.add_argument("--phase2-epochs", type=int, default=15)
    parser.add_argument("--dry-run", action="store_true", help="Run quick 1-epoch synthetic sanity test")

    args = parser.parse_args()

    data_path = Path(args.data_dir)
    if not data_path.is_absolute():
        data_path = PROJECT_ROOT / data_path

    weights_out = Path(args.weights_out)
    if not weights_out.is_absolute():
        weights_out = PROJECT_ROOT / weights_out

    train_classifier(
        data_dir=data_path,
        output_weights_path=weights_out,
        batch_size=args.batch_size,
        phase1_epochs=args.phase1_epochs,
        phase2_epochs=args.phase2_epochs,
        dry_run=args.dry_run,
    )
