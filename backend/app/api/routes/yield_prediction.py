import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_optional, get_current_user
from app.models.user import User
from app.repositories.yield_repo import YieldRepository
from app.schemas.yield_prediction import YieldInput, YieldResponse, YieldHistoryResponse
from app.ml.yield_model.predictor import YieldPredictor

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/yield", tags=["Yield Prediction"])


@router.post(
    "/predict",
    response_model=YieldResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict crop harvest yield",
    description="Calculate expected yield in kg/hectare and total tonnage based on soil type, acreage, district climate, and irrigation parameters."
)
async def predict_yield(
    input_data: YieldInput,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> YieldResponse:
    predictor = YieldPredictor()
    pred_res = predictor.predict(input_data)

    user_id = current_user.id if current_user else None

    # Persist prediction in DB
    repo = YieldRepository(db)
    record = await repo.create(
        user_id=user_id,
        crop=pred_res["crop"],
        district=pred_res["district"],
        season=pred_res["season"],
        area_hectares=pred_res["area_hectares"],
        soil_type=pred_res["soil_type"],
        irrigation=pred_res["irrigation"],
        predicted_yield_kg_per_hectare=pred_res["predicted_yield_kg_per_hectare"],
        predicted_total_production_kg=pred_res["predicted_total_production_kg"],
        prediction_range_low=pred_res["prediction_range_low"],
        prediction_range_high=pred_res["prediction_range_high"],
        risk_factors=pred_res["risk_factors"],
        influencing_factors=pred_res["influencing_factors"]
    )

    return YieldResponse.model_validate(record)


@router.get(
    "/history",
    response_model=YieldHistoryResponse,
    summary="Get user yield prediction history",
    description="Retrieve past yield projections made by the current user."
)
async def get_yield_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    crop: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> YieldHistoryResponse:
    repo = YieldRepository(db)
    items, total = await repo.list_for_user(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        crop=crop
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return YieldHistoryResponse(
        items=[YieldResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
