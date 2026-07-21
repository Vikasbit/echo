"""
Echo — Auth Routes
Handles user registration, login, profile management.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.core.dependencies import CurrentUser
from backend.core.exceptions import AuthenticationError, ConflictError
from backend.core.logging import get_logger
from backend.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from backend.db.repositories.user_repo import UserRepository
from backend.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UpdateProfileRequest,
    UserProfile,
)
from backend.schemas.base import ApiResponse

logger = get_logger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

user_repo = UserRepository()


@router.post("/register", response_model=ApiResponse[AuthResponse])
async def register(request: RegisterRequest):
    """Register a new user account."""
    exists = await user_repo.exists(request.email)
    if exists:
        raise ConflictError("An account with this email already exists")

    hashed = hash_password(request.password)

    user = await user_repo.create({
        "email": request.email,
        "full_name": request.full_name,
        "organization": request.organization,
        "role": "admin",
        "password_hash": hashed,
    })

    access_token = create_access_token({"sub": user["id"]})
    refresh_token = create_refresh_token(user["id"])

    profile = UserProfile(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user.get("role", "viewer"),
        organization=user.get("organization", ""),
        created_at=user.get("created_at"),
    )

    return ApiResponse(
        data=AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=86400,
            user=profile,
        ),
        message="Account created successfully",
    )


@router.post("/login", response_model=ApiResponse[AuthResponse])
async def login(request: LoginRequest):
    """Authenticate user and return JWT tokens."""
    user = await user_repo.get_by_email(request.email)

    if not user:
        raise AuthenticationError("Invalid email or password")

    if not verify_password(request.password, user.get("password_hash", "")):
        raise AuthenticationError("Invalid email or password")

    access_token = create_access_token({"sub": user["id"]})
    refresh_token = create_refresh_token(user["id"])

    profile = UserProfile(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        role=user.get("role", "viewer"),
        organization=user.get("organization", ""),
        created_at=user.get("created_at"),
    )

    logger.info("user_logged_in", user_id=user["id"])

    return ApiResponse(
        data=AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=86400,
            user=profile,
        ),
        message="Login successful",
    )


@router.get("/profile", response_model=ApiResponse[UserProfile])
async def get_profile(user_id: CurrentUser):
    """Get the current user's profile."""
    user = await user_repo.get_by_id(user_id)

    if not user:
        # Demo mode fallback
        return ApiResponse(
            data=UserProfile(
                id="demo-user-001",
                email="demo@indus.ai",
                full_name="Demo Engineer",
                role="admin",
                organization="Petromax Industries",
            )
        )

    return ApiResponse(
        data=UserProfile(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            avatar_url=user.get("avatar_url"),
            role=user.get("role", "viewer"),
            organization=user.get("organization", ""),
            created_at=user.get("created_at"),
        )
    )


@router.patch("/profile", response_model=ApiResponse[UserProfile])
async def update_profile(request: UpdateProfileRequest, user_id: CurrentUser):
    """Update the current user's profile."""
    update_data = request.model_dump(exclude_none=True)
    if not update_data:
        return ApiResponse(message="No changes provided")

    user = await user_repo.update(user_id, update_data)

    return ApiResponse(
        data=UserProfile(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            avatar_url=user.get("avatar_url"),
            role=user.get("role", "viewer"),
            organization=user.get("organization", ""),
        ),
        message="Profile updated",
    )
