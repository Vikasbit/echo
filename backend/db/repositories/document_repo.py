"""
Echo — Document Repository
Data access layer for documents and document chunks.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.core.logging import get_logger
from backend.db.supabase import SupabaseRepository

logger = get_logger(__name__)


class DocumentRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("documents")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.insert(data).execute()
        logger.info("document_created", document_id=result.data[0]["id"])
        return result.data[0]

    async def get_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        result = self.table.select("*").eq("id", document_id).maybe_single().execute()
        return result.data

    async def list_by_user(
        self,
        workspace_id: str,
        page: int = 1,
        page_size: int = 20,
        category: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        query = self.table.select("*", count="exact").eq("workspace_id", workspace_id)

        if category:
            query = query.eq("category", category)
        if status:
            query = query.eq("status", status)
        if search:
            query = query.ilike("title", f"%{search}%")

        offset = (page - 1) * page_size
        query = query.order("created_at", desc=True).range(offset, offset + page_size - 1)

        result = query.execute()
        return {
            "data": result.data,
            "total": result.count or 0,
            "page": page,
            "page_size": page_size,
        }

    async def update(self, document_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.table.update(data).eq("id", document_id).execute()
        return result.data[0] if result.data else {}

    async def delete(self, document_id: str) -> bool:
        self.table.delete().eq("id", document_id).execute()
        logger.info("document_deleted", document_id=document_id)
        return True

    async def update_status(self, document_id: str, status: str) -> None:
        self.table.update({"status": status}).eq("id", document_id).execute()

    async def get_stats(self, user_id: str) -> Dict[str, int]:
        total = self.table.select("id", count="exact").eq("user_id", user_id).execute()
        indexed = (
            self.table.select("id", count="exact")
            .eq("user_id", user_id)
            .eq("status", "indexed")
            .execute()
        )
        processing = (
            self.table.select("id", count="exact")
            .eq("user_id", user_id)
            .eq("status", "processing")
            .execute()
        )
        return {
            "total": total.count or 0,
            "indexed": indexed.count or 0,
            "processing": processing.count or 0,
        }


class ChunkRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("document_chunks")

    async def create_many(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = self.table.insert(chunks).execute()
        logger.info("chunks_created", count=len(result.data))
        return result.data

    async def get_by_document(self, document_id: str) -> List[Dict[str, Any]]:
        result = (
            self.table.select("*")
            .eq("document_id", document_id)
            .order("chunk_index")
            .execute()
        )
        return result.data

    async def delete_by_document(self, document_id: str) -> None:
        self.table.delete().eq("document_id", document_id).execute()

    async def similarity_search(
        self,
        query_embedding: List[float],
        user_id: str,
        top_k: int = 8,
    ) -> List[Dict[str, Any]]:
        """Perform vector similarity search using pgvector via Supabase RPC."""
        result = self.client.rpc(
            "match_chunks",
            {
                "query_embedding": query_embedding,
                "match_count": top_k,
                "filter_user_id": user_id,
            },
        ).execute()
        return result.data
