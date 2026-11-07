import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlalchemy import String, Float, JSON, ForeignKey, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.report import Report


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    crop_type: Mapped[str] = mapped_column(String(100), nullable=False, default="Unknown")
    predicted_disease: Mapped[str] = mapped_column(String(200), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="Unknown", nullable=False)
    severity_percentage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    ensemble_results: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    pest_detections: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    explainability_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    recommendations: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), default="1.0.0", nullable=False)
    inference_time_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="completed", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="diagnoses")
    reports: Mapped[List["Report"]] = relationship(
        "Report", back_populates="diagnosis", cascade="all, delete-orphan"
    )
