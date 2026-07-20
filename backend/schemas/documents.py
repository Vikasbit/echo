"""
INDUS AI — Document Schemas
Request and response models for document endpoints.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    PPTX = "pptx"
    TXT = "txt"
    CSV = "csv"
    IMAGE = "image"


class ProcessingStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    OCR = "ocr"
    EMBEDDING = "embedding"
    INDEXED = "indexed"
    FAILED = "failed"


class DocumentResponse(BaseModel):
    id: str
    title: str
    file_type: str
    file_url: Optional[str] = None
    file_size: int = 0
    page_count: int = 0
    category: Optional[str] = None
    status: str = "uploading"
    summary: Optional[str] = None
    equipment_tags: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class DocumentCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    category: Optional[str] = None
    equipment_tags: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None


class DocumentUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    category: Optional[str] = None
    equipment_tags: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class DocumentSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    category: Optional[str] = None
    file_type: Optional[str] = None
    top_k: int = Field(default=10, ge=1, le=50)


class DocumentSearchResult(BaseModel):
    document_id: str
    document_title: str
    chunk_content: str
    page_number: Optional[int] = None
    relevance_score: float
    category: Optional[str] = None


class UploadStatusResponse(BaseModel):
    document_id: str
    status: str
    progress: int = 0
    message: str = ""
    metadata: Optional[dict] = None
