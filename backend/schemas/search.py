"""
INDUS AI — Search Schemas
Request and response models for the unified command palette search.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    limit: int = Field(default=10, ge=1, le=50)


class SearchResultItem(BaseModel):
    id: str
    type: str  # document | equipment | conversation
    title: str
    excerpt: str
    relevance: float
    url: Optional[str] = None


class SearchResponse(BaseModel):
    results: List[SearchResultItem] = Field(default_factory=list)
    query_time_ms: float = 0.0
