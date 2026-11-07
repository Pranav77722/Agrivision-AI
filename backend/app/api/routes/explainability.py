import io
import uuid
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from PIL import Image

from app.schemas.diagnosis import ExplainabilityResponse
from app.ml.explainability.gradcam import GradCAMGenerator
from app.services.storage_service import get_storage_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/explainability", tags=["Model Explainability"])


@router.post(
    "/gradcam",
    response_model=ExplainabilityResponse,
    summary="Generate Grad-CAM saliency map",
    description="Generate a visual attention heatmap explaining which regions of the plant leaf triggered the neural network's diagnostic decision."
)
async def generate_gradcam(
    image: UploadFile = File(..., description="Crop leaf image (JPG/PNG)")
) -> ExplainabilityResponse:
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

    generator = GradCAMGenerator()
    res = generator.generate(pil_image)

    storage = get_storage_service()
    heatmap_url = await storage.upload_file(
        file_bytes=res["heatmap_bytes"],
        filename=f"gradcam_{uuid.uuid4().hex}.jpg",
        content_type="image/jpeg",
        folder="explainability"
    )

    return ExplainabilityResponse(
        gradcam_image_url=heatmap_url,
        heatmap_intensity=res["heatmap_intensity"],
        focus_regions_description=res["focus_regions_description"]
    )
