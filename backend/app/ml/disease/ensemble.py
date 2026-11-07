"""
Ensemble Disease Classifier for Agrivision AI+.

Combines predictions from 4 distinct deep convolutional architectures:
- VGG16 (weight: 0.20)
- VGG19 (weight: 0.20)
- InceptionV3 (weight: 0.30)
- ResNet101V2 (weight: 0.30)

Supports dynamic partial evaluation: if only a subset of models has trained weights,
weights are automatically re-normalized across available models.
"""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from backend.app.ml import ModelStatus, get_model_registry
from backend.app.ml.disease.classifier import PLANT_VILLAGE_CLASSES
from backend.app.ml.preprocessing import (
    assess_image_quality,
    load_image,
    preprocess_for_model,
)

logger = logging.getLogger(__name__)

DEFAULT_ENSEMBLE_CONFIG: Dict[str, Dict[str, Any]] = {
    "VGG16": {
        "input_size": (224, 224),
        "default_weight": 0.20,
        "weights_path": "ml/models/weights/vgg16_disease.h5",
        "registry_key": "ensemble_vgg16",
    },
    "VGG19": {
        "input_size": (224, 224),
        "default_weight": 0.20,
        "weights_path": "ml/models/weights/vgg19_disease.h5",
        "registry_key": "ensemble_vgg19",
    },
    "InceptionV3": {
        "input_size": (299, 299),
        "default_weight": 0.30,
        "weights_path": "ml/models/weights/inceptionv3_disease.h5",
        "registry_key": "ensemble_inceptionv3",
    },
    "ResNet101V2": {
        "input_size": (224, 224),
        "default_weight": 0.30,
        "weights_path": "ml/models/weights/resnet101v2_disease.h5",
        "registry_key": "ensemble_resnet101v2",
    },
}


