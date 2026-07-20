"""
INDUS AI — Activity Repository
Data access layer for user activity logs.
"""

from __future__ import annotations

from typing import Any, Dict, List

from backend.db.supabase import SupabaseRepository


class ActivityRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("activity_log")

    async def log_activity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        return result.data[0]

    async def get_recent_activity(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        result = (
            self.table.select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data
