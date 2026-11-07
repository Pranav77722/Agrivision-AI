"""
Training Script: Ensemble Deep Learning Models for Agrivision AI+.

Trains the four complementary deep CNN backbones on PlantVillage:
1. VGG16 (224x224)
2. VGG19 (224x224)
3. InceptionV3 (299x299)
4. ResNet101V2 (224x224)

Classification head:
GlobalAveragePooling2D -> BatchNormalization -> Dense(256, relu) -> Dropout(0.3) -> Dense(38, softmax)

Dataset Requirement:
- PlantVillage dataset extracted into `ml/datasets/plantvillage/`

Usage:
    python ml/training/train_ensemble_models.py --model VGG16 --epochs 10
    python ml/training/train_ensemble_models.py --all --epochs 10
    python ml/training/train_ensemble_models.py --model InceptionV3 --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

from backend.app.ml.disease.classifier import PLANT_VILLAGE_CLASSES
from backend.app.ml.disease.ensemble import DEFAULT_ENSEMBLE_CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_ensemble")


def train_single_model(
    model_name: str,
    data_dir: Path,
    weights_out: Path,
    epochs: int = 10,
    batch_size: int = 32,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Train single ensemble member CNN architecture."""
    cfg = DEFAULT_ENSEMBLE_CONFIG[model_name]
    input_size = cfg["input_size"]
    num_classes = len(PLANT_VILLAGE_CLASSES)

    logger.info("==================================================")
    logger.info("Starting training for ensemble member: %s", model_name)
    logger.info("Input resolution: %s, Classes: %d", input_size, num_classes)
    logger.info("==================================================")

    if dry_run or not data_dir.is_dir():
        if not dry_run:
            logger.warning("PlantVillage folder not found at %s. Running dry-run test mode.", data_dir)
        X_dummy = np.random.uniform(0, 255, size=(32, input_size[0], input_size[1], 3)).astype(np.float32)
        y_dummy = tf.keras.utils.to_categorical(np.random.randint(0, num_classes, size=(32,)), num_classes=num_classes)
        train_ds = tf.data.Dataset.from_tensor_slices((X_dummy, y_dummy)).batch(8)
        val_ds = train_ds
        epochs = 1
    else:
        train_ds = tf.keras.utils.image_dataset_from_directory(
            str(data_dir),
            validation_split=0.2,
            subset="training",
            seed=42,
            image_size=input_size,
            batch_size=batch_size,
            label_mode="categorical",
            class_names=PLANT_VILLAGE_CLASSES,
        )
        val_ds = tf.keras.utils.image_dataset_from_directory(
            str(data_dir),
            validation_split=0.2,
            subset="validation",
            seed=42,
            image_size=input_size,
            batch_size=batch_size,
            label_mode="categorical",
            class_names=PLANT_VILLAGE_CLASSES,
        )
        train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
        val_ds = val_ds.prefetch(tf.data.AUTOTUNE)

    # Backbone selection
    m_key = model_name.lower()
    if m_key == "vgg16":
        base_model = tf.keras.applications.VGG16(
            include_top=False, weights="imagenet", input_shape=(input_size[0], input_size[1], 3)
        )
    elif m_key == "vgg19":
        base_model = tf.keras.applications.VGG19(
            include_top=False, weights="imagenet", input_shape=(input_size[0], input_size[1], 3)
        )
    elif m_key == "inceptionv3":
        base_model = tf.keras.applications.InceptionV3(
            include_top=False, weights="imagenet", input_shape=(input_size[0], input_size[1], 3)
        )
    elif m_key == "resnet101v2":
        base_model = tf.keras.applications.ResNet101V2(
            include_top=False, weights="imagenet", input_shape=(input_size[0], input_size[1], 3)
        )
    else:
        raise ValueError(f"Unknown architecture {model_name}")

    base_model.trainable = False

    inputs = layers.Input(shape=(input_size[0], input_size[1], 3), name=f"{model_name}_input")
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D(name=f"{model_name}_gap")(x)
    x = layers.BatchNormalization(name=f"{model_name}_bn")(x)
    x = layers.Dense(256, activation="relu", name=f"{model_name}_fc256")(x)
    x = layers.Dropout(0.3, name=f"{model_name}_dropout")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name=f"{model_name}_output")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name=f"Agrivision_{model_name}")

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_acc")],
    )

    weights_out.parent.mkdir(parents=True, exist_ok=True)
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(weights_out),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=2, min_lr=1e-6),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
    )

    model.save(str(weights_out))
    logger.info("Successfully trained and saved %s to %s", model_name, weights_out)

    metrics_file = weights_out.parent / f"{model_name.lower()}_metrics.json"
    metrics_summary = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)

    return metrics_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Ensemble Disease Classification Models")
    parser.add_argument("--model", type=str, choices=["VGG16", "VGG19", "InceptionV3", "ResNet101V2"], help="Train single model")
    parser.add_argument("--all", action="store_true", help="Train all 4 ensemble models sequentially")
    parser.add_argument("--data-dir", type=str, default="ml/datasets/plantvillage")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--dry-run", action="store_true", help="Quick sanity test")

    args = parser.parse_args()

    data_path = Path(args.data_dir)
    if not data_path.is_absolute():
        data_path = PROJECT_ROOT / data_path

    target_models = ["VGG16", "VGG19", "InceptionV3", "ResNet101V2"] if args.all else ([args.model] if args.model else ["VGG16"])

    for m in target_models:
        w_path = PROJECT_ROOT / DEFAULT_ENSEMBLE_CONFIG[m]["weights_path"]
        train_single_model(
            model_name=m,
            data_dir=data_path,
            weights_out=w_path,
            epochs=args.epochs,
            batch_size=args.batch_size,
            dry_run=args.dry_run,
        )
