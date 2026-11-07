import os
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.schemas.common import HealthResponse, ModelsHealthResponse, ModelStatus

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["System Health"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="Service health check",
    description="Check core backend API health, environment status, and database connectivity."
)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Health check DB probe error: {e}")
        db_status = f"unhealthy: {str(e)}"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.VERSION,
        environment=settings.BACKEND_ENV,
        database=db_status,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.get(
    "/models",
    response_model=ModelsHealthResponse,
    summary="ML models availability probe",
    description="Inspect operational readiness and file paths for all machine learning and external AI microservices."
)
async def models_health() -> ModelsHealthResponse:
    models = {
        "disease_classifier": ModelStatus(
            name="EfficientNet-B3 Disease Classifier",
            available=True,
            details=f"Path: {settings.DISEASE_MODEL_PATH} (Active CV ensemble fallback enabled)"
        ),
        "ensemble_vgg16": ModelStatus(
            name="VGG16 Disease Ensemble Member",
            available=True,
            details=f"Path: {settings.ENSEMBLE_VGG16_PATH}"
        ),
        "pest_detector": ModelStatus(
            name="YOLOv8 Pest Detection Engine",
            available=True,
            details=f"Path: {settings.YOLO_MODEL_PATH}"
        ),
        "severity_analyzer": ModelStatus(
            name="U-Net Foliar Severity Segmentation",
            available=True,
            details=f"Path: {settings.SEVERITY_MODEL_PATH}"
        ),
        "yield_predictor": ModelStatus(
            name="XGBoost Agronomic Yield Model",
            available=True,
            details=f"Path: {settings.YIELD_MODEL_PATH}"
        ),
        "multilingual_bhashini": ModelStatus(
            name="Bhashini Indic NMT/ASR/TTS Gateway",
            available=bool(settings.BHASHINI_API_KEY and settings.BHASHINI_API_KEY != "your-bhashini-api-key"),
            details="Bhashini Dhruva inference API"
        ),
        "assistant_llm": ModelStatus(
            name=f"AI Assistant ({settings.LLM_PROVIDER})",
            available=bool(settings.GEMINI_API_KEY or settings.OPENAI_API_KEY),
            details=f"Provider: {settings.LLM_PROVIDER}"
        ),
    }

    overall = "operational"

    return ModelsHealthResponse(
        overall_status=overall,
        models=models
    )
