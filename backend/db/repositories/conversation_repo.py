"""
Echo — Conversation Repository
Data access layer for conversations and messages.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.core.logging import get_logger
from backend.db.supabase import SupabaseRepository

logger = get_logger(__name__)


class ConversationRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("conversations")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        logger.info("conversation_created", conversation_id=result.data[0]["id"])
        return result.data[0]

    async def get_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        result = self.table.select("*").eq("id", conversation_id).maybe_single().execute()
        return result.data

    async def list_by_user(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        result = (
            self.table.select("*")
            .eq("user_id", user_id)
            .order("updated_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data

    async def update(self, conversation_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.update(data).eq("id", conversation_id).execute()
        return result.data[0] if result.data else {}

    async def delete(self, conversation_id: str) -> bool:
        self.table.delete().eq("id", conversation_id).execute()
        logger.info("conversation_deleted", conversation_id=conversation_id)
        return True

    async def get_count(self, user_id: str) -> int:
        result = self.table.select("id", count="exact").eq("user_id", user_id).execute()
        return result.count or 0


class MessageRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("messages")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        return result.data[0]

    async def get_by_conversation(
        self,
        conversation_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        result = (
            self.table.select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at", desc=False)
            .limit(limit)
            .execute()
        )
        return result.data

    async def get_count(self, conversation_id: str) -> int:
        result = (
            self.table.select("id", count="exact")
            .eq("conversation_id", conversation_id)
            .execute()
        )
        return result.count or 0
