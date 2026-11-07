import io
import logging
from typing import Optional
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, status
from PIL import Image

from app.schemas.diagnosis import EnsemblePredictionResponse, EnsembleModelScore
from app.ml.disease.classifier import DiseaseClassifier

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ensemble", tags=["Ensemble Classification"])


@router.post(
    "/predict",
    response_model=EnsemblePredictionResponse,
    summary="Run multi-model ensemble classification",
    description="Classifies crop diseases across multiple deep neural networks (EfficientNetB3, ResNet101V2, InceptionV3, VGG19) and calculates soft-voting agreement."
)
async def predict_ensemble(
    image: UploadFile = File(..., description="Crop leaf image (JPG/PNG)"),
    crop_type: Optional[str] = Form("Unknown", description="Crop hint"),
) -> EnsemblePredictionResponse:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid image.",
        )

    file_bytes = await image.read()
    try:
        pil_image = Image.open(io.BytesIO(file_bytes))
        pil_image.verify()
        pil_image = Image.open(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file.")

    classifier = DiseaseClassifier()
    result = classifier.predict(pil_image, crop_hint=crop_type or "Unknown")

    model_scores = [
        EnsembleModelScore(
            model_name=m["model_name"],
            prediction=m["prediction"],
            confidence=m["confidence"]
        )
        for m in result["ensemble_results"]["models"]
    ]

    return EnsemblePredictionResponse(
        predicted_disease=result["predicted_disease"],
        confidence=result["confidence"],
        crop_type=result["crop_type"],
        model_predictions=model_scores,
        agreement_score=result["ensemble_results"]["consensus_agreement"]
    )
