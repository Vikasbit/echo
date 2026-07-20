"""
INDUS AI — Document Routes
CRUD and search endpoints for documents.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from backend.core.dependencies import CurrentUser
from backend.core.logging import get_logger
from backend.schemas.base import ApiResponse, PaginatedResponse
from backend.schemas.documents import DocumentResponse, DocumentSearchRequest, DocumentSearchResult
from backend.services.document_service import DocumentService
from backend.services.search_service import SearchService

logger = get_logger(__name__)
router = APIRouter(prefix="/documents", tags=["Documents"])

doc_service = DocumentService()
search_service = SearchService()


@router.get("", response_model=PaginatedResponse[DocumentResponse])
async def list_documents(
    user_id: CurrentUser,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    category: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
):
    """List documents with pagination and optional filters."""
    result = await doc_service.list_documents(
        user_id=user_id,
        page=page,
        page_size=page_size,
        category=category,
        status=status,
        search=search,
    )

    documents = [DocumentResponse(**doc) for doc in result["data"]]

    return PaginatedResponse(
        data=documents,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result.get("total_pages", 0),
    )


@router.get("/search", response_model=ApiResponse[list[DocumentSearchResult]])
async def search_documents(
    user_id: CurrentUser,
    query: str = Query(min_length=1, max_length=500),
    category: Optional[str] = Query(default=None),
    file_type: Optional[str] = Query(default=None),
    top_k: int = Query(default=10, ge=1, le=50),
):
    """Semantic search across all indexed documents."""
    results = await search_service.hybrid_search(
        query=query,
        user_id=user_id,
        top_k=top_k,
        category=category,
        file_type=file_type,
    )

    search_results = [
        DocumentSearchResult(
            document_id=r.get("document_id", ""),
            document_title=r.get("document_title", "Unknown"),
            chunk_content=r.get("content", ""),
            page_number=r.get("page_number"),
            relevance_score=round(r.get("similarity", 0), 3),
            category=r.get("category"),
        )
        for r in results
    ]

    return ApiResponse(data=search_results)


@router.get("/{document_id}", response_model=ApiResponse[DocumentResponse])
async def get_document(document_id: str, user_id: CurrentUser):
    """Get a single document by ID."""
    doc = await doc_service.get_document(document_id)
    return ApiResponse(data=DocumentResponse(**doc))


@router.delete("/{document_id}", response_model=ApiResponse)
async def delete_document(document_id: str, user_id: CurrentUser):
    """Delete a document and all its processed chunks."""
    await doc_service.delete_document(document_id)
    return ApiResponse(message="Document deleted successfully")


@router.get("/{document_id}/summary", response_model=ApiResponse[dict])
async def get_document_summary(document_id: str, user_id: CurrentUser):
    """Get the AI-generated summary for a document."""
    doc = await doc_service.get_document(document_id)
    return ApiResponse(
        data={
            "document_id": doc["id"],
            "title": doc.get("title", ""),
            "summary": doc.get("summary", "No summary available."),
            "page_count": doc.get("page_count", 0),
            "category": doc.get("category", ""),
        }
    )
