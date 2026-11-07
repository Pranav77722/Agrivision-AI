import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class ReportGenerateRequest(BaseModel):
    language: str = Field(default="en", pattern="^(en|mr|hi)$")


class ReportResponse(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    diagnosis_id: uuid.UUID
    report_url: str
    language: str
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportListResponse(BaseModel):
    items: List[ReportResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
