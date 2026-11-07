"""
Disease Severity Estimation via U-Net Semantic Segmentation for Agrivision AI+.

Segments crop leaves into healthy tissue and diseased lesion areas, calculating
exact surface damage percentages and categorizing severity into clinical bands:
- Healthy: 0% - 5%
- Mild: 5% - 20%
- Moderate: 20% - 40%
- Severe: 40% - 60%
- Critical: > 60%
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import cv2
import numpy as np

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
        encode_image_base64,
        load_image,
        preprocess_for_model,
    )
except ImportError:
    from app.ml import ModelStatus, get_model_registry
    from app.ml.preprocessing import (
        assess_image_quality,
        encode_image_base64,
        load_image,
        preprocess_for_model,
    )

logger = logging.getLogger(__name__)


def build_unet_model(
    input_size: Tuple[int, int] = (256, 256),
    num_classes: int = 2,
) -> Any:
    """
    Build U-Net segmentation architecture using TensorFlow/Keras.

    Args:
        input_size: (height, width)
        num_classes: Number of output channels (2 for healthy vs diseased).

    Returns:
        tf.keras.Model: Compiled or ready-to-train U-Net model.
    """
    import tensorflow as tf
    from tensorflow.keras import layers, models

    inputs = layers.Input(shape=(input_size[0], input_size[1], 3), name="leaf_image_input")

    # Encoder (Contracting Path)
    # Block 1
    c1 = layers.Conv2D(32, (3, 3), activation="relu", padding="same", name="enc_c1_1")(inputs)
    c1 = layers.BatchNormalization()(c1)
    c1 = layers.Conv2D(32, (3, 3), activation="relu", padding="same", name="enc_c1_2")(c1)
    c1 = layers.BatchNormalization()(c1)
    p1 = layers.MaxPooling2D((2, 2), name="pool1")(c1)

    # Block 2
    c2 = layers.Conv2D(64, (3, 3), activation="relu", padding="same", name="enc_c2_1")(p1)
    c2 = layers.BatchNormalization()(c2)
    c2 = layers.Conv2D(64, (3, 3), activation="relu", padding="same", name="enc_c2_2")(c2)
    c2 = layers.BatchNormalization()(c2)
    p2 = layers.MaxPooling2D((2, 2), name="pool2")(c2)

    # Block 3
    c3 = layers.Conv2D(128, (3, 3), activation="relu", padding="same", name="enc_c3_1")(p2)
    c3 = layers.BatchNormalization()(c3)
    c3 = layers.Conv2D(128, (3, 3), activation="relu", padding="same", name="enc_c3_2")(c3)
    c3 = layers.BatchNormalization()(c3)
    p3 = layers.MaxPooling2D((2, 2), name="pool3")(c3)

    # Block 4
    c4 = layers.Conv2D(256, (3, 3), activation="relu", padding="same", name="enc_c4_1")(p3)
    c4 = layers.BatchNormalization()(c4)
    c4 = layers.Conv2D(256, (3, 3), activation="relu", padding="same", name="enc_c4_2")(c4)
    c4 = layers.BatchNormalization()(c4)
    p4 = layers.MaxPooling2D((2, 2), name="pool4")(c4)

    # Bottleneck
    bn = layers.Conv2D(512, (3, 3), activation="relu", padding="same", name="bottleneck_1")(p4)
    bn = layers.BatchNormalization()(bn)
    bn = layers.Conv2D(512, (3, 3), activation="relu", padding="same", name="bottleneck_2")(bn)
    bn = layers.BatchNormalization()(bn)

    # Decoder (Expansive Path)
    # UpBlock 4
    u4 = layers.Conv2DTranspose(256, (2, 2), strides=(2, 2), padding="same", name="up4")(bn)
    u4 = layers.concatenate([u4, c4], name="concat4")
    c5 = layers.Conv2D(256, (3, 3), activation="relu", padding="same", name="dec_c5_1")(u4)
    c5 = layers.Conv2D(256, (3, 3), activation="relu", padding="same", name="dec_c5_2")(c5)

    # UpBlock 3
    u3 = layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding="same", name="up3")(c5)
    u3 = layers.concatenate([u3, c3], name="concat3")
    c6 = layers.Conv2D(128, (3, 3), activation="relu", padding="same", name="dec_c6_1")(u3)
    c6 = layers.Conv2D(128, (3, 3), activation="relu", padding="same", name="dec_c6_2")(c6)

    # UpBlock 2
    u2 = layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding="same", name="up2")(c6)
    u2 = layers.concatenate([u2, c2], name="concat2")
    c7 = layers.Conv2D(64, (3, 3), activation="relu", padding="same", name="dec_c7_1")(u2)
    c7 = layers.Conv2D(64, (3, 3), activation="relu", padding="same", name="dec_c7_2")(c7)

    # UpBlock 1
    u1 = layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding="same", name="up1")(c7)
    u1 = layers.concatenate([u1, c1], name="concat1")
    c8 = layers.Conv2D(32, (3, 3), activation="relu", padding="same", name="dec_c8_1")(u1)
    c8 = layers.Conv2D(32, (3, 3), activation="relu", padding="same", name="dec_c8_2")(c8)

    # Output head
    if num_classes == 1:
        outputs = layers.Conv2D(1, (1, 1), activation="sigmoid", name="lesion_mask")(c8)
    else:
        outputs = layers.Conv2D(num_classes, (1, 1), activation="softmax", name="severity_segmentation")(c8)

    model = models.Model(inputs=inputs, outputs=outputs, name="Agrivision_UNet_Severity")
    return model


class SeverityEstimator:
    """
    Leaf lesion and disease severity estimation engine.
    """

    def __init__(
        self,
        weights_path: Optional[Union[str, Path]] = None,
        input_size: Tuple[int, int] = (256, 256),
        auto_load: bool = True,
    ) -> None:
        self.input_size = input_size
        project_root = Path(__file__).resolve().parents[4]
        self.weights_path = Path(
            weights_path
            or os.environ.get("SEVERITY_MODEL_WEIGHTS", "ml/models/weights/unet_severity.h5")
        )
        if not self.weights_path.is_absolute():
            self.weights_path = project_root / self.weights_path

        self.model: Optional[Any] = None
        self.status: ModelStatus = ModelStatus.NOT_INITIALIZED
        self.registry = get_model_registry()

        if auto_load:
            self.load()

    def load(self) -> bool:
        """Load U-Net weights from disk."""
        t0 = time.perf_counter()
        if not self.weights_path.is_file():
            self.status = ModelStatus.WEIGHTS_MISSING
            self.registry.set_status(
                "severity_estimator",
                ModelStatus.WEIGHTS_MISSING,
                error_message=f"Weights missing at {self.weights_path}",
            )
            logger.info("Severity U-Net weights missing at %s", self.weights_path)
            return False

        try:
            import tensorflow as tf

            logger.info("Loading U-Net severity model from %s...", self.weights_path)
            try:
                self.model = tf.keras.models.load_model(str(self.weights_path), compile=False)
            except Exception:
                self.model = build_unet_model(self.input_size, num_classes=2)
                self.model.load_weights(str(self.weights_path))

            self.status = ModelStatus.AVAILABLE
            self.registry.set_status("severity_estimator", ModelStatus.AVAILABLE, instance=self.model)
            logger.info("U-Net model loaded in %.2f ms", (time.perf_counter() - t0) * 1000)
            return True
        except Exception as e:
            self.status = ModelStatus.LOAD_FAILED
            self.registry.set_status("severity_estimator", ModelStatus.LOAD_FAILED, error_message=str(e))
            logger.error("Failed to load U-Net severity model: %s", e, exc_info=True)
            return False

    @staticmethod
    def categorize_severity(percentage: float) -> Tuple[str, str, str]:
        """
        Map severity damage percentage into clinical categories.

        Returns:
            (category_en, category_mr, category_hi)
        """
        if percentage <= 5.0:
            return ("Healthy", "निरोगी (अत्यल्प बाधा)", "स्वस्थ / नगण्य")
        elif percentage <= 20.0:
            return ("Mild", "सौम्य प्रादुर्भाव", "हल्का संक्रमण")
        elif percentage <= 40.0:
            return ("Moderate", "मध्यम प्रादुर्भाव", "मध्यम संक्रमण")
        elif percentage <= 60.0:
            return ("Severe", "तीव्र प्रादुर्भाव", "गंभीर संक्रमण")
        else:
            return ("Critical", "अति-गंभीर प्रादुर्भाव (तात्काळ उपाय आवश्यक)", "अति गंभीर / विनाशकारी")

    def segment(
        self,
        image_input: Union[str, Path, bytes, np.ndarray],
        threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Perform semantic segmentation and severity area calculation.

        Args:
            image_input: Leaf image input.
            threshold: Probability threshold for lesion classification.

        Returns:
            Dict containing severity percentage, category, healthy/diseased areas,
            and base64-encoded color-coded overlay image.
        """
        t0 = time.perf_counter()

        if self.status != ModelStatus.AVAILABLE or self.model is None:
            return {
                "status": "model_unavailable",
                "model_available": False,
                "model_name": "UNet_Severity",
                "weights_path": str(self.weights_path),
                "error": "Model weights are not available on this server.",
                "message": (
                    "Severity U-Net model weights not found. Please train weights using "
                    f"'python ml/training/train_severity_model.py' and place at '{self.weights_path}'"
                ),
                "severity_percentage": 0.0,
                "severity_category": "Unknown",
                "inference_time_ms": round((time.perf_counter() - t0) * 1000, 2),
            }

        try:
            img_rgb = load_image(image_input, to_rgb=True)
            orig_h, orig_w = img_rgb.shape[:2]

            tensor = preprocess_for_model(
                img_rgb,
                model_name="unet",
                target_size=self.input_size,
            )

            t_infer = time.perf_counter()
            pred_mask = self.model.predict(tensor, verbose=0)[0]
            infer_duration = (time.perf_counter() - t_infer) * 1000

            # Determine whether model outputs 1 or 2 channels
            if pred_mask.shape[-1] == 2:
                # Channel 0: Healthy tissue, Channel 1: Diseased lesion
                healthy_prob = pred_mask[..., 0]
                diseased_prob = pred_mask[..., 1]
                diseased_mask_256 = (diseased_prob > threshold).astype(np.uint8)
                healthy_mask_256 = ((healthy_prob > threshold) & (diseased_mask_256 == 0)).astype(np.uint8)
            else:
                # 1 channel lesion mask
                lesion_prob = pred_mask[..., 0]
                diseased_mask_256 = (lesion_prob > threshold).astype(np.uint8)
                healthy_mask_256 = (lesion_prob <= threshold).astype(np.uint8)

            # Resize masks back to original resolution
            diseased_mask = cv2.resize(
                diseased_mask_256, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST
            )
            healthy_mask = cv2.resize(
                healthy_mask_256, (orig_w, orig_h), interpolation=cv2.INTER_NEAREST
            )

            # Exclude non-leaf background (simple Otsu/HSV leaf foreground mask)
            hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
            leaf_mask = cv2.inRange(hsv, (20, 25, 25), (160, 255, 255))
            if np.sum(leaf_mask > 0) > (orig_w * orig_h * 0.05):
                # Apply leaf mask to eliminate false background lesions
                diseased_mask = cv2.bitwise_and(diseased_mask, diseased_mask, mask=leaf_mask)
                healthy_mask = cv2.bitwise_and(healthy_mask, healthy_mask, mask=leaf_mask)

            diseased_pixel_count = int(np.sum(diseased_mask > 0))
            healthy_pixel_count = int(np.sum(healthy_mask > 0))
            total_leaf_pixels = healthy_pixel_count + diseased_pixel_count

            if total_leaf_pixels > 0:
                severity_percentage = round((diseased_pixel_count / total_leaf_pixels) * 100.0, 2)
                healthy_percentage = round((healthy_pixel_count / total_leaf_pixels) * 100.0, 2)
            else:
                severity_percentage = 0.0
                healthy_percentage = 100.0

            cat_en, cat_mr, cat_hi = self.categorize_severity(severity_percentage)

            # Build color-coded overlay: Green = healthy, Red = diseased
            overlay = img_rgb.copy()
            # Green tint for healthy leaf tissue
            overlay[healthy_mask > 0] = (
                0.65 * overlay[healthy_mask > 0] + 0.35 * np.array([34, 197, 94])
            ).astype(np.uint8)
            # Red tint for diseased lesion areas
            overlay[diseased_mask > 0] = (
                0.45 * overlay[diseased_mask > 0] + 0.55 * np.array([239, 68, 68])
            ).astype(np.uint8)

            overlay_b64 = encode_image_base64(overlay, format_ext=".jpg")
            total_duration = (time.perf_counter() - t0) * 1000

            return {
                "status": "success",
                "model_available": True,
                "model_name": "UNet_Severity",
                "severity_percentage": severity_percentage,
                "healthy_percentage": healthy_percentage,
                "healthy_area_pixels": healthy_pixel_count,
                "diseased_area_pixels": diseased_pixel_count,
                "total_leaf_pixels": total_leaf_pixels,
                "severity_category": cat_en,
                "severity_category_multilingual": {
                    "en": cat_en,
                    "mr": cat_mr,
                    "hi": cat_hi,
                },
                "overlay_image": overlay_b64,
                "color_legend": {
                    "healthy_tissue": "Green (#22c55e)",
                    "diseased_lesion": "Red (#ef4444)",
                },
                "inference_time_ms": round(infer_duration, 2),
                "total_processing_time_ms": round(total_duration, 2),
            }

        except Exception as exc:
            logger.error("Error during severity estimation: %s", exc, exc_info=True)
            return {
                "status": "error",
                "model_available": True,
                "error": str(exc),
                "inference_time_ms": round((time.perf_counter() - t0) * 1000, 2),
            }
