import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, Query, status

from app.services.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendations", tags=["Treatment Recommendations"])


@router.get(
    "/pest/{pest_id}",
    response_model=Dict[str, Any],
    summary="Get pest management recommendations",
    description="Retrieve chemical, biological, and organic control protocols for identified pests."
)
async def get_pest_recommendation(
    pest_id: str,
    language: Optional[str] = Query("en", description="Target language: en, mr, or hi")
) -> Dict[str, Any]:
    return RecommendationService.get_pest_recommendations(pest_name=pest_id, language=language or "en")


@router.get(
    "/{disease_id}",
    response_model=Dict[str, Any],
    summary="Get disease treatment recommendations",
    description="Retrieve multilingual chemical spray dosages, organic biocontrols, and cultural practices for a disease."
)
async def get_disease_recommendation(
    disease_id: str,
    language: Optional[str] = Query("en", description="Target language: en, mr, or hi")
) -> Dict[str, Any]:
    return RecommendationService.get_disease_recommendations(disease_name=disease_id, language=language or "en")
