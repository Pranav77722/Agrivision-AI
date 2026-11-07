"""
EfficientNetB3 Crop Disease Classifier for Agrivision AI+.

Preprocesses plant leaf images and classifies them into 38 PlantVillage crop-disease categories
using a deep convolutional EfficientNetB3 architecture in TensorFlow/Keras.
Includes graceful fallback when trained weights are missing.
"""

from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image

try:
    from app.core.config import settings
except ImportError:
    try:
        from backend.app.core.config import settings
    except ImportError:
        settings = None

try:
    from backend.app.ml import ModelStatus, get_model_registry
    from backend.app.ml.preprocessing import (
        assess_image_quality,
        load_image,
        preprocess_for_model,
    )
except ImportError:
    from app.ml import ModelStatus, get_model_registry
    from app.ml.preprocessing import (
        assess_image_quality,
        load_image,
        preprocess_for_model,
    )

logger = logging.getLogger(__name__)

# The 38 canonical PlantVillage classes
PLANT_VILLAGE_CLASSES: List[str] = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry___Powdery_mildew",
    "Cherry___healthy",
    "Corn___Cercospora_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Grape___Black_rot",
    "Grape___Esca",
    "Grape___Leaf_blight",
    "Grape___healthy",
    "Orange___Haunglongbing",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper___Bacterial_spot",
    "Pepper___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Target_Spot",
    "Tomato___Yellow_Leaf_Curl_Virus",
    "Tomato___Mosaic_virus",
    "Tomato___healthy",
]


