import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings

logger = logging.getLogger(__name__)


class FirestoreService:
    _db: Optional[firestore.Client] = None

    @classmethod
    def get_db(cls) -> Optional[firestore.Client]:
        if cls._db is not None:
            return cls._db

        try:
            cred_path = settings.FIREBASE_CREDENTIALS_PATH
            if not os.path.exists(cred_path):
                # Try fallback root directory path
                root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "agrivision-4223d-firebase-adminsdk-fbsvc-8744bcabb3.json"))
                if os.path.exists(root_path):
                    cred_path = root_path

            if os.path.exists(cred_path):
                try:
                    app = firebase_admin.get_app()
                except ValueError:
                    cred = credentials.Certificate(cred_path)
                    app = firebase_admin.initialize_app(cred)
                cls._db = firestore.client(app=app)
                logger.info("Firestore Admin Client successfully connected.")
            else:
                logger.warning(f"Firebase credentials not found at {cred_path}. Firestore running in mock mode.")
        except Exception as e:
            logger.error(f"Failed to initialize Firestore Client: {e}")

        return cls._db

    @classmethod
    def save_farmer_profile(cls, user_data: Dict[str, Any]) -> bool:
        """Save or update farmer profile in Firestore collection 'users'."""
        db = cls.get_db()
        if db is None:
            logger.warning("Firestore DB not available, skipping save_farmer_profile.")
            return False

        try:
            user_id = str(user_data.get("id") or user_data.get("phone") or "farmer")
            doc_ref = db.collection("users").document(user_id)
            
            # Prepare clean serializable dict
            clean_data = {
                "id": user_id,
                "fullName": user_data.get("full_name") or user_data.get("fullName") or "",
                "phoneNumber": user_data.get("phone") or user_data.get("phoneNumber") or "",
                "email": user_data.get("email") or "",
                "village": user_data.get("village") or "Gunjalwadi",
                "district": user_data.get("district") or "Ahilyanagar",
                "state": user_data.get("state") or "Maharashtra",
                "totalAcres": float(user_data.get("total_acres") or user_data.get("totalAcres") or user_data.get("farm_area_hectares") or 5.0),
                "primaryCrops": user_data.get("primary_crops") or user_data.get("primaryCrops") or ["tomato", "wheat"],
                "preferredLanguage": user_data.get("preferred_language") or "en",
                "updatedAt": datetime.utcnow().isoformat(),
            }
            if "createdAt" not in user_data:
                clean_data["createdAt"] = datetime.utcnow().isoformat()

            doc_ref.set(clean_data, merge=True)
            logger.info(f"Saved farmer profile to Firestore: {user_id} ({clean_data['fullName']})")
            return True
        except Exception as e:
            logger.error(f"Error saving farmer profile to Firestore: {e}")
            return False

    @classmethod
    def save_diagnosis(cls, diagnosis_data: Dict[str, Any]) -> bool:
        """Save crop disease diagnosis, image URL (Cloudinary), and model analysis to Firestore."""
        db = cls.get_db()
        if db is None:
            logger.warning("Firestore DB not available, skipping save_diagnosis.")
            return False

        try:
            diag_id = str(diagnosis_data.get("id") or f"diag_{int(datetime.utcnow().timestamp())}")
            doc_ref = db.collection("diagnoses").document(diag_id)

            record = {
                "id": diag_id,
                "userId": str(diagnosis_data.get("user_id") or diagnosis_data.get("userId") or "farmer_01"),
                "imageUrl": diagnosis_data.get("image_url") or diagnosis_data.get("imageUrl") or diagnosis_data.get("imageUri") or "",
                "cropType": diagnosis_data.get("crop_type") or diagnosis_data.get("cropType") or diagnosis_data.get("crop") or "Unknown",
                "predictedDisease": diagnosis_data.get("predicted_disease") or diagnosis_data.get("predictedDisease") or diagnosis_data.get("diseaseName") or "Unknown",
                "confidence": float(diagnosis_data.get("confidence") or 0.0),
                "severity": diagnosis_data.get("severity") or "Mild",
                "severityPercentage": float(diagnosis_data.get("severity_percentage") or diagnosis_data.get("severityPercentage") or 0.0),
                "pestDetections": diagnosis_data.get("pest_detections") or diagnosis_data.get("pestDetections") or [],
                "recommendations": diagnosis_data.get("recommendations") or {},
                "explainabilityUrl": diagnosis_data.get("explainability_url") or diagnosis_data.get("explainabilityUrl") or "",
                "modelVersion": diagnosis_data.get("model_version") or diagnosis_data.get("modelVersion") or "1.0.0",
                "status": diagnosis_data.get("status") or "completed",
                "createdAt": diagnosis_data.get("created_at") or diagnosis_data.get("createdAt") or datetime.utcnow().isoformat(),
                "updatedAt": datetime.utcnow().isoformat(),
            }

            doc_ref.set(record, merge=True)
            logger.info(f"Saved diagnosis {diag_id} to Firestore collection 'diagnoses' with image: {record['imageUrl']}")
            return True
        except Exception as e:
            logger.error(f"Error saving diagnosis to Firestore: {e}")
            return False

    @classmethod
    def list_diagnoses(cls, user_id: Optional[str] = None, limit_count: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent diagnoses from Firestore."""
        db = cls.get_db()
        if db is None:
            return []

        try:
            coll = db.collection("diagnoses")
            if user_id:
                query = coll.where("userId", "==", str(user_id)).order_by("createdAt", direction=firestore.Query.DESCENDING).limit(limit_count)
            else:
                query = coll.order_by("createdAt", direction=firestore.Query.DESCENDING).limit(limit_count)

            docs = query.stream()
            return [d.to_dict() for d in docs]
        except Exception as e:
            logger.error(f"Error fetching diagnoses from Firestore: {e}")
            return []
