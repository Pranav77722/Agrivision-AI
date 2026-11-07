import uuid
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, Query, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_optional, get_current_user
from app.models.user import User
from app.repositories.diagnosis_repo import DiagnosisRepository
from app.schemas.diagnosis import DiagnosisResponse, DiagnosisListResponse
from app.schemas.common import StatusResponse
from app.services.diagnosis_service import DiagnosisService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/diagnosis", tags=["Disease Diagnosis"])


@router.post(
    "/",
    response_model=DiagnosisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze crop image for diseases and pests",
    description="Upload an image of an affected leaf/plant to run ensemble disease classification, severity analysis, pest detection, and generate treatment recommendations."
)
@router.post(
    "/predict",
    response_model=DiagnosisResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
async def create_diagnosis(
    image: UploadFile = File(..., description="Crop leaf image (JPG/PNG)"),
    crop_type: Optional[str] = Form("Unknown", description="Optional crop hint (e.g. Tomato, Rice, Wheat, Cotton)"),
    language: Optional[str] = Form("en", description="Target language: en, mr, or hi"),
    cloud_image_url: Optional[str] = Form(None, description="Optional pre-uploaded Cloudinary URL"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
) -> DiagnosisResponse:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid image (JPEG/PNG).",
        )

    file_bytes = await image.read()
    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded image file is empty.",
        )

    user_id = current_user.id if current_user else None
    user_lang = current_user.preferred_language if (current_user and language == "en") else (language or "en")

    service = DiagnosisService(db)
    try:
        diagnosis = await service.run_full_diagnosis(
            image_bytes=file_bytes,
            filename=image.filename or "crop_leaf.jpg",
            user_id=user_id,
            crop_type=crop_type,
            language=user_lang,
            cloud_image_url=cloud_image_url,
        )
        return DiagnosisResponse.model_validate(diagnosis)
    except Exception as e:
        from app.ml.disease.leaf_detector import PlantValidationError
        if isinstance(e, PlantValidationError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error_code": "NOT_A_PLANT",
                    "is_plant": False,
                    "message": e.message,
                    "detected_object": e.detected_object,
                    "reasons": e.reasons,
                }
            )
        if isinstance(e, ValueError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        logger.error(f"Error during diagnosis execution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the crop diagnostic image.",
        )


@router.post(
    "/validate-image",
    summary="Validate if image is a real plant or crop leaf",
    description="Quickly checks botanical foliage, chlorophyll, chlorosis, and semantic features before full diagnosis."
)
async def validate_crop_image(
    image: UploadFile = File(..., description="Crop leaf image (JPG/PNG)"),
    db: AsyncSession = Depends(get_db)
):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a valid image.",
        )
    file_bytes = await image.read()
    service = DiagnosisService(db)
    result = service.check_is_plant(file_bytes)
    return result


@router.post(
    "/save-to-firestore",
    summary="Save diagnosis to Firebase Firestore",
    description="Save Cloudinary image URL and full model analysis to Firestore collection 'diagnoses'."
)
async def save_diagnosis_to_firestore(payload: Dict[str, Any] = Body(...)):
    from app.services.firestore_service import FirestoreService
    success = FirestoreService.save_diagnosis(payload)
    return {"success": success, "message": "Saved to Firestore successfully" if success else "Failed to save to Firestore"}


@router.get(
    "/",
    response_model=DiagnosisListResponse,
    summary="List past diagnoses",
    description="Retrieve paginated history of plant disease analyses performed by the farmer."
)
async def list_diagnoses(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
    crop_type: Optional[str] = Query(None, description="Filter by crop name"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> DiagnosisListResponse:
    repo = DiagnosisRepository(db)
    items, total = await repo.list_for_user(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        crop_type=crop_type,
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    return DiagnosisListResponse(
        items=[DiagnosisResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{id}",
    response_model=DiagnosisResponse,
    summary="Get diagnosis details",
    description="Retrieve detailed results, recommendations, severity metrics, and Grad-CAM visualization for a specific diagnosis."
)
async def get_diagnosis(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> DiagnosisResponse:
    repo = DiagnosisRepository(db)
    diagnosis = await repo.get(id)
    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis record not found.",
        )
    return DiagnosisResponse.model_validate(diagnosis)


@router.delete(
    "/{id}",
    response_model=StatusResponse,
    summary="Delete diagnosis record",
    description="Delete a diagnosis record."
)
async def delete_diagnosis(
    id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> StatusResponse:
    repo = DiagnosisRepository(db)
    diagnosis = await repo.get(id)
    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis record not found.",
        )
    if diagnosis.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this diagnosis.",
        )

    await repo.delete(id)
    return StatusResponse(success=True, message="Diagnosis record deleted successfully.")
