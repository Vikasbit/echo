"""
INDUS AI — Base Schemas
Shared Pydantic models used across the API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool = True
    message: str = "OK"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    message: str
    detail: Optional[Any] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""

    success: bool = True
    data: List[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20
    total_pages: int = 0


class PaginationParams(BaseModel):
    """Pagination query parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class TimestampMixin(BaseModel):
    """Mixin for created_at/updated_at fields."""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
