import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class FarmerProfileBase(BaseModel):
    village: Optional[str] = None
    district: Optional[str] = None
    state: str = "Maharashtra"
    farm_area_hectares: float = Field(default=0.0, ge=0.0)
    primary_crops: List[str] = Field(default_factory=list)
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    profile_photo_url: Optional[str] = None


class FarmerProfileCreate(FarmerProfileBase):
    pass


class FarmerProfileUpdate(BaseModel):
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    farm_area_hectares: Optional[float] = Field(default=None, ge=0.0)
    primary_crops: Optional[List[str]] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    profile_photo_url: Optional[str] = None


class FarmerProfileResponse(FarmerProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    preferred_language: str = Field(default="en", pattern="^(en|mr|hi)$")
    preferred_theme: str = Field(default="light", pattern="^(light|dark)$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)
    village: Optional[str] = "Gunjalwadi"
    district: Optional[str] = "Sangamner, Ahilyanagar"
    state: Optional[str] = "Maharashtra"
    total_acres: Optional[float] = Field(default=5.0, alias="totalAcres")
    primary_crops: Optional[List[str]] = Field(default_factory=lambda: ["Tomato", "Wheat"], alias="primaryCrops")

    model_config = ConfigDict(populate_by_name=True)


class UserLogin(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    phone_or_email: Optional[str] = Field(default=None, alias="phoneOrEmail")
    username_or_phone: Optional[str] = Field(default=None, alias="usernameOrPhone")
    password: str

    model_config = ConfigDict(populate_by_name=True)

    def get_identifier(self) -> str:
        return (
            self.phone_or_email
            or self.username_or_phone
            or self.email
            or self.phone
            or ""
        )


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class FirebaseLoginRequest(BaseModel):
    id_token: str
    preferred_language: Optional[str] = "en"
    village: Optional[str] = None
    district: Optional[str] = "Pune"
    state: Optional[str] = "Maharashtra"


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None


class LanguageUpdate(BaseModel):
    preferred_language: str = Field(..., pattern="^(en|mr|hi)$")


class ThemeUpdate(BaseModel):
    preferred_theme: str = Field(..., pattern="^(light|dark)$")


class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    phone: str
    email: Optional[str] = None
    is_active: bool
    preferred_language: str
    preferred_theme: str
    created_at: datetime
    updated_at: datetime
    profile: Optional[FarmerProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
