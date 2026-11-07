import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Float, JSON, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    village: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    state: Mapped[str] = mapped_column(String(100), default="Maharashtra", nullable=False)
    farm_area_hectares: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    primary_crops: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    soil_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    irrigation_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    profile_photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="profile")
