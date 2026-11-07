"""
Agrivision AI+ - Machine Learning Subsystem & Model Registry.

Tracks model loading status, handles lazy-loading, maintains model registries,
and exposes availability diagnostics for the FastAPI application.
"""

from __future__ import annotations

import enum
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("agrivision.ml")


class ModelStatus(str, enum.Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    WEIGHTS_MISSING = "weights_missing"
    LOAD_FAILED = "load_failed"
    NOT_INITIALIZED = "not_initialized"


@dataclass
class ModelInfo:
    name: str
    category: str
    status: ModelStatus = ModelStatus.NOT_INITIALIZED
    weights_path: Optional[str] = None
    input_shape: Optional[List[int]] = None
    classes_count: Optional[int] = None
    error_message: Optional[str] = None
    instance: Optional[Any] = field(default=None, repr=False)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MLModelRegistry:
    """
    Central registry for all AI/ML models in Agrivision AI+.
    Provides centralized tracking, fallback handling, and status reporting.
    """

    _instance: Optional["MLModelRegistry"] = None

    def __new__(cls) -> "MLModelRegistry":
        if cls._instance is None:
            cls._instance = super(MLModelRegistry, cls).__new__(cls)
            cls._instance._models: Dict[str, ModelInfo] = {}
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._register_known_models()
        self._initialized = True

    def _register_known_models(self) -> None:
        """Register placeholders for all system models."""
        self.register(
            name="disease_classifier",
            category="disease_classification",
            weights_path="ml/models/weights/efficientnetb3_disease.h5",
            input_shape=[300, 300, 3],
            classes_count=38,
            metadata={"architecture": "EfficientNetB3", "dataset": "PlantVillage"},
        )
        self.register(
            name="ensemble_vgg16",
            category="disease_classification",
            weights_path="ml/models/weights/vgg16_disease.h5",
            input_shape=[224, 224, 3],
            classes_count=38,
            metadata={"architecture": "VGG16", "weight": 0.2},
        )
        self.register(
            name="ensemble_vgg19",
            category="disease_classification",
            weights_path="ml/models/weights/vgg19_disease.h5",
            input_shape=[224, 224, 3],
            classes_count=38,
            metadata={"architecture": "VGG19", "weight": 0.2},
        )
        self.register(
            name="ensemble_inceptionv3",
            category="disease_classification",
            weights_path="ml/models/weights/inceptionv3_disease.h5",
            input_shape=[299, 299, 3],
            classes_count=38,
            metadata={"architecture": "InceptionV3", "weight": 0.3},
        )
        self.register(
            name="ensemble_resnet101v2",
            category="disease_classification",
            weights_path="ml/models/weights/resnet101v2_disease.h5",
            input_shape=[224, 224, 3],
            classes_count=38,
            metadata={"architecture": "ResNet101V2", "weight": 0.3},
        )
        self.register(
            name="pest_detector",
            category="pest_detection",
            weights_path="ml/models/weights/yolov8_pest.pt",
            metadata={"architecture": "YOLOv8", "framework": "PyTorch / Ultralytics"},
        )
        self.register(
            name="severity_estimator",
            category="severity_segmentation",
            weights_path="ml/models/weights/unet_severity.h5",
            input_shape=[256, 256, 3],
            classes_count=2,
            metadata={"architecture": "U-Net", "task": "leaf_lesion_segmentation"},
        )
        self.register(
            name="yield_predictor",
            category="yield_prediction",
            weights_path="ml/models/weights/xgboost_yield.joblib",
            metadata={"architecture": "XGBoost / RandomForest", "framework": "scikit-learn"},
        )

    def register(
        self,
        name: str,
        category: str,
        weights_path: Optional[str] = None,
        input_shape: Optional[List[int]] = None,
        classes_count: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._models[name] = ModelInfo(
            name=name,
            category=category,
            weights_path=weights_path,
            input_shape=input_shape,
            classes_count=classes_count,
            metadata=metadata or {},
        )

    def get_info(self, name: str) -> Optional[ModelInfo]:
        return self._models.get(name)

    def set_status(
        self,
        name: str,
        status: ModelStatus,
        instance: Optional[Any] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        if name in self._models:
            self._models[name].status = status
            if instance is not None:
                self._models[name].instance = instance
            if error_message is not None:
                self._models[name].error_message = error_message
            if metadata:
                self._models[name].metadata.update(metadata)

    def is_available(self, name: str) -> bool:
        info = self._models.get(name)
        return info is not None and info.status == ModelStatus.AVAILABLE

    def get_status_summary(self) -> Dict[str, Any]:
        """Return a structured summary of all registered models."""
        summary = {}
        for name, info in self._models.items():
            summary[name] = {
                "category": info.category,
                "status": info.status.value,
                "weights_path": info.weights_path,
                "weights_exist": Path(info.weights_path).is_file() if info.weights_path else False,
                "error": info.error_message,
                "metadata": info.metadata,
            }
        return summary


_registry = MLModelRegistry()


def get_model_registry() -> MLModelRegistry:
    """Return the global MLModelRegistry instance."""
    return _registry


def check_model_availability(model_name: str) -> bool:
    """Check if a specific model is loaded and ready for inference."""
    return _registry.is_available(model_name)


def load_all_models() -> Dict[str, bool]:
    """
    Central model loading function.
    Attempts to initialize and load weights for all registered models.

    Returns:
        Dict[str, bool]: Status of each model (True if loaded, False otherwise).
    """
    results: Dict[str, bool] = {}

    try:
        from backend.app.ml.disease.classifier import DiseaseClassifier
        dc = DiseaseClassifier(auto_load=True)
        results["disease_classifier"] = (dc.status == ModelStatus.AVAILABLE)
    except Exception as e:
        logger.warning("Failed to initialize DiseaseClassifier: %s", e)
        results["disease_classifier"] = False

    try:
        from backend.app.ml.disease.ensemble import EnsembleClassifier
        ens = EnsembleClassifier(auto_load=True)
        for m_name in ["VGG16", "VGG19", "InceptionV3", "ResNet101V2"]:
            results[f"ensemble_{m_name.lower()}"] = (ens.model_statuses.get(m_name) == ModelStatus.AVAILABLE)
    except Exception as e:
        logger.warning("Failed to initialize EnsembleClassifier: %s", e)
        for m_name in ["VGG16", "VGG19", "InceptionV3", "ResNet101V2"]:
            results[f"ensemble_{m_name.lower()}"] = False

    try:
        from backend.app.ml.pest.detector import PestDetector
        pd = PestDetector(auto_load=True)
        results["pest_detector"] = (pd.status == ModelStatus.AVAILABLE)
    except Exception as e:
        logger.warning("Failed to initialize PestDetector: %s", e)
        results["pest_detector"] = False

    try:
        from backend.app.ml.severity.estimator import SeverityEstimator
        se = SeverityEstimator(auto_load=True)
        results["severity_estimator"] = (se.status == ModelStatus.AVAILABLE)
    except Exception as e:
        logger.warning("Failed to initialize SeverityEstimator: %s", e)
        results["severity_estimator"] = False

    try:
        from backend.app.ml.yield_model.predictor import YieldPredictor
        yp = YieldPredictor(auto_load=True)
        results["yield_predictor"] = (yp.status == ModelStatus.AVAILABLE)
    except Exception as e:
        logger.warning("Failed to initialize YieldPredictor: %s", e)
        results["yield_predictor"] = False

    return results

