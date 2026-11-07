import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
    FirebaseLoginRequest,
)
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new farmer account",
    description="Registers a new farmer with their name, phone number, and password, creating their profile and returning access/refresh tokens."
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    auth_service = AuthService(db)
    return await auth_service.register(user_in)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Farmer login",
    description="Authenticate with phone number or email and password to obtain JWT access and refresh tokens."
)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    auth_service = AuthService(db)
    identifier = credentials.get_identifier()
    return await auth_service.login(phone=identifier, password=credentials.password)


@router.post(
    "/firebase-login",
    response_model=TokenResponse,
    summary="Firebase / Google OAuth login",
    description="Authenticate via Firebase Google ID token, creating or retrieving the farmer's account."
)
async def firebase_login(
    req: FirebaseLoginRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    auth_service = AuthService(db)
    return await auth_service.login_with_firebase(req)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Exchange a valid refresh token for a newly issued access/refresh token pair."
)
async def refresh_token(
    refresh_req: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    auth_service = AuthService(db)
    return await auth_service.refresh_access_token(refresh_req.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Retrieve the authenticated farmer's profile, including their farm details and preferences."
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)
