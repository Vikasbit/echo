"""
INDUS AI — Graph Service
Knowledge graph entity and edge management.
"""

from __future__ import annotations

from typing import Any, Dict, List

from backend.core.logging import get_logger
from backend.db.repositories.graph_repo import GraphRepository
from backend.db.repositories.document_repo import DocumentRepository
from backend.db.repositories.equipment_repo import EquipmentRepository

logger = get_logger(__name__)


class GraphService:
    def __init__(self) -> None:
        self.graph_repo = GraphRepository()
        self.doc_repo = DocumentRepository()
        self.equip_repo = EquipmentRepository()

    async def get_full_graph(self, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get nodes and edges for the user's knowledge graph."""
        # 1. Fetch Edges
        edges = await self.graph_repo.get_by_user(user_id)
        
        # 2. Extract unique node IDs from edges
        node_refs = set()
        for e in edges:
            node_refs.add((e["source_id"], e["source_type"]))
            node_refs.add((e["target_id"], e["target_type"]))
            
        nodes = []
        
        # In a real app we'd bulk query nodes by ID and Type.
        # For MVP we can just pull all docs and equipment and map them.
        docs = await self.doc_repo.table.select("id, title, category").eq("user_id", user_id).execute()
        equips = await self.equip_repo.table.select("id, name, type").eq("user_id", user_id).execute()
        
        doc_map = {str(d["id"]): d for d in docs.data}
        equip_map = {str(e["id"]): e for e in equips.data}
        
        for ref_id, ref_type in node_refs:
            if ref_type == "document" and ref_id in doc_map:
                d = doc_map[ref_id]
                nodes.append({
                    "id": ref_id,
                    "type": "document",
                    "label": d["title"],
                    "metadata": {"category": d.get("category", "")}
                })
            elif ref_type == "equipment" and ref_id in equip_map:
                e = equip_map[ref_id]
                nodes.append({
                    "id": ref_id,
                    "type": "equipment",
                    "label": e["name"],
                    "metadata": {"equipment_type": e.get("type", "")}
                })
            else:
                # Ghost node
                nodes.append({
                    "id": ref_id,
                    "type": ref_type,
                    "label": f"Unknown {ref_type}",
                    "metadata": {}
                })
                
        return {
            "nodes": nodes,
            "edges": edges
        }
