"""
Echo — Dependency Injection
FastAPI dependencies for authentication, database access, and service injection.
"""

from __future__ import annotations

from typing import Annotated, Optional
from pydantic import BaseModel

from fastapi import Depends, Header


from backend.core.config import Settings, get_settings
from backend.core.exceptions import AuthenticationError
from backend.core.logging import get_logger


logger = get_logger(__name__)

class UserContext(BaseModel):
    id: str
    workspace_id: str
    company_id: str
    role: str

async def get_current_user(
    authorization: Annotated[Optional[str], Header()] = None,
) -> UserContext:
    """Extract and validate user from the Authorization header using Supabase.

    Accepts:
        Authorization: Bearer <jwt_token>
    """
    if not authorization:
        raise AuthenticationError("Authorization header required")

    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Invalid authorization header format. Use: Bearer <token>")

    token = authorization[7:]

    try:
        from backend.db.supabase import get_supabase_client
        client = get_supabase_client()
        # Verify token with Supabase Auth
        response = client.auth.get_user(token)
        if not response or not response.user:
            raise AuthenticationError("Invalid or expired token")
            
        user_id = response.user.id
        
        # Fetch profile to get workspace_id, company_id, and role
        profile_res = client.table("profiles").select("workspace_id, company_id, role").eq("id", user_id).single().execute()
        
        if not profile_res.data:
            raise AuthenticationError("User profile not found")
            
        profile = profile_res.data
        return UserContext(
            id=user_id,
            workspace_id=profile.get("workspace_id", ""),
            company_id=profile.get("company_id", ""),
            role=profile.get("role", "Viewer")
        )
    except Exception as e:
        logger.warning("jwt_decode_failed", error=str(e))
        raise AuthenticationError("Invalid or expired token")

async def get_current_user_id(
    user: Annotated[UserContext, Depends(get_current_user)]
) -> str:
    """Legacy dependency for routes that only need user_id"""
    return user.id

async def require_admin(
    user: Annotated[UserContext, Depends(get_current_user)],
) -> UserContext:
    """Dependency that requires the current user to be an admin or owner."""
    if user.role not in ["Owner", "Admin"]:
        raise AuthenticationError("Insufficient permissions")
    return user


def get_settings_dep() -> Settings:
    """Dependency wrapper for settings injection."""
    return get_settings()


# Type aliases for cleaner route signatures
CurrentUser = Annotated[UserContext, Depends(get_current_user)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
AdminUser = Annotated[UserContext, Depends(require_admin)]
AppSettings = Annotated[Settings, Depends(get_settings_dep)]
