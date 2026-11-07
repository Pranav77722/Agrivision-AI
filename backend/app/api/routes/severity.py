import io
import uuid
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from PIL import Image

from app.schemas.diagnosis import SeverityResponse
from app.ml.severity.analyzer import SeverityAnalyzer
from app.services.storage_service import get_storage_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/severity", tags=["Severity Analysis"])


@router.post(
    "/analyze",
    response_model=SeverityResponse,
    summary="Estimate crop infection severity",
    description="Segment diseased plant tissue from healthy leaf area and compute infection percentage and clinical severity level."
)
async def analyze_severity(
    image: UploadFile = File(..., description="Crop leaf image (JPG/PNG)")
) -> SeverityResponse:
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
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file.")

    analyzer = SeverityAnalyzer()
    res = analyzer.analyze(pil_image)

    storage = get_storage_service()
    mask_url = await storage.upload_file(
        file_bytes=res["mask_bytes"],
        filename=f"mask_{uuid.uuid4().hex}.jpg",
        content_type="image/jpeg",
        folder="severity"
    )

    return SeverityResponse(
        severity_level=res["severity_level"],
        affected_percentage=res["severity_percentage"],
        mask_image_url=mask_url,
        description=res["description"]
    )
