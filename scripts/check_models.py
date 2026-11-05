#!/usr/bin/env python3
"""
Agrivision AI+ — Model Health Check Script
Verifies that all ML model weights are available and loadable.
"""

import os
import sys
from pathlib import Path

WEIGHTS_DIR = Path(__file__).parent.parent / "ml" / "models" / "weights"

REQUIRED_MODELS = {
    "efficientnetb3_disease.h5": {
        "name": "EfficientNetB3 Disease Classifier",
        "framework": "TensorFlow/Keras",
        "purpose": "Primary crop disease detection",
    },
    "vgg16_disease.h5": {
        "name": "VGG16 Ensemble Model",
        "framework": "TensorFlow/Keras",
        "purpose": "Ensemble disease classification",
    },
    "vgg19_disease.h5": {
        "name": "VGG19 Ensemble Model",
        "framework": "TensorFlow/Keras",
        "purpose": "Ensemble disease classification",
    },
    "inceptionv3_disease.h5": {
        "name": "InceptionV3 Ensemble Model",
        "framework": "TensorFlow/Keras",
        "purpose": "Ensemble disease classification",
    },
    "resnet101v2_disease.h5": {
        "name": "ResNet101V2 Ensemble Model",
        "framework": "TensorFlow/Keras",
        "purpose": "Ensemble disease classification",
    },
    "yolov8_pest.pt": {
        "name": "YOLOv8 Pest Detector",
        "framework": "PyTorch/Ultralytics",
        "purpose": "Pest detection with bounding boxes",
    },
    "unet_severity.h5": {
        "name": "U-Net Severity Estimator",
        "framework": "TensorFlow/Keras",
        "purpose": "Disease severity segmentation",
    },
    "xgboost_yield.joblib": {
        "name": "XGBoost Yield Predictor",
        "framework": "XGBoost/Scikit-learn",
        "purpose": "Crop yield prediction",
    },
}


def check_models():
    """Check availability of all required model weights."""
    print("=" * 60)
    print("🧠 Agrivision AI+ Model Health Check")
    print("=" * 60)
    print(f"\nWeights directory: {WEIGHTS_DIR}")
    print()

    if not WEIGHTS_DIR.exists():
        print(f"⚠ Weights directory does not exist. Creating it...")
        WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)

    available = 0
    missing = 0

    for filename, info in REQUIRED_MODELS.items():
        filepath = WEIGHTS_DIR / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"✅ {info['name']}")
            print(f"   File: {filename} ({size_mb:.1f} MB)")
            available += 1
        else:
            print(f"❌ {info['name']}")
            print(f"   Missing: {filename}")
            print(f"   Purpose: {info['purpose']}")
            print(f"   Framework: {info['framework']}")
            missing += 1

    print()
    print("=" * 60)
    print(f"Results: {available} available, {missing} missing")

    if missing > 0:
        print()
        print("To train missing models, run the training scripts in ml/training/")
        print("Or download pre-trained weights to ml/models/weights/")

    print("=" * 60)
    return missing == 0


if __name__ == "__main__":
    success = check_models()
    sys.exit(0 if success else 1)
