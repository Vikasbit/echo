"""
Echo — Dashboard Service
Aggregates statistics and chart data.
"""

from __future__ import annotations

from typing import Any, Dict

from backend.db.repositories.document_repo import DocumentRepository
from backend.db.repositories.equipment_repo import EquipmentRepository
from backend.db.repositories.conversation_repo import ConversationRepository
from backend.db.repositories.activity_repo import ActivityRepository

class DashboardService:
    def __init__(self) -> None:
        self.doc_repo = DocumentRepository()
        self.equip_repo = EquipmentRepository()
        self.conv_repo = ConversationRepository()
        self.activity_repo = ActivityRepository()

    async def get_stats(self, user_id: str) -> Dict[str, Any]:
        docs = await self.doc_repo.get_stats(user_id)
        equips = await self.equip_repo.get_stats(user_id)
        queries = await self.conv_repo.get_count(user_id)
        
        return {
            "total_documents": docs["total"],
            "total_equipment": equips["total"],
            "total_queries": queries,
            "active_alerts": equips["alerts"],
            "documents_change": 12.5,  # Mock delta
            "equipment_change": 0.0,
            "queries_change": 24.8,
            "alerts_change": -5.0
        }

    async def get_activity(self, user_id: str, limit: int = 10) -> Dict[str, Any]:
        activities = await self.activity_repo.get_recent_activity(user_id, limit)
        return {"data": activities}
        
    async def get_charts(self, user_id: str) -> Dict[str, Any]:
        # Mock chart data for MVP
        return {
            "document_types": [
                {"label": "PDF", "value": 65},
                {"label": "Word", "value": 20},
                {"label": "Images", "value": 15}
            ],
            "query_volume": [
                {"label": "Mon", "value": 12},
                {"label": "Tue", "value": 19},
                {"label": "Wed", "value": 15},
                {"label": "Thu", "value": 22},
                {"label": "Fri", "value": 30},
                {"label": "Sat", "value": 8},
                {"label": "Sun", "value": 5}
            ],
            "top_categories": [
                {"label": "Maintenance", "value": 45},
                {"label": "Safety", "value": 30},
                {"label": "Engineering", "value": 25}
            ]
        }
