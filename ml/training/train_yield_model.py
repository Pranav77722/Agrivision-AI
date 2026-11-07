"""
Training Script: Crop Yield Prediction Model for Agrivision AI+.

Trains XGBoost and Random Forest regressors on Indian district-level agricultural data.
Builds an end-to-end ColumnTransformer pipeline with one-hot encoding for categorical variables
(crop, district, season, soil_type, irrigation) and standard scaling for numerical features
(area, rainfall, temperature).

Features:
- crop, district, season, area, soil_type, irrigation, rainfall, temperature -> yield (Tonnes/Ha)

Evaluates:
- Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R² Score.
- Saves trained model pipelines with joblib.

Usage:
    python ml/training/train_yield_model.py --data ml/datasets/yield/indian_crop_yield_data.csv
    python ml/training/train_yield_model.py --generate-sample-data
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor

from ml.training.dataset_utils import generate_synthetic_yield_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_yield_model")

CATEGORICAL_COLS = ["crop", "district", "season", "soil_type", "irrigation"]
NUMERICAL_COLS = ["area", "rainfall", "temperature"]
TARGET_COL = "yield"


def build_preprocessor() -> ColumnTransformer:
    """Construct OneHot and Scaling preprocessor pipeline."""
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    numerical_transformer = StandardScaler()

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_transformer, CATEGORICAL_COLS),
            ("num", numerical_transformer, NUMERICAL_COLS),
        ]
    )
    return preprocessor


def train_and_evaluate(
    data_path: Path,
    output_xgb_path: Path,
    output_rf_path: Path,
) -> Dict[str, Any]:
    """Train XGBoost and Random Forest pipelines and persist weights."""
    if not data_path.is_file():
        logger.warning("Dataset not found at %s. Generating realistic synthetic agro-statistics...", data_path)
        data_path = generate_synthetic_yield_dataset(data_path, num_samples=6000)

    logger.info("Loading agricultural data from %s...", data_path)
    df = pd.read_csv(data_path)
    logger.info("Dataset shape: %s", df.shape)

    # Validate required columns
    required = set(CATEGORICAL_COLS + NUMERICAL_COLS + [TARGET_COL])
    if not required.issubset(set(df.columns)):
        missing = required - set(df.columns)
        raise ValueError(f"Dataset is missing required columns: {missing}")

    X = df[CATEGORICAL_COLS + NUMERICAL_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info("Train samples: %d, Test samples: %d", len(X_train), len(X_test))

    # --- 1. Train Random Forest Baseline ---
    logger.info("--- Training Random Forest Regressor ---")
    rf_pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("regressor", RandomForestRegressor(n_estimators=100, max_depth=16, random_state=42, n_jobs=-1)),
        ]
    )
    rf_pipeline.fit(X_train, y_train)
    rf_pred = rf_pipeline.predict(X_test)

    rf_mae = float(mean_absolute_error(y_test, rf_pred))
    rf_rmse = float(np.sqrt(mean_squared_error(y_test, rf_pred)))
    rf_r2 = float(r2_score(y_test, rf_pred))
    logger.info("Random Forest: MAE=%.3f, RMSE=%.3f, R²=%.3f", rf_mae, rf_rmse, rf_r2)

    # --- 2. Train XGBoost Primary Regressor ---
    logger.info("--- Training XGBoost Regressor ---")
    xgb_pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "regressor",
                XGBRegressor(
                    n_estimators=180,
                    learning_rate=0.08,
                    max_depth=6,
                    subsample=0.85,
                    colsample_bytree=0.85,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    xgb_pipeline.fit(X_train, y_train)
    xgb_pred = xgb_pipeline.predict(X_test)

    xgb_mae = float(mean_absolute_error(y_test, xgb_pred))
    xgb_rmse = float(np.sqrt(mean_squared_error(y_test, xgb_pred)))
    xgb_r2 = float(r2_score(y_test, xgb_pred))
    logger.info("XGBoost: MAE=%.3f, RMSE=%.3f, R²=%.3f", xgb_mae, xgb_rmse, xgb_r2)

    # 5-fold cross validation for XGBoost
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(xgb_pipeline, X, y, cv=cv, scoring="r2", n_jobs=-1)
    logger.info("XGBoost 5-Fold CV R²: %.3f ± %.3f", float(np.mean(cv_scores)), float(np.std(cv_scores)))

    # Persist model weights
    output_xgb_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(xgb_pipeline, str(output_xgb_path))
    logger.info("Saved trained XGBoost model to: %s", output_xgb_path)

    output_rf_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(rf_pipeline, str(output_rf_path))
    logger.info("Saved trained Random Forest model to: %s", output_rf_path)

    # Save metrics report
    metrics = {
        "xgboost": {
            "mae": round(xgb_mae, 4),
            "rmse": round(xgb_rmse, 4),
            "r2_score": round(xgb_r2, 4),
            "cv_r2_mean": round(float(np.mean(cv_scores)), 4),
            "cv_r2_std": round(float(np.std(cv_scores)), 4),
        },
        "random_forest": {
            "mae": round(rf_mae, 4),
            "rmse": round(rf_rmse, 4),
            "r2_score": round(rf_r2, 4),
        },
        "test_samples": len(y_test),
        "train_samples": len(y_train),
    }

    metrics_file = output_xgb_path.parent / "yield_model_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Crop Yield Prediction Regressors")
    parser.add_argument("--data", type=str, default="ml/datasets/yield/indian_crop_yield_data.csv")
    parser.add_argument("--xgb-out", type=str, default="ml/models/weights/xgboost_yield.joblib")
    parser.add_argument("--rf-out", type=str, default="ml/models/weights/rf_yield.joblib")
    parser.add_argument("--generate-sample-data", action="store_true")

    args = parser.parse_args()

    data_file = Path(args.data)
    if not data_file.is_absolute():
        data_file = PROJECT_ROOT / data_file

    if args.generate_sample_data:
        generate_synthetic_yield_dataset(data_file)

    xgb_out = Path(args.xgb_out)
    if not xgb_out.is_absolute():
        xgb_out = PROJECT_ROOT / xgb_out

    rf_out = Path(args.rf_out)
    if not rf_out.is_absolute():
        rf_out = PROJECT_ROOT / rf_out

    train_and_evaluate(data_file, xgb_out, rf_out)