class DiseaseClassifier:
    """
    Production inference engine for crop disease identification using EfficientNetB3.
    """

    def __init__(
        self,
        model_path: Optional[Union[str, Path]] = None,
        weights_path: Optional[Union[str, Path]] = None,
        labels_path: Optional[Union[str, Path]] = None,
        input_size: Tuple[int, int] = (300, 300),
        auto_load: bool = True,
    ) -> None:
        self.input_size = input_size
        self.num_classes = len(PLANT_VILLAGE_CLASSES)
        self.classes = PLANT_VILLAGE_CLASSES

        # Determine file path
        target_path = model_path or weights_path
        if not target_path:
            target_path = (
                getattr(settings, "DISEASE_MODEL_PATH", None)
                or os.environ.get("DISEASE_MODEL_WEIGHTS", "ml/models/weights/efficientnetb3_disease.h5")
            )

        project_root = Path(__file__).resolve().parents[4]
        self.weights_path = Path(target_path)
        if not self.weights_path.is_absolute():
            self.weights_path = project_root / self.weights_path
        self.model_path = str(self.weights_path)

        # Labels metadata
        self.labels_path = Path(
            labels_path or (project_root / "ml" / "configs" / "class_labels.json")
        )
        self.disease_details: Dict[str, Any] = {}
        self._load_label_metadata()

        self.model: Optional[Any] = None
        self.status: ModelStatus = ModelStatus.NOT_INITIALIZED
        self.model_loaded: bool = False
        self.registry = get_model_registry()

        if auto_load:
            self.load()

    def _load_label_metadata(self) -> None:
        """Load multilingual translation metadata for classes if available."""
        if self.labels_path.is_file():
            try:
                with open(self.labels_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.disease_details = data.get("disease_details", {})
            except Exception as e:
                logger.warning("Could not parse class labels file %s: %s", self.labels_path, e)

    def build_architecture(self, load_imagenet_backbone: bool = False) -> Any:
        """Construct the EfficientNetB3 fine-tuning architecture."""
        import tensorflow as tf
        from tensorflow.keras import layers, models

        base_model = tf.keras.applications.EfficientNetB3(
            include_top=False,
            weights="imagenet" if load_imagenet_backbone else None,
            input_shape=(self.input_size[0], self.input_size[1], 3),
        )

        inputs = layers.Input(shape=(self.input_size[0], self.input_size[1], 3), name="leaf_image_input")
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D(name="avg_pool")(x)
        x = layers.BatchNormalization(name="batch_norm")(x)
        x = layers.Dropout(0.3, name="top_dropout_1")(x)
        x = layers.Dense(256, activation="relu", name="fc_256")(x)
        x = layers.Dropout(0.2, name="top_dropout_2")(x)
        outputs = layers.Dense(self.num_classes, activation="softmax", name="disease_prediction")(x)

        model = models.Model(inputs=inputs, outputs=outputs, name="Agrivision_EfficientNetB3_Disease")
        return model

    def load(self) -> bool:
        """Load model weights into memory."""
        t0 = time.perf_counter()
        if not self.weights_path.is_file():
            self.status = ModelStatus.WEIGHTS_MISSING
            self.model_loaded = False
            self.registry.set_status(
                "disease_classifier",
                ModelStatus.WEIGHTS_MISSING,
                error_message=f"Weights file not found at {self.weights_path}",
            )
            logger.info(
                "EfficientNetB3 weights not found at %s. Inference requests will report model_unavailable.",
                self.weights_path,
            )
            return False

        try:
            import tensorflow as tf

            logger.info("Loading EfficientNetB3 model from %s...", self.weights_path)
            try:
                self.model = tf.keras.models.load_model(str(self.weights_path), compile=False)
            except Exception as load_err:
                logger.info("Constructing architecture and loading weights: %s", load_err)
                self.model = self.build_architecture(load_imagenet_backbone=False)
                self.model.load_weights(str(self.weights_path))

            self.status = ModelStatus.AVAILABLE
            self.model_loaded = True
            self.registry.set_status("disease_classifier", ModelStatus.AVAILABLE, instance=self.model)
            load_time = (time.perf_counter() - t0) * 1000
            logger.info("EfficientNetB3 loaded successfully in %.2f ms.", load_time)
            return True
        except Exception as exc:
            self.status = ModelStatus.LOAD_FAILED
            self.model_loaded = False
            self.registry.set_status(
                "disease_classifier",
                ModelStatus.LOAD_FAILED,
                error_message=str(exc),
            )
            logger.error("Failed to load EfficientNetB3 disease classifier: %s", exc, exc_info=True)
            return False

    def predict(
        self,
        image: Any,
        crop_hint: str = "Unknown",
        top_k: int = 5,
        check_quality: bool = True,
    ) -> Dict[str, Any]:
        """
        Run disease classification on input image.

        Args:
            image: Image path, bytes, PIL Image, or numpy array.
            crop_hint: Optional crop species hint.
            top_k: Number of highest-probability candidate classes to return.
            check_quality: If True, assess blur and brightness.

        Returns:
            Dict containing classification results, top-k candidates, timing,
            or an explicit 'model_unavailable' status when weights are absent.
        """
        start_time = time.perf_counter()

        if self.status != ModelStatus.AVAILABLE or self.model is None:
            return {
                "status": "model_unavailable",
                "model_available": False,
                "model_name": "EfficientNetB3",
                "predicted_disease": "Model Weights Missing",
                "crop_type": crop_hint or "Unknown",
                "confidence": 0.0,
                "model_version": "EfficientNetB3-WeightsUnavailable",
                "weights_path": str(self.weights_path),
                "error": "Model weights are not available on this server.",
                "message": (
                    "EfficientNetB3 model weights not found. Please train weights using "
                    "'python ml/training/train_disease_classifier.py' and place at "
                    f"'{self.weights_path}'."
                ),
                "ensemble_results": {
                    "models": [],
                    "consensus_agreement": 0.0,
                    "voting_method": "Unavailable",
                },
                "top_k_predictions": [],
                "inference_time_ms": round((time.perf_counter() - start_time) * 1000, 2),
            }

        try:
            img_rgb = load_image(image, to_rgb=True)
            quality_info = assess_image_quality(img_rgb) if check_quality else {}

            tensor = preprocess_for_model(
                img_rgb,
                model_name="efficientnetb3",
                target_size=self.input_size,
            )

            # Inference
            t_infer = time.perf_counter()
            raw_preds = self.model.predict(tensor, verbose=0)
            infer_duration_ms = (time.perf_counter() - t_infer) * 1000

            probabilities = raw_preds[0]
            top_indices = np.argsort(probabilities)[::-1][:top_k]

            top_predictions = []
            for idx in top_indices:
                cls_key = self.classes[idx]
                conf = float(probabilities[idx])
                details = self.disease_details.get(cls_key, {})

                crop = details.get("crop", cls_key.split("___")[0])
                disease = details.get("disease", cls_key.split("___")[1].replace("_", " "))
                is_healthy = details.get("is_healthy", "healthy" in cls_key.lower())

                top_predictions.append(
                    {
                        "class_index": int(idx),
                        "class_name": cls_key,
                        "crop": crop,
                        "disease": disease,
                        "is_healthy": is_healthy,
                        "confidence": round(conf, 4),
                        "confidence_percentage": round(conf * 100.0, 2),
                        "name_en": details.get("en", cls_key.replace("___", " - ")),
                        "name_mr": details.get("mr", ""),
                        "name_hi": details.get("hi", ""),
                        "symptoms": details.get("symptoms", ""),
                        "treatment": details.get("treatment", ""),
                    }
                )

            primary = top_predictions[0]
            total_duration_ms = (time.perf_counter() - start_time) * 1000

            models_list = [
                {"model_name": "EfficientNetB3 (Primary)", "prediction": primary["disease"], "confidence": primary["confidence"]}
            ]

            return {
                "status": "success",
                "model_available": True,
                "model_name": "EfficientNetB3",
                "predicted_class": primary["class_name"],
                "predicted_disease": primary["disease"],
                "disease": primary["disease"],
                "crop": primary["crop"],
                "crop_type": primary["crop"],
                "is_healthy": primary["is_healthy"],
                "confidence": primary["confidence"],
                "confidence_percentage": primary["confidence_percentage"],
                "multilingual": {
                    "en": primary["name_en"],
                    "mr": primary["name_mr"],
                    "hi": primary["name_hi"],
                },
                "treatment_recommendation": primary["treatment"],
                "symptoms": primary["symptoms"],
                "top_k_predictions": top_predictions,
                "model_version": "EfficientNetB3-v1.0",
                "ensemble_results": {
                    "models": models_list,
                    "consensus_agreement": primary["confidence"],
                    "voting_method": "Single-Model Fine-Tuned",
                },
                "quality_assessment": quality_info,
                "inference_time_ms": round(infer_duration_ms, 2),
                "total_processing_time_ms": round(total_duration_ms, 2),
            }

        except Exception as exc:
            logger.error("Error during disease inference: %s", exc, exc_info=True)
            return {
                "status": "error",
                "model_available": True,
                "predicted_disease": "Diagnosis Error",
                "crop_type": crop_hint or "Unknown",
                "confidence": 0.0,
                "model_version": "Error",
                "ensemble_results": {"models": [], "consensus_agreement": 0.0, "voting_method": "Error"},
                "error": str(exc),
                "inference_time_ms": round((time.perf_counter() - start_time) * 1000, 2),
            }
