import io
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from PIL import Image

from app.schemas.diagnosis import PestDetectionResponse, PestDetectionItem
from app.ml.pest.detector import PestDetector

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pest", tags=["Pest Detection"])


@router.post(
    "/detect",
    response_model=PestDetectionResponse,
    summary="Detect agricultural insect pests",
    description="Run YOLO-based computer vision detection to identify, count, and locate pests (such as Whiteflies, Aphids, Thrips) in the image."
)
async def detect_pests(
    image: UploadFile = File(..., description="Crop leaf image (JPG/PNG)")
) -> PestDetectionResponse:
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

    detector = PestDetector()
    res = detector.detect(pil_image)

    items = [
        PestDetectionItem(
            pest_name=d["pest_name"],
            confidence=d["confidence"],
            bbox=d["bbox"]
        )
        for d in res["detections"]
    ]

    return PestDetectionResponse(
        pest_count=res["pest_count"],
        detections=items,
        annotated_image_url=None
    )
