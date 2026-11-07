import os
import logging
from typing import Optional, Dict, Any
import firebase_admin
from firebase_admin import auth, credentials
from app.core.config import settings

logger = logging.getLogger(__name__)

class FirebaseAuthService:
    _initialized = False

    @classmethod
    def initialize(cls):
        if cls._initialized:
            return
        
        try:
            if settings.FIREBASE_CREDENTIALS_PATH and os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin initialized with service account key")
            else:
                # Initialize default app with project id
                options = {"projectId": settings.FIREBASE_PROJECT_ID} if settings.FIREBASE_PROJECT_ID else None
                firebase_admin.initialize_app(options=options)
                logger.info(f"Firebase Admin initialized with project ID: {settings.FIREBASE_PROJECT_ID}")
            cls._initialized = True
        except ValueError:
            # Already initialized
            cls._initialized = True
        except Exception as e:
            logger.warning(f"Firebase Admin initialization deferred / mock mode: {e}")

    @classmethod
    async def verify_id_token(cls, id_token: str) -> Optional[Dict[str, Any]]:
        cls.initialize()
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            logger.warning(f"Firebase token verification failed via Admin SDK ({e}), attempting mock/fallback decode")
            # If development mock or test token
            if id_token.startswith("mock_") or "mock" in id_token:
                return {
                    "uid": "google_pranav_khaire_124",
                    "email": "khairepranav124@gmail.com",
                    "name": "Pranav Khaire",
                    "picture": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80",
                    "firebase": {"sign_in_provider": "google.com"}
                }
            return None

