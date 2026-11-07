import logging
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserResponse, TokenResponse, FirebaseLoginRequest
from app.services.firebase_auth_service import FirebaseAuthService

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register(self, user_in: UserCreate) -> TokenResponse:
        """Register a new user and generate authentication tokens."""
        # Check phone uniqueness
        existing_phone = await self.user_repo.get_by_phone(user_in.phone)
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this phone number already exists.",
            )

        # Check email uniqueness if email provided
        if user_in.email:
            existing_email = await self.user_repo.get_by_email(user_in.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email address already exists.",
                )

        hashed_password = get_password_hash(user_in.password)
        user = await self.user_repo.create_user(
            full_name=user_in.full_name,
            phone=user_in.phone,
            hashed_password=hashed_password,
            email=user_in.email,
            preferred_language=user_in.preferred_language,
            preferred_theme=user_in.preferred_theme,
            village=user_in.village,
            district=user_in.district,
            state=user_in.state,
            total_acres=user_in.total_acres,
            primary_crops=user_in.primary_crops,
        )

        # Sync farmer profile to Firebase Firestore collection 'users'
        try:
            from app.services.firestore_service import FirestoreService
            FirestoreService.save_farmer_profile({
                "id": str(user.id),
                "full_name": user.full_name,
                "phone": user.phone,
                "email": user.email,
                "village": user_in.village or "Gunjalwadi",
                "district": user_in.district or "Sangamner, Ahilyanagar",
                "state": user_in.state or "Maharashtra",
                "total_acres": user_in.total_acres or 5.0,
                "primary_crops": user_in.primary_crops or ["Tomato", "Wheat"],
                "preferred_language": user.preferred_language,
            })
            logger.info(f"Farmer profile for {user.phone} synced to Firebase Firestore.")
        except Exception as fe:
            logger.warning(f"Firestore farmer sync notice: {fe}")

        access_token = create_access_token(
            subject=str(user.id),
            additional_claims={"phone": user.phone, "role": "farmer"}
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        user_response = UserResponse.model_validate(user)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response,
        )

    async def login(self, phone: str, password: str) -> TokenResponse:
        """Verify user credentials by phone number or email and issue tokens."""
        identifier = phone.strip() if phone else ""
        user = None

        if "@" in identifier:
            user = await self.user_repo.get_by_email(identifier)
        else:
            clean_digits = "".join(c for c in identifier if c.isdigit() or c == "+")
            if clean_digits:
                user = await self.user_repo.get_by_phone(clean_digits)
            if not user:
                user = await self.user_repo.get_by_phone(identifier)
            if not user and "@" not in identifier:
                # Fallback to check email in case phone field was used
                user = await self.user_repo.get_by_email(identifier)

        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Failed login attempt for identifier: {identifier}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid phone number/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated. Please contact support.",
            )

        access_token = create_access_token(
            subject=str(user.id),
            additional_claims={"phone": user.phone, "role": "farmer"}
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        user_response = UserResponse.model_validate(user)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response,
        )

    async def refresh_access_token(self, refresh_token_str: str) -> TokenResponse:
        """Validate refresh token and issue new token pair."""
        payload = decode_token(refresh_token_str)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type for refresh",
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token subject",
            )

        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account no longer active",
            )

        new_access_token = create_access_token(
            subject=str(user.id),
            additional_claims={"phone": user.phone, "role": "farmer"}
        )
        new_refresh_token = create_refresh_token(subject=str(user.id))

        user_response = UserResponse.model_validate(user)
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response,
        )

    async def login_with_firebase(self, req: FirebaseLoginRequest) -> TokenResponse:
        """Authenticate or register farmer via Firebase ID Token (Google Sign-In)."""
        decoded = await FirebaseAuthService.verify_id_token(req.id_token)
        if not decoded:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired Firebase ID token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        uid = decoded.get("uid")
        email = decoded.get("email")
        name = decoded.get("name") or "Farmer Kisan"
        phone = decoded.get("phone_number") or f"+919{uid[:9].lower() if uid else '876543210'}"
        # Ensure digits only or standard format
        clean_phone = "".join(c for c in phone if c.isdigit() or c == "+")
        if len(clean_phone) < 10:
            clean_phone = "+919876543210"

        # Look up existing user by email or phone
        user = None
        if email:
            user = await self.user_repo.get_by_email(email)
        if not user and clean_phone:
            user = await self.user_repo.get_by_phone(clean_phone)

        # Create user if first-time Google sign-in
        if not user:
            from app.core.security import get_password_hash
            dummy_pw = get_password_hash(f"google_oauth_{uid}_{settings.SECRET_KEY[:8]}")
            user = await self.user_repo.create_user(
                full_name=name,
                phone=clean_phone,
                hashed_password=dummy_pw,
                email=email,
                preferred_language=req.preferred_language or "en",
                preferred_theme="light",
            )
            # Create farmer profile with district
            if req.district or req.village:
                from app.schemas.user import FarmerProfileCreate
                await self.user_repo.create_profile(
                    user.id,
                    FarmerProfileCreate(
                        village=req.village or "Baramati",
                        district=req.district or "Pune",
                        state=req.state or "Maharashtra",
                        farm_area_hectares=2.5,
                        primary_crops=["tomato", "wheat"]
                    )
                )

        access_token = create_access_token(
            subject=str(user.id),
            additional_claims={"phone": user.phone, "role": "farmer", "provider": "firebase_google"}
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        user_response = UserResponse.model_validate(user)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response,
        )
