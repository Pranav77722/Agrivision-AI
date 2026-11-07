import io
import logging
import uuid
from typing import Optional, Dict, Any
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.diagnosis import Diagnosis
from app.repositories.diagnosis_repo import DiagnosisRepository
from app.services.storage_service import get_storage_service
from app.services.recommendation_service import RecommendationService
from app.ml.disease.classifier import DiseaseClassifier
from app.ml.pest.detector import PestDetector
from app.ml.severity.analyzer import SeverityAnalyzer
from app.ml.explainability.gradcam import GradCAMGenerator
from app.ml.disease.leaf_detector import PlantLeafDetector, PlantValidationError

logger = logging.getLogger(__name__)


class DiagnosisService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DiagnosisRepository(db)
        self.storage = get_storage_service()
        self.classifier = DiseaseClassifier()
        self.pest_detector = PestDetector()
        self.severity_analyzer = SeverityAnalyzer()
        self.gradcam_generator = GradCAMGenerator()
        self.leaf_detector = PlantLeafDetector.get_instance()

    def check_is_plant(self, image_bytes: bytes) -> Dict[str, Any]:
        """Verify if image is a real plant or crop leaf."""
        return self.leaf_detector.validate(image_bytes)

    async def run_full_diagnosis(
        self,
        image_bytes: bytes,
        filename: str,
        user_id: Optional[uuid.UUID] = None,
        crop_type: Optional[str] = "Unknown",
        language: str = "en",
        cloud_image_url: Optional[str] = None
    ) -> Diagnosis:
        """Run complete diagnostic pipeline and persist results."""
        # 1. Validate & open image
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
            image = Image.open(io.BytesIO(image_bytes))  # Re-open after verify
            # Memory optimization for production cloud containers (Voroa Nano / 512MB RAM):
            # Downscale large mobile camera photos (e.g. 12MP/50MP) to max 1024x1024 to prevent cgroup OOM kills
            if max(image.size) > 1024:
                image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                image.convert("RGB").save(buf, format="JPEG", quality=85)
                image_bytes = buf.getvalue()
                logger.info(f"Downscaled high-res leaf image to {image.size} for lightweight memory efficiency.")
        except Exception as e:
            logger.error(f"Invalid image format: {e}")
            raise ValueError("Invalid image file. Please upload a valid JPG or PNG.")

        # 1.5. Plant & Leaf Out-of-Domain Verification
        validation = self.check_is_plant(image_bytes)
        if not validation["is_plant"]:
            logger.warning(
                f"Image rejected - NOT a plant leaf: object={validation['detected_object']}, "
                f"foliage={validation['foliage_ratio']:.2f}, skin={validation['skin_ratio']:.2f}"
            )
            raise PlantValidationError(
                message=validation["message"],
                detected_object=validation["detected_object"],
                reasons=validation["reasons"],
            )

        # 2. Upload original image (or use provided Cloudinary URL)
        if cloud_image_url and cloud_image_url.startswith("http"):
            uploaded_image_url = cloud_image_url
            logger.info(f"Using pre-uploaded Cloudinary image URL: {uploaded_image_url}")
        else:
            uploaded_image_url = await self.storage.upload_file(
                file_bytes=image_bytes,
                filename=filename,
                content_type="image/jpeg",
                folder="crop-scans"
            )

        # 3. Disease Classification & Ensemble (Local Agronomic CV)
        disease_res = self.classifier.predict(image, crop_hint=crop_type or "Unknown")
        predicted_disease = disease_res["predicted_disease"]
        detected_crop = disease_res["crop_type"] if crop_type == "Unknown" else crop_type

        # 3.5 NVIDIA NIM Multimodal Vision AI Enhancement
        nvidia_res = None
        try:
            from app.services.nvidia_vision_service import NvidiaVisionService
            nvidia_res = await NvidiaVisionService.analyze_leaf(
                image_bytes=image_bytes,
                crop_hint=crop_type or "Unknown",
                cloud_image_url=uploaded_image_url,
                language=language
            )
            if nvidia_res and nvidia_res.get("predicted_disease"):
                logger.info(f"Applying NVIDIA NIM Vision diagnosis: {nvidia_res['predicted_disease']}")
                predicted_disease = nvidia_res["predicted_disease"]
                if nvidia_res.get("crop_type") and (detected_crop == "Unknown" or not detected_crop):
                    detected_crop = str(nvidia_res["crop_type"]).capitalize()
                if nvidia_res.get("confidence"):
                    disease_res["confidence"] = float(nvidia_res["confidence"])
                disease_res["ensemble_results"]["nvidia_nemotron_vision"] = {
                    "disease": nvidia_res["predicted_disease"],
                    "confidence": float(nvidia_res.get("confidence", 0.92)),
                    "pathogen": nvidia_res.get("pathogen", ""),
                    "reasoning": nvidia_res.get("ai_reasoning", ""),
                    "focus": nvidia_res.get("focus_description", ""),
                    "attention_regions": nvidia_res.get("attention_regions", [])
                }
        except Exception as ne:
            logger.warning(f"NVIDIA Vision enhancement skipped: {ne}")

        # 4. Severity Analysis
        severity_res = self.severity_analyzer.analyze(image)
        if nvidia_res and nvidia_res.get("is_healthy"):
            severity_res["severity_level"] = "Healthy"
            severity_res["severity_percentage"] = 0.0
        elif nvidia_res and "diseased_area_percent" in nvidia_res:
            severity_res["severity_percentage"] = float(nvidia_res["diseased_area_percent"])
            if nvidia_res.get("severity_level"):
                severity_res["severity_level"] = str(nvidia_res["severity_level"]).capitalize()
        elif nvidia_res and nvidia_res.get("severity_level") in ["Mild", "Moderate", "Severe"]:
            # Harmonize with NVIDIA pathology assessment if local CV is uncertain
            if severity_res["severity_level"] == "Healthy":
                severity_res["severity_level"] = nvidia_res["severity_level"]
                severity_res["severity_percentage"] = 25.0 if nvidia_res["severity_level"] == "Moderate" else (10.0 if nvidia_res["severity_level"] == "Mild" else 60.0)

        # 5. Pest Detection
        pest_res = self.pest_detector.detect(image)

        # 6. Grad-CAM Explainability
        explain_res = self.gradcam_generator.generate(image)
        gradcam_url = await self.storage.upload_file(
            file_bytes=explain_res["heatmap_bytes"],
            filename=f"gradcam_{uuid.uuid4().hex}.jpg",
            content_type="image/jpeg",
            folder="explainability"
        )

        # 7. Recommendations
        recommendations = RecommendationService.get_disease_recommendations(
            disease_name=predicted_disease,
            language=language
        )
        if nvidia_res:
            # Enrich recommendations with clinical details extracted directly by the vision model
            if nvidia_res.get("symptoms"):
                recommendations["symptoms"] = nvidia_res["symptoms"]
            if nvidia_res.get("organic_control"):
                recommendations["organic_control"] = nvidia_res["organic_control"]
            if nvidia_res.get("chemical_control"):
                recommendations["chemical_control"] = nvidia_res["chemical_control"]
            if nvidia_res.get("cultural_practices"):
                recommendations["cultural_practices"] = nvidia_res["cultural_practices"]
            if nvidia_res.get("safety_measures"):
                recommendations["safety"] = nvidia_res["safety_measures"]
            if nvidia_res.get("dosage"):
                recommendations["dosage"] = nvidia_res["dosage"]
            if nvidia_res.get("spray_interval_days"):
                recommendations["interval_days"] = nvidia_res["spray_interval_days"]
            if nvidia_res.get("pathogen"):
                recommendations["pathogen"] = nvidia_res["pathogen"]
            if nvidia_res.get("urgency_window"):
                recommendations["urgency_window"] = nvidia_res["urgency_window"]
            if nvidia_res.get("local_names"):
                recommendations["local_names"] = nvidia_res["local_names"]

        # 8. Persist to Database
        diagnosis = await self.repo.create(
            user_id=user_id,
            image_url=uploaded_image_url,
            crop_type=detected_crop,
            predicted_disease=predicted_disease,
            confidence=disease_res["confidence"],
            severity=severity_res["severity_level"],
            severity_percentage=severity_res["severity_percentage"],
            ensemble_results=disease_res["ensemble_results"],
            pest_detections=pest_res["detections"],
            explainability_url=gradcam_url,
            recommendations=recommendations,
            model_version=disease_res["model_version"],
            inference_time_ms=disease_res["inference_time_ms"],
            language=language,
            status="completed",
        )

        # 9. Sync full model analysis and Cloudinary image link to Firebase Firestore
        try:
            from app.services.firestore_service import FirestoreService
            FirestoreService.save_diagnosis({
                "id": str(diagnosis.id),
                "user_id": str(diagnosis.user_id) if diagnosis.user_id else "farmer_01",
                "image_url": uploaded_image_url,
                "crop_type": detected_crop,
                "predicted_disease": predicted_disease,
                "confidence": disease_res["confidence"],
                "severity": severity_res["severity_level"],
                "severity_percentage": severity_res["severity_percentage"],
                "pest_detections": pest_res["detections"],
                "recommendations": recommendations,
                "explainability_url": gradcam_url,
                "model_version": disease_res["model_version"],
            })
            logger.info(f"Diagnosis {diagnosis.id} synced to Firebase Firestore successfully.")
        except Exception as fe:
            logger.warning(f"Firestore sync warning: {fe}")

        return diagnosis
