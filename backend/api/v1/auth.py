"""
Echo — Auth API
Endpoints for authentication.
"""

from fastapi import APIRouter, Depends
from backend.schemas.auth import LoginRequest, RegisterRequest, AuthResponse, RefreshTokenRequest
from backend.services.auth_service import AuthService
from backend.schemas.base import ApiResponse
from backend.core.dependencies import get_current_user_id

router = APIRouter()


@router.post("/register", response_model=ApiResponse[dict])
async def register(request: RegisterRequest):
    service = AuthService()
    data = await service.register(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        organization=request.organization
    )
    return ApiResponse(data=data, message="Registration successful")


@router.post("/login", response_model=ApiResponse[AuthResponse])
async def login(request: LoginRequest):
    service = AuthService()
    data = await service.login(request.email, request.password)
    return ApiResponse(data=data, message="Login successful")


@router.post("/refresh", response_model=ApiResponse[dict])
async def refresh(request: RefreshTokenRequest):
    service = AuthService()
    data = await service.refresh_token(request.refresh_token)
    return ApiResponse(data=data)


@router.get("/me", response_model=ApiResponse[dict])
async def get_me(user_id: str = Depends(get_current_user_id)):
    # Simple returning the user_id for now, usually would fetch from DB
    return ApiResponse(data={"id": user_id})
