import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field


class PestDetectionItem(BaseModel):
    pest_name: str
    confidence: float
    bbox: List[float] = Field(default_factory=list, description="[x_min, y_min, x_max, y_max]")


class RecommendationItem(BaseModel):
    treatment_type: str = Field(description="e.g. chemical, organic, cultural")
    recommendation: str
    dosage: Optional[str] = None
    precautions: Optional[str] = None


class RecommendationsData(BaseModel):
    crop: str
    disease_or_pest: str
    severity: Optional[str] = None
    chemical_control: List[str] = Field(default_factory=list)
    organic_control: List[str] = Field(default_factory=list)
    cultural_practices: List[str] = Field(default_factory=list)
    preventive_measures: List[str] = Field(default_factory=list)
    additional_notes: Optional[str] = None


class EnsembleModelScore(BaseModel):
    model_name: str
    prediction: str
    confidence: float


class EnsemblePredictionResponse(BaseModel):
    predicted_disease: str
    confidence: float
    crop_type: str
    model_predictions: List[EnsembleModelScore]
    agreement_score: float


class PestDetectionResponse(BaseModel):
    pest_count: int
    detections: List[PestDetectionItem]
    annotated_image_url: Optional[str] = None


class SeverityResponse(BaseModel):
    severity_level: str  # Low, Moderate, High, Severe
    affected_percentage: float
    mask_image_url: Optional[str] = None
    description: Optional[str] = None


class ExplainabilityResponse(BaseModel):
    gradcam_image_url: str
    heatmap_intensity: float
    focus_regions_description: Optional[str] = None


class DiagnosisCreate(BaseModel):
    crop_type: Optional[str] = "Unknown"
    language: Optional[str] = "en"


class DiagnosisResponse(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    image_url: str
    crop_type: str
    predicted_disease: str
    confidence: float
    severity: str
    severity_percentage: float
    ensemble_results: Dict[str, Any]
    pest_detections: List[Dict[str, Any]]
    explainability_url: Optional[str] = None
    recommendations: Dict[str, Any]
    model_version: str
    inference_time_ms: float
    language: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiagnosisListResponse(BaseModel):
    items: List[DiagnosisResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