class EnsembleClassifier:
    """
    Weighted-average ensemble classification engine.
    """

    def __init__(
        self,
        weights_config: Optional[Dict[str, float]] = None,
        custom_weights_paths: Optional[Dict[str, Union[str, Path]]] = None,
        labels_path: Optional[Union[str, Path]] = None,
        auto_load: bool = True,
    ) -> None:
        self.num_classes = len(PLANT_VILLAGE_CLASSES)
        self.classes = PLANT_VILLAGE_CLASSES
        self.registry = get_model_registry()

        # Resolve paths
        project_root = Path(__file__).resolve().parents[4]
        self.labels_path = Path(
            labels_path or (project_root / "ml" / "configs" / "class_labels.json")
        )
        self.disease_details: Dict[str, Any] = {}
        self._load_label_metadata()

        # Model configs and weights
        self.model_configs: Dict[str, Dict[str, Any]] = {}
        for m_name, cfg in DEFAULT_ENSEMBLE_CONFIG.items():
            path_val = (
                custom_weights_paths.get(m_name)
                if custom_weights_paths and m_name in custom_weights_paths
                else cfg["weights_path"]
            )
            p = Path(path_val)
            if not p.is_absolute():
                p = project_root / p

            weight = (
                weights_config.get(m_name, cfg["default_weight"])
                if weights_config
                else cfg["default_weight"]
            )

            self.model_configs[m_name] = {
                "input_size": cfg["input_size"],
                "weight": weight,
                "weights_path": p,
                "registry_key": cfg["registry_key"],
            }

        self.loaded_models: Dict[str, Any] = {}
        self.model_statuses: Dict[str, ModelStatus] = {}

        if auto_load:
            self.load_all()

    def _load_label_metadata(self) -> None:
        if self.labels_path.is_file():
            try:
                with open(self.labels_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.disease_details = data.get("disease_details", {})
            except Exception as e:
                logger.warning("Could not read labels file %s: %s", self.labels_path, e)

    @staticmethod
    def build_model_architecture(
        model_name: str,
        input_size: Tuple[int, int],
        num_classes: int = 38,
        load_imagenet: bool = False,
    ) -> Any:
        """Construct individual ensemble member architecture."""
        import tensorflow as tf
        from tensorflow.keras import layers, models

        m_key = model_name.lower()
        if m_key == "vgg16":
            base = tf.keras.applications.VGG16(
                include_top=False,
                weights="imagenet" if load_imagenet else None,
                input_shape=(input_size[0], input_size[1], 3),
            )
        elif m_key == "vgg19":
            base = tf.keras.applications.VGG19(
                include_top=False,
                weights="imagenet" if load_imagenet else None,
                input_shape=(input_size[0], input_size[1], 3),
            )
        elif m_key == "inceptionv3":
            base = tf.keras.applications.InceptionV3(
                include_top=False,
                weights="imagenet" if load_imagenet else None,
                input_shape=(input_size[0], input_size[1], 3),
            )
        elif m_key == "resnet101v2":
            base = tf.keras.applications.ResNet101V2(
                include_top=False,
                weights="imagenet" if load_imagenet else None,
                input_shape=(input_size[0], input_size[1], 3),
            )
        else:
            raise ValueError(f"Unknown ensemble architecture: {model_name}")

        inputs = layers.Input(shape=(input_size[0], input_size[1], 3), name=f"{model_name}_input")
        x = base(inputs, training=False)
        x = layers.GlobalAveragePooling2D(name=f"{model_name}_gap")(x)
        x = layers.BatchNormalization(name=f"{model_name}_bn")(x)
        x = layers.Dense(256, activation="relu", name=f"{model_name}_fc256")(x)
        x = layers.Dropout(0.3, name=f"{model_name}_dropout")(x)
        outputs = layers.Dense(num_classes, activation="softmax", name=f"{model_name}_output")(x)

        return models.Model(inputs=inputs, outputs=outputs, name=f"Agrivision_{model_name}")

    def load_all(self) -> Dict[str, bool]:
        """Attempt loading all 4 ensemble model weights."""
        results = {}
        for name in ["VGG16", "VGG19", "InceptionV3", "ResNet101V2"]:
            results[name] = self.load_model(name)
        return results

    def load_model(self, name: str) -> bool:
        """Load single ensemble model weights."""
        cfg = self.model_configs[name]
        weights_path: Path = cfg["weights_path"]
        reg_key: str = cfg["registry_key"]

        if not weights_path.is_file():
            self.model_statuses[name] = ModelStatus.WEIGHTS_MISSING
            self.registry.set_status(reg_key, ModelStatus.WEIGHTS_MISSING, error_message="File missing")
            logger.info("Ensemble model %s weights not found at %s", name, weights_path)
            return False

        try:
            import tensorflow as tf

            logger.info("Loading ensemble member %s from %s...", name, weights_path)
            try:
                model = tf.keras.models.load_model(str(weights_path), compile=False)
            except Exception:
                model = self.build_model_architecture(
                    name, input_size=cfg["input_size"], num_classes=self.num_classes
                )
                model.load_weights(str(weights_path))

            self.loaded_models[name] = model
            self.model_statuses[name] = ModelStatus.AVAILABLE
            self.registry.set_status(reg_key, ModelStatus.AVAILABLE, instance=model)
            return True
        except Exception as e:
            self.model_statuses[name] = ModelStatus.LOAD_FAILED
            self.registry.set_status(reg_key, ModelStatus.LOAD_FAILED, error_message=str(e))
            logger.error("Failed to load %s weights: %s", name, e, exc_info=True)
            return False

    def predict(
        self,
        image_input: Union[str, Path, bytes, np.ndarray],
        top_k: int = 5,
        check_quality: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute ensemble inference using all available models.
        Dynamically normalizes weights if only a subset of models is available.
        """
        t0 = time.perf_counter()

        available_models = [m for m, model in self.loaded_models.items() if model is not None]
        unavailable_models = [m for m in self.model_configs if m not in available_models]

        if not available_models:
            return {
                "status": "model_unavailable",
                "model_available": False,
                "ensemble_type": "weighted_average",
                "models_used": [],
                "models_unavailable": unavailable_models,
                "message": (
                    "No ensemble models are available. Please train weights using "
                    "'python ml/training/train_ensemble_models.py'"
                ),
                "inference_time_ms": round((time.perf_counter() - t0) * 1000, 2),
            }

        try:
            img_rgb = load_image(image_input, to_rgb=True)
            quality_info = assess_image_quality(img_rgb) if check_quality else {}

            # Calculate normalized weights for available models
            raw_weights = {m: self.model_configs[m]["weight"] for m in available_models}
            total_weight = sum(raw_weights.values())
            normalized_weights = {m: w / total_weight for m, w in raw_weights.items()}

            individual_predictions: Dict[str, Any] = {}
            inference_times: Dict[str, float] = {}
            weighted_probabilities = np.zeros(self.num_classes, dtype=np.float64)

            for m_name in available_models:
                cfg = self.model_configs[m_name]
                model = self.loaded_models[m_name]

                t_start_m = time.perf_counter()
                tensor = preprocess_for_model(
                    img_rgb,
                    model_name=m_name,
                    target_size=cfg["input_size"],
                )
                preds = model.predict(tensor, verbose=0)[0]
                m_duration = (time.perf_counter() - t_start_m) * 1000
                inference_times[m_name] = round(m_duration, 2)

                top_idx = int(np.argmax(preds))
                individual_predictions[m_name] = {
                    "predicted_class": self.classes[top_idx],
                    "confidence": round(float(preds[top_idx]), 4),
                    "confidence_percentage": round(float(preds[top_idx]) * 100.0, 2),
                    "ensemble_weight": round(normalized_weights[m_name], 4),
                    "inference_time_ms": round(m_duration, 2),
                }

                weighted_probabilities += preds * normalized_weights[m_name]

            # Aggregate ensemble results
            top_indices = np.argsort(weighted_probabilities)[::-1][:top_k]
            top_predictions = []
            for idx in top_indices:
                cls_key = self.classes[idx]
                conf = float(weighted_probabilities[idx])
                details = self.disease_details.get(cls_key, {})

                top_predictions.append(
                    {
                        "class_index": int(idx),
                        "class_name": cls_key,
                        "crop": details.get("crop", cls_key.split("___")[0]),
                        "disease": details.get("disease", cls_key.split("___")[1].replace("_", " ")),
                        "is_healthy": details.get("is_healthy", "healthy" in cls_key.lower()),
                        "confidence": round(conf, 4),
                        "confidence_percentage": round(conf * 100.0, 2),
                        "name_en": details.get("en", cls_key.replace("___", " - ")),
                        "name_mr": details.get("mr", ""),
                        "name_hi": details.get("hi", ""),
                        "treatment": details.get("treatment", ""),
                    }
                )

            primary = top_predictions[0]
            total_duration = (time.perf_counter() - t0) * 1000

            return {
                "status": "success",
                "model_available": True,
                "ensemble_prediction": primary["class_name"],
                "disease": primary["disease"],
                "crop": primary["crop"],
                "is_healthy": primary["is_healthy"],
                "confidence": primary["confidence"],
                "confidence_percentage": primary["confidence_percentage"],
                "multilingual": {
                    "en": primary["name_en"],
                    "mr": primary["name_mr"],
                    "hi": primary["name_hi"],
                },
                "treatment_recommendation": primary["treatment"],
                "individual_predictions": individual_predictions,
                "top_k_predictions": top_predictions,
                "models_used": available_models,
                "models_unavailable": unavailable_models,
                "inference_times": inference_times,
                "total_processing_time_ms": round(total_duration, 2),
                "quality_assessment": quality_info,
            }

        except Exception as exc:
            logger.error("Ensemble inference failed: %s", exc, exc_info=True)
            return {
                "status": "error",
                "model_available": True,
                "error": str(exc),
                "inference_time_ms": round((time.perf_counter() - t0) * 1000, 2),
            }
