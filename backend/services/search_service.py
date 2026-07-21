"""
Echo — Search Service
Vector similarity search using pgvector through Supabase.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.core.logging import get_logger
from backend.db.repositories.document_repo import ChunkRepository
from backend.services.embedding_service import EmbeddingService

logger = get_logger(__name__)


class SearchService:
    """Performs semantic search over document chunks using vector similarity."""

    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.chunk_repo = ChunkRepository()

    async def semantic_search(
        self,
        query: str,
        user_id: str,
        top_k: int = 8,
        min_score: float = 0.3,
    ) -> List[Dict[str, Any]]:
        """Search for relevant document chunks using embedding similarity.

        Args:
            query: The user's search query.
            user_id: Filter results to this user's documents.
            top_k: Number of results to return.
            min_score: Minimum similarity score threshold.

        Returns:
            List of matching chunks with metadata and scores.
        """
        logger.info("semantic_search_started", query=query[:100], top_k=top_k)

        # Generate query embedding
        query_embedding = await self.embedding_service.embed_text(query)

        # Search via pgvector
        results = await self.chunk_repo.similarity_search(
            query_embedding=query_embedding,
            user_id=user_id,
            top_k=top_k,
        )

        # Filter by minimum score
        filtered = [r for r in results if r.get("similarity", 0) >= min_score]

        logger.info(
            "semantic_search_completed",
            total_results=len(results),
            filtered_results=len(filtered),
        )

        return filtered

    async def hybrid_search(
        self,
        query: str,
        user_id: str,
        top_k: int = 10,
        category: Optional[str] = None,
        file_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Combine semantic search with metadata filtering.

        First performs vector similarity search, then applies
        additional filters on category and file type.
        """
        # Get more results than needed so we can filter
        raw_results = await self.semantic_search(
            query=query,
            user_id=user_id,
            top_k=top_k * 2,
            min_score=0.25,
        )

        filtered = raw_results
        if category:
            filtered = [r for r in filtered if r.get("category") == category]
        if file_type:
            filtered = [r for r in filtered if r.get("file_type") == file_type]

        return filtered[:top_k]
