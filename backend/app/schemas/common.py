from typing import Generic, List, Optional, TypeVar, Any, Dict
from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseBase(BaseModel):
    success: bool = True
    message: Optional[str] = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    environment: str = "development"
    database: str = "connected"
    timestamp: str


class ModelStatus(BaseModel):
    name: str
    available: bool
    details: Optional[str] = None


class ModelsHealthResponse(BaseModel):
    overall_status: str
    models: Dict[str, ModelStatus]


class ErrorResponse(BaseModel):
    success: bool = False
    detail: str
    error_code: Optional[str] = None


class StatusResponse(BaseModel):
    success: bool = True
    message: str


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
