"""
Echo — Equipment Repository
Data access layer for equipment and maintenance events.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.core.logging import get_logger
from backend.db.supabase import SupabaseRepository

logger = get_logger(__name__)


class EquipmentRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("equipment")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        logger.info("equipment_created", equipment_id=result.data[0]["id"])
        return result.data[0]

    async def get_by_id(self, equipment_id: str) -> Optional[Dict[str, Any]]:
        result = self.table.select("*").eq("id", equipment_id).maybe_single().execute()
        return result.data

    async def list_by_user(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 20,
        equipment_type: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = self.table.select("*", count="exact").eq("user_id", user_id)

        if equipment_type:
            query = query.eq("type", equipment_type)
        if status:
            query = query.eq("status", status)
        if search:
            query = query.ilike("name", f"%{search}%")

        offset = (page - 1) * page_size
        query = query.order("created_at", desc=True).range(offset, offset + page_size - 1)

        result = query.execute()
        return {
            "data": result.data,
            "total": result.count or 0,
            "page": page,
            "page_size": page_size,
        }

    async def update(self, equipment_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.update(data).eq("id", equipment_id).execute()
        return result.data[0] if result.data else {}

    async def delete(self, equipment_id: str) -> bool:
        self.table.delete().eq("id", equipment_id).execute()
        logger.info("equipment_deleted", equipment_id=equipment_id)
        return True

    async def get_stats(self, user_id: str) -> Dict[str, int]:
        total = self.table.select("id", count="exact").eq("user_id", user_id).execute()
        critical = (
            self.table.select("id", count="exact")
            .eq("user_id", user_id)
            .in_("status", ["critical", "warning"])
            .execute()
        )
        return {
            "total": total.count or 0,
            "alerts": critical.count or 0,
        }


class MaintenanceRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("maintenance_events")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        return result.data[0]

    async def get_by_equipment(self, equipment_id: str) -> List[Dict[str, Any]]:
        result = (
            self.table.select("*")
            .eq("equipment_id", equipment_id)
            .order("event_date", desc=True)
            .execute()
        )
        return result.data

    async def get_recent(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        result = (
            self.table.select("*, equipment!inner(user_id, name)")
            .eq("equipment.user_id", user_id)
            .order("event_date", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data
