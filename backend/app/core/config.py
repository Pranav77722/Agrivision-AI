import os
from pathlib import Path
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    # Server Configuration
    PROJECT_NAME: str = "Agrivision AI+"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_ENV: str = "development"
    DEBUG: bool = True

    # Security & JWT
    SECRET_KEY: str = "agrivision-ai-super-secret-key-production-change-32-chars-min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:8081",
        "http://localhost:19006",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./agrivision.db"
    DB_ECHO: bool = False

    # Supabase (Optional production cloud storage & auth)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    SUPABASE_STORAGE_BUCKET: str = "agrivision-images"
    SUPABASE_REPORTS_BUCKET: str = "agrivision-reports"

    # Firebase Authentication & Admin
    FIREBASE_CREDENTIALS_PATH: str = ""
    FIREBASE_PROJECT_ID: str = "agrivision-ai"

    # Local Storage Directory
    STORAGE_LOCAL_DIR: str = "./uploads"

    # Cloudinary Storage Configuration
    STORAGE_PROVIDER: str = "cloudinary"
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    CLOUDINARY_FOLDER: str = "Agrivision"

    # ML Model Paths
    MODEL_WEIGHTS_DIR: str = "./ml/models/weights"
    DISEASE_MODEL_PATH: str = "./ml/models/weights/efficientnetb3_disease.h5"
    ENSEMBLE_VGG16_PATH: str = "./ml/models/weights/vgg16_disease.h5"
    ENSEMBLE_VGG19_PATH: str = "./ml/models/weights/vgg19_disease.h5"
    ENSEMBLE_INCEPTION_PATH: str = "./ml/models/weights/inceptionv3_disease.h5"
    ENSEMBLE_RESNET_PATH: str = "./ml/models/weights/resnet101v2_disease.h5"
    YOLO_MODEL_PATH: str = "./ml/models/weights/yolov8_pest.pt"
    SEVERITY_MODEL_PATH: str = "./ml/models/weights/unet_severity.h5"
    YIELD_MODEL_PATH: str = "./ml/models/weights/xgboost_yield.joblib"

    # Weather API (OpenWeatherMap)
    WEATHER_API_KEY: str = ""
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"

    # Bhashini Multilingual / Speech APIs
    BHASHINI_API_KEY: str = ""
    BHASHINI_USER_ID: str = ""
    BHASHINI_ULCA_API_URL: str = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model"
    BHASHINI_PIPELINE_URL: str = "https://dhruva-api.bhashini.gov.in/services/inference"

    # LLM Provider
    LLM_PROVIDER: str = "nvidia"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # NVIDIA NIM Vision AI
    NVIDIA_API_KEY: str = "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"
    NVIDIA_BACKUP_KEYS: List[str] = [
        "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",
        "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"
    ]
    NVIDIA_MODEL: str = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"
    NVIDIA_API_URL: str = "https://integrate.api.nvidia.com/v1/chat/completions"
    NVIDIA_TIMEOUT_SECONDS: int = 25

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 120


settings = Settings()


def resolve_asset_path(path_str: str) -> Path:
    """Resolve file path checking cwd, backend directory, and ancestor project roots."""
    p = Path(path_str)
    if p.is_file():
        return p.resolve()
    if (Path.cwd() / p).is_file():
        return (Path.cwd() / p).resolve()
    cur_file = Path(__file__).resolve()
    for parent in cur_file.parents:
        if (parent / p).is_file():
            return (parent / p).resolve()
    return p

