"""
INDUS AI — Dependency Injection
FastAPI dependencies for authentication, database access, and service injection.
"""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, Header
from jose import JWTError

from backend.core.config import Settings, get_settings
from backend.core.exceptions import AuthenticationError
from backend.core.logging import get_logger
from backend.core.security import decode_access_token

logger = get_logger(__name__)


async def get_current_user_id(
    authorization: Annotated[Optional[str], Header()] = None,
) -> str:
    """Extract and validate user ID from the Authorization header.

    Accepts:
        Authorization: Bearer <jwt_token>

    For demo mode, if no token is provided, returns a demo user ID.
    """
    if not authorization:
        # Demo mode fallback
        return "demo-user-001"

    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Invalid authorization header format. Use: Bearer <token>")

    token = authorization[7:]

    try:
        from backend.db.supabase import get_supabase_client
        client = get_supabase_client()
        # In a real app we'd want to use a fresh client per request or handle the token properly
        # For this prototype we can decode it with jose using Supabase's JWT secret,
        # or just call auth.get_user. Note: setting session on the global client is not thread-safe in python.
        # But `client.auth.get_user(token)` can work if supported by the SDK version.
        # Actually, python-jose is fine if we use the correct JWT secret.
        # Let's decode locally using settings.jwt_secret_key which should be set to Supabase JWT secret.
        payload = decode_access_token(token)
    except JWTError as e:
        logger.warning("jwt_decode_failed", error=str(e))
        raise AuthenticationError("Invalid or expired token")

    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Token payload missing user identifier")

    return user_id


async def require_admin(
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> str:
    """Dependency that requires the current user to be an admin.

    In production, this would check the user's role in the database.
    For demo, we allow all authenticated users.
    """
    return user_id


def get_settings_dep() -> Settings:
    """Dependency wrapper for settings injection."""
    return get_settings()


# Type aliases for cleaner route signatures
CurrentUser = Annotated[str, Depends(get_current_user_id)]
AdminUser = Annotated[str, Depends(require_admin)]
AppSettings = Annotated[Settings, Depends(get_settings_dep)]
