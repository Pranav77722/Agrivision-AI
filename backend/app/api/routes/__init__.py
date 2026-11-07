from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.diagnosis import router as diagnosis_router
from app.api.routes.ensemble import router as ensemble_router
from app.api.routes.pest_detection import router as pest_router
from app.api.routes.severity import router as severity_router
from app.api.routes.explainability import router as explainability_router
from app.api.routes.yield_prediction import router as yield_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.knowledge import router as knowledge_router
from app.api.routes.assistant import router as assistant_router
from app.api.routes.reports import router as reports_router
from app.api.routes.language import router as language_router
from app.api.routes.weather import router as weather_router
from app.api.routes.health import router as health_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(diagnosis_router)
api_router.include_router(ensemble_router)
api_router.include_router(pest_router)
api_router.include_router(severity_router)
api_router.include_router(explainability_router)
api_router.include_router(yield_router)
api_router.include_router(recommendations_router)
api_router.include_router(knowledge_router)
api_router.include_router(assistant_router)
api_router.include_router(reports_router)
api_router.include_router(language_router)
api_router.include_router(weather_router)
api_router.include_router(health_router)
