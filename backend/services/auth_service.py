"""
INDUS AI — Auth Service
Handles authentication using Supabase Auth.
"""

from __future__ import annotations

from typing import Any, Dict

from backend.db.supabase import get_supabase_client
from backend.core.exceptions import AuthenticationError


class AuthService:
    def __init__(self) -> None:
        self.client = get_supabase_client()

    async def register(self, email: str, password: str, full_name: str, organization: str) -> Dict[str, Any]:
        response = self.client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name,
                    "organization": organization
                }
            }
        })
        if response.user:
            return {
                "id": response.user.id,
                "email": response.user.email,
                "full_name": full_name,
                "organization": organization
            }
        raise AuthenticationError("Registration failed")

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if response.session:
                return {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_in": response.session.expires_in,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "full_name": response.user.user_metadata.get("full_name", ""),
                        "organization": response.user.user_metadata.get("organization", "")
                    }
                }
            raise AuthenticationError("Login failed")
        except Exception as e:
            raise AuthenticationError(f"Login failed: {str(e)}")

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        try:
            response = self.client.auth.refresh_session(refresh_token)
            if response.session:
                return {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_in": response.session.expires_in
                }
            raise AuthenticationError("Token refresh failed")
        except Exception as e:
            raise AuthenticationError(f"Token refresh failed: {str(e)}")
