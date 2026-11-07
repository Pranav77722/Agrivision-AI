"""
CLI Inference Tool for Agrivision AI+.

Enables end-to-end testing and verification of all machine learning models:
- disease   : EfficientNetB3 primary disease classifier
- ensemble  : Multi-architecture ensemble classifier (VGG16, VGG19, InceptionV3, ResNet101V2)
- pest      : YOLOv8 / YOLO11 insect pest detector
- severity  : U-Net disease severity percentage & area estimator
- gradcam   : Visual attention explainability heatmap
- yield     : XGBoost / Random Forest crop yield predictor

Usage Examples:
    python ml/inference/predict.py --task disease --image path/to/leaf.jpg
    python ml/inference/predict.py --task ensemble --image path/to/leaf.jpg
    python ml/inference/predict.py --task pest --image path/to/field.jpg
    python ml/inference/predict.py --task severity --image path/to/leaf.jpg
    python ml/inference/predict.py --task gradcam --image path/to/leaf.jpg --output-dir ml/inference/output
    python ml/inference/predict.py --task yield --crop cotton --district Pune --area 2.5 --rainfall 750 --temp 28.5
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.ml.disease.classifier import DiseaseClassifier
from backend.app.ml.disease.ensemble import EnsembleClassifier
from backend.app.ml.explainability.gradcam import generate_gradcam
from backend.app.ml.pest.detector import PestDetector
from backend.app.ml.preprocessing import load_image
from backend.app.ml.severity.estimator import SeverityEstimator
from backend.app.ml.yield_model.predictor import YieldPredictor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("predict_cli")


def run_disease_inference(image_path: Path, top_k: int = 5) -> Dict[str, Any]:
    classifier = DiseaseClassifier(auto_load=True)
    return classifier.predict(image_path, top_k=top_k)


def run_ensemble_inference(image_path: Path, top_k: int = 5) -> Dict[str, Any]:
    ensemble = EnsembleClassifier(auto_load=True)
    return ensemble.predict(image_path, top_k=top_k)


def run_pest_inference(image_path: Path, conf: float = 0.25) -> Dict[str, Any]:
    detector = PestDetector(confidence_threshold=conf, auto_load=True)
    return detector.detect(image_path, conf_threshold=conf)


def run_severity_inference(image_path: Path) -> Dict[str, Any]:
    estimator = SeverityEstimator(auto_load=True)
    return estimator.segment(image_path)


def run_gradcam_inference(image_path: Path, output_dir: Optional[Path] = None) -> Dict[str, Any]:
    classifier = DiseaseClassifier(auto_load=True)
    if classifier.model is None:
        classifier.model = classifier.build_architecture(load_imagenet_backbone=True)

    result = generate_gradcam(classifier.model, image_path, model_name="efficientnetb3")
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        # Decode and save overlay image
        import base64

        if "overlay_image" in result and result["overlay_image"].startswith("data:image"):
            b64_data = result["overlay_image"].split(",")[1]
            out_img = output_dir / f"gradcam_overlay_{image_path.name}"
            with open(out_img, "wb") as f:
                f.write(base64.b64decode(b64_data))
            result["saved_overlay_path"] = str(out_img)

    return result


def run_yield_inference(payload: Dict[str, Any]) -> Dict[str, Any]:
    predictor = YieldPredictor(auto_load=True)
    return predictor.predict(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Agrivision AI+ Command-Line Inference Engine")
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        choices=["disease", "ensemble", "pest", "severity", "gradcam", "yield"],
        help="Model inference task",
    )
    parser.add_argument("--image", type=str, help="Path to input image file (for vision models)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of top candidates to return")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold for pest detection")
    parser.add_argument("--output-dir", type=str, default="ml/inference/output", help="Output directory for generated artifacts")
    parser.add_argument("--json", action="store_true", help="Print raw JSON response")

    # Yield prediction feature arguments
    parser.add_argument("--crop", type=str, default="cotton", help="Crop species")
    parser.add_argument("--district", type=str, default="Pune", help="District name")
    parser.add_argument("--season", type=str, default="Kharif", help="Growing season")
    parser.add_argument("--area", type=float, default=2.0, help="Cultivated area in hectares")
    parser.add_argument("--soil-type", type=str, default="black_soil", help="Soil type")
    parser.add_argument("--irrigation", type=str, default="drip", help="Irrigation system")
    parser.add_argument("--rainfall", type=float, default=750.0, help="Annual/Seasonal rainfall in mm")
    parser.add_argument("--temp", type=float, default=28.0, help="Mean temperature in Celsius")

    args = parser.parse_args()

    # Image requirement check
    if args.task in ["disease", "ensemble", "pest", "severity", "gradcam"]:
        if not args.image:
            logger.error("--image argument is required for task '%s'", args.task)
            sys.exit(1)
        img_p = Path(args.image)
        if not img_p.is_file():
            logger.error("Image file not found: %s", img_p)
            sys.exit(1)
    else:
        img_p = None

    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir

    result: Dict[str, Any] = {}

    if args.task == "disease":
        result = run_disease_inference(img_p, top_k=args.top_k)
    elif args.task == "ensemble":
        result = run_ensemble_inference(img_p, top_k=args.top_k)
    elif args.task == "pest":
        result = run_pest_inference(img_p, conf=args.conf)
    elif args.task == "severity":
        result = run_severity_inference(img_p)
    elif args.task == "gradcam":
        result = run_gradcam_inference(img_p, output_dir=out_dir)
    elif args.task == "yield":
        payload = {
            "crop": args.crop,
            "district": args.district,
            "season": args.season,
            "area": args.area,
            "soil_type": args.soil_type,
            "irrigation": args.irrigation,
            "rainfall": args.rainfall,
            "temperature": args.temp,
        }
        result = run_yield_inference(payload)

    if args.json:
        # Strip long base64 strings from raw stdout print for readability
        sanitized = {k: ("<base64_data_uri>" if isinstance(v, str) and v.startswith("data:image") else v) for k, v in result.items()}
        print(json.dumps(sanitized, indent=2))
    else:
        print("\n========================================================")
        print(f" Agrivision AI+ Inference Output: {args.task.upper()}")
        print("========================================================")
        for k, v in result.items():
            if isinstance(v, str) and v.startswith("data:image"):
                print(f"  {k}: [base64 image payload encoded]")
            elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                print(f"  {k}:")
                for item in v[:5]:
                    print(f"    - {item}")
            else:
                print(f"  {k}: {v}")
        print("========================================================\n")


if __name__ == "__main__":
    main()
