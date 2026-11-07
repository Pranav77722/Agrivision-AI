import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.farmer_profile import FarmerProfile
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate, FarmerProfileUpdate


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = (
            select(User)
            .options(selectinload(User.profile))
            .where(User.id == user_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_phone(self, phone: str) -> Optional[User]:
        stmt = (
            select(User)
            .options(selectinload(User.profile))
            .where(User.phone == phone)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        if not email:
            return None
        stmt = (
            select(User)
            .options(selectinload(User.profile))
            .where(User.email == email)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        full_name: str,
        phone: str,
        hashed_password: str,
        email: Optional[str] = None,
        preferred_language: str = "en",
        preferred_theme: str = "light",
        village: Optional[str] = "Gunjalwadi",
        district: Optional[str] = "Sangamner, Ahilyanagar",
        state: Optional[str] = "Maharashtra",
        total_acres: Optional[float] = 5.0,
        primary_crops: Optional[list] = None
    ) -> User:
        user = User(
            full_name=full_name,
            phone=phone,
            hashed_password=hashed_password,
            email=email,
            preferred_language=preferred_language,
            preferred_theme=preferred_theme,
        )
        self.db.add(user)
        await self.db.flush()

        # Create farmer profile with provided details
        acres = float(total_acres or 5.0)
        profile = FarmerProfile(
            user_id=user.id,
            village=village or "Gunjalwadi",
            district=district or "Sangamner, Ahilyanagar",
            state=state or "Maharashtra",
            farm_area_hectares=round(acres * 0.404686, 2),
            primary_crops=primary_crops or ["Tomato", "Wheat", "Soybean"],
        )
        self.db.add(profile)
        await self.db.flush()

        # Reload with profile
        return await self.get_by_id(user.id)  # type: ignore

    async def update_profile(
        self,
        user_id: uuid.UUID,
        profile_data: FarmerProfileUpdate
    ) -> Optional[FarmerProfile]:
        stmt = select(FarmerProfile).where(FarmerProfile.user_id == user_id)
        result = await self.db.execute(stmt)
        profile = result.scalar_one_or_none()

        if not profile:
            profile = FarmerProfile(user_id=user_id)
            self.db.add(profile)

        update_dict = profile_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)

        await self.db.flush()
        await self.db.refresh(profile)
        return profile
