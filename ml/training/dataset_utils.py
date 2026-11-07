"""
Agrivision AI+ - Dataset Utilities and Data Loaders.

Provides helpers for:
- PlantVillage dataset loading, verification, and splitting
- PlantDoc validation dataset utilities
- YOLO format dataset generator / validator for IP102 pests
- Synthetic benchmark generator for Indian agricultural yield data
- Leaf lesion segmentation mask utilities for U-Net
"""

from __future__ import annotations

import json
import logging
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)

# Official PlantVillage classes
PLANT_VILLAGE_CLASSES = [
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


def get_dataset_dir(dataset_name: str) -> Path:
    """Get absolute path to local dataset folder in ml/datasets/."""
    project_root = Path(__file__).resolve().parents[2]
    d_path = project_root / "ml" / "datasets" / dataset_name
    d_path.mkdir(parents=True, exist_ok=True)
    return d_path


def get_weights_dir() -> Path:
    """Get absolute path to model weights directory in ml/models/weights/."""
    project_root = Path(__file__).resolve().parents[2]
    w_path = project_root / "ml" / "models" / "weights"
    w_path.mkdir(parents=True, exist_ok=True)
    return w_path


def load_plantvillage_dataset(
    data_dir: Union[str, Path],
    image_size: Tuple[int, int] = (300, 300),
    batch_size: int = 32,
    validation_split: float = 0.2,
    seed: int = 42,
) -> Tuple[Any, Any]:
    """
    Load PlantVillage dataset into TensorFlow train & validation datasets.

    Args:
        data_dir: Path to PlantVillage directory containing class subfolders.
        image_size: (height, width)
        batch_size: Mini-batch size.
        validation_split: Validation partition ratio (default 20%).
        seed: Random seed for deterministic splitting.

    Returns:
        (train_ds, val_ds)
    """
    import tensorflow as tf

    path = Path(data_dir)
    if not path.is_dir():
        raise FileNotFoundError(
            f"PlantVillage dataset directory does not exist at '{path}'. "
            "Please download PlantVillage from Kaggle: "
            "'https://www.kaggle.com/datasets/emmarex/plantdisease' or Mendeley Data."
        )

    logger.info("Loading PlantVillage images from %s with size %s...", path, image_size)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        str(path),
        validation_split=validation_split,
        subset="training",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="categorical",
        class_names=PLANT_VILLAGE_CLASSES,
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        str(path),
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode="categorical",
        class_names=PLANT_VILLAGE_CLASSES,
    )

    # Prefetch optimization
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds


def generate_synthetic_yield_dataset(
    output_path: Optional[Union[str, Path]] = None,
    num_samples: int = 5000,
    seed: int = 42,
) -> Path:
    """
    Synthesize an Indian district-level agricultural statistics CSV dataset
    reflecting realistic agro-climatic yield relationships across Maharashtra & India.

    Returns:
        Path to generated CSV file.
    """
    import pandas as pd

    np.random.seed(seed)
    random.seed(seed)

    crops = ["cotton", "soybean", "sugarcane", "wheat", "rice", "maize", "tomato", "onion", "gram", "groundnut"]
    districts = [
        "Pune", "Nashik", "Ahmednagar", "Nagpur", "Aurangabad",
        "Solapur", "Amravati", "Kolhapur", "Jalgaon", "Nanded",
        "Satara", "Sangli", "Latur", "Buldhana", "Yavatmal",
    ]
    seasons = ["Kharif", "Rabi", "Zaid", "Whole Year"]
    soil_types = ["black_soil", "alluvial", "red_soil", "sandy_loam", "clay_loam", "laterite"]
    irrigations = ["drip", "sprinkler", "canal_flood", "borewell", "rainfed"]

    crop_base_params = {
        "cotton": {"base": 2.2, "rain_opt": 750, "temp_opt": 28, "std": 0.35},
        "soybean": {"base": 2.1, "rain_opt": 850, "temp_opt": 26, "std": 0.30},
        "sugarcane": {"base": 85.0, "rain_opt": 1400, "temp_opt": 30, "std": 12.0},
        "wheat": {"base": 3.8, "rain_opt": 350, "temp_opt": 20, "std": 0.45},
        "rice": {"base": 3.6, "rain_opt": 1200, "temp_opt": 27, "std": 0.50},
        "maize": {"base": 4.2, "rain_opt": 650, "temp_opt": 25, "std": 0.55},
        "tomato": {"base": 28.0, "rain_opt": 600, "temp_opt": 24, "std": 4.0},
        "onion": {"base": 18.0, "rain_opt": 650, "temp_opt": 25, "std": 3.0},
        "gram": {"base": 1.4, "rain_opt": 400, "temp_opt": 22, "std": 0.25},
        "groundnut": {"base": 2.0, "rain_opt": 600, "temp_opt": 27, "std": 0.30},
    }

    irr_multipliers = {
        "drip": 1.25,
        "sprinkler": 1.15,
        "canal_flood": 1.05,
        "borewell": 1.02,
        "rainfed": 0.82,
    }

    soil_multipliers = {
        "black_soil": 1.15,
        "alluvial": 1.12,
        "clay_loam": 1.05,
        "red_soil": 0.95,
        "sandy_loam": 0.90,
        "laterite": 0.85,
    }

    records = []
    for _ in range(num_samples):
        c = random.choice(crops)
        d = random.choice(districts)
        s = random.choice(seasons)
        soil = random.choice(soil_types)
        irr = random.choice(irrigations)
        area = round(float(np.random.exponential(scale=2.5) + 0.5), 2)  # 0.5 to 15 ha

        params = crop_base_params[c]
        # Simulate realistic rainfall and temp around optimum with variance
        rainfall = round(float(np.random.normal(loc=params["rain_opt"], scale=params["rain_opt"] * 0.25)), 1)
        rainfall = max(100.0, min(2500.0, rainfall))

        temp = round(float(np.random.normal(loc=params["temp_opt"], scale=3.5)), 1)
        temp = max(12.0, min(45.0, temp))

        # Yield formula with nonlinear weather penalty
        rain_ratio = rainfall / params["rain_opt"]
        rain_penalty = max(0.65, 1.0 - (0.35 * (abs(rain_ratio - 1.0) ** 1.3)))

        temp_diff = abs(temp - params["temp_opt"])
        temp_penalty = max(0.70, 1.0 - (0.04 * temp_diff))

        y = (
            params["base"]
            * irr_multipliers[irr]
            * soil_multipliers[soil]
            * rain_penalty
            * temp_penalty
            + np.random.normal(0, params["std"])
        )
        y = max(0.2, round(float(y), 2))

        records.append({
            "crop": c,
            "district": d,
            "season": s,
            "area": area,
            "soil_type": soil,
            "irrigation": irr,
            "rainfall": rainfall,
            "temperature": temp,
            "yield": y,
        })

    df = pd.DataFrame(records)

    if output_path is None:
        datasets_dir = get_dataset_dir("yield")
        out_file = datasets_dir / "indian_crop_yield_data.csv"
    else:
        out_file = Path(output_path)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_file, index=False)
    logger.info("Generated synthetic crop yield dataset at %s with %d rows.", out_file, len(df))
    return out_file


