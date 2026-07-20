"""
INDUS AI — User Repository
Data access layer for user profiles.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from backend.core.logging import get_logger
from backend.db.supabase import SupabaseRepository

logger = get_logger(__name__)


class UserRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("profiles")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        logger.info("user_created", user_id=result.data[0]["id"])
        return result.data[0]

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        result = self.table.select("*").eq("id", user_id).maybe_single().execute()
        return result.data

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        result = self.table.select("*").eq("email", email).maybe_single().execute()
        return result.data

    async def update(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.update(data).eq("id", user_id).execute()
        return result.data[0] if result.data else {}

    async def exists(self, email: str) -> bool:
        result = self.table.select("id").eq("email", email).maybe_single().execute()
        return result.data is not None
