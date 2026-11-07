import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlalchemy import String, Float, Boolean, JSON, ForeignKey, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class YieldPrediction(Base):
    __tablename__ = "yield_predictions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    crop: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    season: Mapped[str] = mapped_column(String(50), nullable=False)
    area_hectares: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    soil_type: Mapped[str] = mapped_column(String(100), default="Black Soil", nullable=False)
    irrigation: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    predicted_yield_kg_per_hectare: Mapped[float] = mapped_column(Float, nullable=False)
    predicted_total_production_kg: Mapped[float] = mapped_column(Float, nullable=False)
    prediction_range_low: Mapped[float] = mapped_column(Float, nullable=False)
    prediction_range_high: Mapped[float] = mapped_column(Float, nullable=False)
    risk_factors: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    influencing_factors: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="yield_predictions")
