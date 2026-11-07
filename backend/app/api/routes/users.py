import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import (
    FarmerProfileResponse,
    FarmerProfileUpdate,
    LanguageUpdate,
    ThemeUpdate,
    UserResponse,
)
from app.schemas.common import StatusResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users & Profiles"])


@router.get(
    "/profile",
    response_model=FarmerProfileResponse,
    summary="Get farmer farm profile",
    description="Retrieve the detailed farm profile (land area, crops, soil, irrigation) for the current farmer."
)
async def get_farmer_profile(
    current_user: User = Depends(get_current_user)
) -> FarmerProfileResponse:
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Farmer profile has not been initialized yet.",
        )
    return FarmerProfileResponse.model_validate(current_user.profile)


@router.put(
    "/profile",
    response_model=FarmerProfileResponse,
    summary="Update farmer farm profile",
    description="Update farm parameters such as district, village, crops, soil type, and acreage."
)
async def update_farmer_profile(
    profile_in: FarmerProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> FarmerProfileResponse:
    user_repo = UserRepository(db)
    updated_profile = await user_repo.update_profile(current_user.id, profile_in)
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update farmer profile.",
        )
    return FarmerProfileResponse.model_validate(updated_profile)


@router.put(
    "/language",
    response_model=UserResponse,
    summary="Update preferred language",
    description="Change default communication language: 'en' (English), 'mr' (Marathi), or 'hi' (Hindi)."
)
async def update_language(
    lang_in: LanguageUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user_repo = UserRepository(db)
    updated_user = await user_repo.update(
        current_user.id,
        preferred_language=lang_in.preferred_language
    )
    # Reload with profile
    reloaded = await user_repo.get_by_id(current_user.id)
    return UserResponse.model_validate(reloaded)


@router.put(
    "/theme",
    response_model=UserResponse,
    summary="Update theme preference",
    description="Update UI color theme: 'light' or 'dark'."
)
async def update_theme(
    theme_in: ThemeUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user_repo = UserRepository(db)
    await user_repo.update(
        current_user.id,
        preferred_theme=theme_in.preferred_theme
    )
    reloaded = await user_repo.get_by_id(current_user.id)
    return UserResponse.model_validate(reloaded)


@router.delete(
    "/account",
    response_model=StatusResponse,
    summary="Delete user account",
    description="Permanently remove farmer account and all associated diagnoses, chats, and records."
)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> StatusResponse:
    user_repo = UserRepository(db)
    deleted = await user_repo.delete(current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not delete account.",
        )
    return StatusResponse(success=True, message="Farmer account deleted successfully.")