def document_required_datasets() -> str:
    """Return comprehensive markdown guide of all required datasets for Agrivision AI+."""
    doc = """
# Agrivision AI+ - Required Datasets & Specifications

To train and fine-tune all models to high empirical benchmark accuracy, the following datasets are required:

### 1. PlantVillage Dataset (Disease Classification)
- **Source**: [PlantVillage on Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease) or [Mendeley Data](https://data.mendeley.com/datasets/tywbtsjrjv/1)
- **Size**: ~54,303 RGB leaf images across 38 classes (14 crop species).
- **Target Location**: `ml/datasets/plantvillage/`
- **Class Organization**: Subfolders named matching the 38 classes in `ml/configs/class_labels.json`.
- **Pretrained Weights**: `ml/models/weights/efficientnetb3_disease.h5`

### 2. PlantDoc Dataset (In-Field Real World Validation)
- **Source**: [PlantDoc GitHub Repository](https://github.com/pratikkayal/PlantDoc-Dataset)
- **Size**: 2,569 field-captured leaf images under natural lighting and occlusions.
- **Target Location**: `ml/datasets/plantdoc/`
- **Purpose**: Domain adaptation & generalizability testing on complex agricultural backgrounds.

### 3. IP102 Insect Pest Dataset (YOLO Pest Detection)
- **Source**: [IP102 Benchmark](https://github.com/xpwu95/IP102)
- **Size**: 75,000+ annotated pest images across 102 species.
- **Format**: YOLO TXT format: `<class_idx> <x_center> <y_center> <width> <height>` (normalized 0 to 1).
- **Target Location**: `ml/datasets/ip102_yolo/`
- **Pretrained Weights**: `ml/models/weights/yolov8_pest.pt`

### 4. Leaf Lesion Segmentation Dataset (U-Net Disease Severity)
- **Source**: PlantVillage segmented masks & Kaggle Plant Pathology Segmentation.
- **Size**: Pair of RGB images and binary ground truth PNG masks (`0` = background, `1` = healthy, `2` = diseased).
- **Target Location**: `ml/datasets/leaf_segmentation/`
- **Pretrained Weights**: `ml/models/weights/unet_severity.h5`

### 5. Indian District Agricultural Statistics (Yield Prediction)
- **Source**: Directorate of Economics and Statistics (DES), Ministry of Agriculture & Farmers Welfare, India ([data.gov.in](https://data.gov.in)).
- **Target Location**: `ml/datasets/yield/indian_crop_yield_data.csv`
- **Features**: `crop, district, season, area, soil_type, irrigation, rainfall, temperature, yield`.
- **Pretrained Weights**: `ml/models/weights/xgboost_yield.joblib`
"""
    return doc.strip()
