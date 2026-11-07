import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict, Field


class YieldInput(BaseModel):
    crop: str = Field(..., min_length=2, max_length=100)
    district: str = Field(..., min_length=2, max_length=100)
    season: str = Field(..., min_length=2, max_length=50)
    area_hectares: float = Field(..., gt=0.0)
    soil_type: str = Field(default="Black Soil", max_length=100)
    irrigation: bool = Field(default=True)
    rainfall_mm: Optional[float] = Field(default=None, ge=0.0)
    temperature_c: Optional[float] = Field(default=None)
    fertilizer_used_kg: Optional[float] = Field(default=None, ge=0.0)


class RiskFactor(BaseModel):
    factor: str
    impact_level: str  # Low, Moderate, High
    description: str
    mitigation_strategy: str


class InfluencingFactors(BaseModel):
    soil_suitability_score: float
    weather_impact_score: float
    irrigation_benefit_percentage: float
    historical_benchmark_yield: float


class YieldResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    crop: str
    district: str
    season: str
    area_hectares: float
    soil_type: str
    irrigation: bool
    predicted_yield_kg_per_hectare: float
    predicted_total_production_kg: float
    prediction_range_low: float
    prediction_range_high: float
    risk_factors: List[Dict[str, Any]] = Field(default_factory=list)
    influencing_factors: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class YieldHistoryResponse(BaseModel):
    items: List[YieldResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
