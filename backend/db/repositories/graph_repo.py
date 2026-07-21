"""
Echo — Graph Repository
Data access layer for knowledge graph edges.
"""

from __future__ import annotations

from typing import Any, Dict, List

from backend.db.supabase import SupabaseRepository


class GraphRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("knowledge_edges")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        return result.data[0]

    async def get_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        result = self.table.select("*").eq("user_id", user_id).execute()
        return result.data

    async def get_by_node(self, node_id: str, node_type: str) -> List[Dict[str, Any]]:
        # Match where node is either source or target
        result = self.client.rpc(
            "get_node_edges",
            {"p_node_id": node_id, "p_node_type": node_type}
        ).execute()
        # Fallback if RPC doesn't exist yet, we just query OR condition via Python or Supabase syntax
        # Actually Supabase python client supports OR:
        result = self.table.select("*").or_(
            f"and(source_id.eq.{node_id},source_type.eq.{node_type}),and(target_id.eq.{node_id},target_type.eq.{node_type})"
        ).execute()
        return result.data

    async def delete_by_node(self, node_id: str) -> None:
        # Delete edges where this node is either source or target
        self.table.delete().or_(f"source_id.eq.{node_id},target_id.eq.{node_id}").execute()
