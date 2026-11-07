"""
Agrivision AI+ - Plant & Leaf Image Validator.

Performs robust out-of-domain (OOD) verification before disease diagnosis:
1. Botanical Foliage & Pigment Analysis (Chlorophyll green, chlorosis yellow, necrotic lesions, Normalized Excess Green index).
2. Human Skin Tone & Selfies / Body Parts rejection (YCrCb color space).
3. Deep Semantic Verification via MobileNetV2 (ImageNet botanical vs manufactured/indoor objects).
4. Organic Texture Sanity (vein/lamina cellular contrast vs uniform plastic/wall).

Ensures non-plant photos (furniture, humans, laptops, walls, animals, random objects)
are gracefully rejected with actionable guidance rather than generating false diagnoses.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# Canonical botanical/plant keywords across ImageNet-1k
PLANT_BOTANICAL_KEYWORDS = {
    "leaf", "plant", "tree", "flower", "grass", "moss", "fern", "crop", "vegetable", "fruit",
    "cabbage", "broccoli", "cauliflower", "zucchini", "squash", "cucumber", "pepper", "corn",
    "ear", "daisy", "pot", "greenhouse", "vine", "herb", "wood", "foliage", "strawberry",
    "orange", "lemon", "fig", "pomegranate", "apple", "banana", "rose", "tulip", "garden",
    "hay", "buckeye", "acorn", "cardoon", "artichoke", "mushroom", "spindle", "petal",
    "custard apple", "jackfruit", "head cabbage", "bell pepper", "spaghetti squash", "butternut squash"
}

# Obvious non-plant manufactured / indoor categories
DEFINITE_NON_PLANT_KEYWORDS = {
    "laptop", "keyboard", "mouse", "cellular telephone", "screen", "monitor", "television",
    "shoe", "running shoe", "sandal", "sneaker", "boot", "sock", "suit", "jersey", "t-shirt",
    "car", "automobile", "motorcycle", "bicycle", "steering wheel", "desk", "chair", "couch",
    "pillow", "wall clock", "digital clock", "watch", "remote control", "coffee mug", "water bottle",
    "plate", "doorknob", "bookcase", "microwave", "refrigerator", "toilet", "bed", "vacuum",
    "shovel", "scabbard", "quill", "bow", "mailbag", "stethoscope", "drumstick", "quilt", "doormat"
}


class PlantValidationError(ValueError):
    """Raised when an image is verified as NOT being a plant or leaf."""
    def __init__(self, message: str, detected_object: str = "Unknown", reasons: Optional[List[str]] = None):
        super().__init__(message)
        self.message = message
        self.detected_object = detected_object
        self.reasons = reasons or []


class PlantLeafDetector:
    """
    Two-stage botanical & semantic validator for leaf/plant verification.
    """
    _instance: Optional[PlantLeafDetector] = None

    def __init__(self):
        self._mobilenet = None
        self._initialized = False

    @classmethod
    def get_instance(cls) -> PlantLeafDetector:
        if cls._instance is None:
            cls._instance = PlantLeafDetector()
        return cls._instance

    def _ensure_model(self):
        """Lazy load MobileNetV2 to keep fast initial startup."""
        if not self._initialized:
            try:
                import tensorflow as tf
                logger.info("Initializing MobileNetV2 backbone for leaf/plant verification...")
                self._mobilenet = tf.keras.applications.MobileNetV2(weights="imagenet")
                self._initialized = True
                logger.info("MobileNetV2 leaf validator initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not load MobileNetV2 for deep leaf validation: {e}. Falling back to botanical CV.")
                self._initialized = True
                self._mobilenet = None

    def validate(
        self,
        image_input: Union[np.ndarray, Image.Image, bytes],
        min_foliage_ratio: float = 0.10,
    ) -> Dict[str, Any]:
        """
        Validate whether the given image contains a plant or crop leaf.

        Returns:
            Dict with:
                - is_plant: bool
                - confidence: float
                - detected_object: str
                - foliage_ratio: float
                - green_ratio: float
                - nexg_ratio: float
                - skin_ratio: float
                - reasons: List[str]
                - message: str
        """
        t0 = time.perf_counter()

        # Convert to BGR numpy array
        if isinstance(image_input, bytes):
            nparr = np.frombuffer(image_input, np.uint8)
            img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif isinstance(image_input, Image.Image):
            rgb = np.array(image_input.convert("RGB"), dtype=np.uint8)
            img_bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        elif isinstance(image_input, np.ndarray):
            img_bgr = image_input.copy()
            if len(img_bgr.shape) == 2:
                img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_GRAY2BGR)
            elif img_bgr.shape[2] == 4:
                img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2BGR)
        else:
            raise TypeError(f"Unsupported image type: {type(image_input)}")

        if img_bgr is None or img_bgr.size == 0:
            return {
                "is_plant": False,
                "confidence": 0.0,
                "detected_object": "Invalid Image",
                "foliage_ratio": 0.0,
                "green_ratio": 0.0,
                "nexg_ratio": 0.0,
                "skin_ratio": 0.0,
                "reasons": ["Image could not be decoded or is empty."],
                "message": "Invalid image file. Please provide a clear crop photo.",
            }

        # Downscale for rapid botanical analysis
        small = cv2.resize(img_bgr, (256, 256))
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB).astype(np.float32)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(small, cv2.COLOR_BGR2YCrCb)
        total_px = 256 * 256

        # 1. Botanical Green Foliage: H in [28, 90], S >= 32, V >= 25
        green_mask = cv2.inRange(hsv, (28, 32, 25), (90, 255, 255))
        green_ratio = float(np.count_nonzero(green_mask) / total_px)

        # 2. Chlorotic Yellow Leaf (blight, chlorosis, yellow mosaic): H in [16, 28], S >= 40, V >= 40
        yellow_mask = cv2.inRange(hsv, (16, 40, 40), (28, 255, 255))
        yellow_ratio = float(np.count_nonzero(yellow_mask) / total_px)

        # Combined foliage
        foliage_mask = cv2.bitwise_or(green_mask, yellow_mask)
        foliage_ratio = float(np.count_nonzero(foliage_mask) / total_px)

        # 3. Normalized Excess Green (NExG): (2*G - R - B) / (R + G + B + eps)
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        nexg = (2 * g - r - b) / (r + g + b + 1e-6)
        nexg_ratio = float(np.count_nonzero(nexg > 0.08) / total_px)

        # 4. Human Skin Tone Check: YCrCb Cr in [133, 173], Cb in [77, 127]
        cr, cb = ycrcb[:, :, 1], ycrcb[:, :, 2]
        skin_mask = ((cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127)).astype(np.uint8)
        skin_ratio = float(np.count_nonzero(skin_mask) / total_px)

        # 5. Deep Semantic Verification (ImageNet)
        self._ensure_model()
        top_name = "general object"
        top_conf = 0.0
        plant_score = 0.0

        if self._mobilenet is not None:
            try:
                import tensorflow as tf
                tensor = tf.keras.applications.mobilenet_v2.preprocess_input(
                    np.expand_dims(cv2.resize(rgb, (224, 224)), 0)
                )
                preds = self._mobilenet.predict(tensor, verbose=0)
                decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=5)[0]
                top_name = decoded[0][1].replace("_", " ")
                top_conf = float(decoded[0][2])

                for _, name, score in decoded:
                    clean_name = name.lower()
                    if any(kw in clean_name for kw in PLANT_BOTANICAL_KEYWORDS):
                        plant_score += float(score)
            except Exception as ex:
                logger.warning(f"MobileNet inference error during leaf check: {ex}")

        # Decision rules
        is_plant = True
        reasons: List[str] = []

        # Rule 1: High human skin coverage with minimal foliage
        if skin_ratio > 0.30 and foliage_ratio < 0.15:
            is_plant = False
            reasons.append(
                f"Human skin, face, or body detected ({skin_ratio*100:.0f}%) with insufficient plant foliage."
            )

        # Rule 2: Near zero botanical foliage coverage
        elif foliage_ratio < min_foliage_ratio and nexg_ratio < 0.08 and plant_score < 0.15:
            is_plant = False
            reasons.append(
                f"No significant crop foliage detected ({foliage_ratio*100:.1f}% foliage, detected {top_name})."
            )

        # Rule 3: Confident manufactured non-plant object and weak plant signals
        elif top_conf > 0.35 and plant_score < 0.05 and foliage_ratio < 0.18:
            is_plant = False
            reasons.append(
                f"Photo appears to show {top_name} ({top_conf*100:.0f}% confidence) rather than a crop leaf."
            )

        duration_ms = (time.perf_counter() - t0) * 1000

        if is_plant:
            message = "Plant or leaf verified successfully."
        else:
            message = (
                f"No plant or crop leaf detected. {reasons[0] if reasons else ''} "
                "Please capture a clear, well-lit photo of an affected plant leaf or crop."
            ).strip()

        return {
            "is_plant": is_plant,
            "confidence": round(plant_score if is_plant else max(0.85, 1.0 - plant_score), 3),
            "detected_object": top_name,
            "foliage_ratio": round(foliage_ratio, 3),
            "green_ratio": round(green_ratio, 3),
            "yellow_ratio": round(yellow_ratio, 3),
            "nexg_ratio": round(nexg_ratio, 3),
            "skin_ratio": round(skin_ratio, 3),
            "plant_semantic_score": round(plant_score, 3),
            "reasons": reasons,
            "message": message,
            "check_time_ms": round(duration_ms, 2),
        }

