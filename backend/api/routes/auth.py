"""
Echo — Auth Routes
Handles user registration, login, profile management.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.core.dependencies import CurrentUser
from backend.core.exceptions import AuthenticationError, ConflictError
from backend.core.logging import get_logger
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
                company_name="Petromax Industries",
            )
        )

    return ApiResponse(
        data=UserProfile(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            avatar_url=user.get("avatar_url"),
            role=user.get("role", "viewer"),
            company_name=user.get("company_name", ""),
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
            company_name=user.get("company_name", ""),
        ),
        message="Profile updated",
    )
