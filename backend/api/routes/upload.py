"""
Echo — Upload Routes
File upload and processing status endpoints.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, File, Form, UploadFile

from backend.core.config import get_settings
from backend.core.dependencies import CurrentUser
from backend.core.exceptions import FileTooLargeError, UnsupportedFileTypeError
from backend.core.logging import get_logger
from backend.schemas.base import ApiResponse
from backend.schemas.documents import DocumentResponse, UploadStatusResponse
from backend.services.document_service import DocumentService
from backend.utils.file_utils import is_supported_file, validate_file_size

logger = get_logger(__name__)
router = APIRouter(prefix="/upload", tags=["Upload"])

settings = get_settings()
doc_service = DocumentService()


@router.post("", response_model=ApiResponse[DocumentResponse])
async def upload_file(
    user_id: CurrentUser,
    file: UploadFile = File(...),
    category: Optional[str] = Form(default=None),
    equipment_tags: Optional[str] = Form(default=None),
):
    """Upload a single document for processing.

    The file will be validated, then processed through the pipeline:
    Upload → OCR → Chunk → Embed → Index
    """
    if not file.filename:
        raise UnsupportedFileTypeError("No filename provided")

    if not is_supported_file(file.filename):
        raise UnsupportedFileTypeError(file.filename.rsplit(".", 1)[-1])

    # Read file contents
    file_bytes = await file.read()

    if not validate_file_size(len(file_bytes), settings.upload_max_size_mb):
        raise FileTooLargeError(settings.upload_max_size_mb)

    # Parse equipment tags from comma-separated string
    tags: List[str] = []
    if equipment_tags:
        tags = [t.strip() for t in equipment_tags.split(",") if t.strip()]

    logger.info(
        "file_upload_started",
        filename=file.filename,
        size=len(file_bytes),
        category=category,
    )

    # Process the document
    document = await doc_service.process_document(
        user_id=user_id,
        file_bytes=file_bytes,
        filename=file.filename,
        content_type=file.content_type,
        category=category,
        equipment_tags=tags,
    )

    return ApiResponse(
        data=DocumentResponse(**document),
        message="Document uploaded and processed successfully",
    )


@router.post("/batch", response_model=ApiResponse[list[DocumentResponse]])
async def upload_batch(
    user_id: CurrentUser,
    files: List[UploadFile] = File(...),
    category: Optional[str] = Form(default=None),
):
    """Upload multiple documents at once."""
    results: List[DocumentResponse] = []

    for file in files:
        if not file.filename or not is_supported_file(file.filename):
            logger.warning("batch_skip_unsupported", filename=file.filename)
            continue

        file_bytes = await file.read()

        if not validate_file_size(len(file_bytes), settings.upload_max_size_mb):
            logger.warning("batch_skip_too_large", filename=file.filename)
            continue

        try:
            document = await doc_service.process_document(
                user_id=user_id,
                file_bytes=file_bytes,
                filename=file.filename,
                content_type=file.content_type,
                category=category,
            )
            results.append(DocumentResponse(**document))
        except Exception as e:
            logger.error("batch_file_failed", filename=file.filename, error=str(e))

    return ApiResponse(
        data=results,
        message=f"Processed {len(results)} of {len(files)} files",
    )


@router.get("/{document_id}/status", response_model=ApiResponse[UploadStatusResponse])
async def get_upload_status(document_id: str, user_id: CurrentUser):
    """Check the processing status of an uploaded document."""
    doc = await doc_service.get_document(document_id)

    status_progress = {
        "uploading": 10,
        "processing": 30,
        "ocr": 50,
        "embedding": 75,
        "indexed": 100,
        "failed": 0,
    }

    status_messages = {
        "uploading": "Uploading file...",
        "processing": "Processing document...",
        "ocr": "Extracting text with OCR...",
        "embedding": "Generating AI embeddings...",
        "indexed": "Document indexed and ready",
        "failed": "Processing failed",
    }

    current_status = doc.get("status", "uploading")

    return ApiResponse(
        data=UploadStatusResponse(
            document_id=doc["id"],
            status=current_status,
            progress=status_progress.get(current_status, 0),
            message=status_messages.get(current_status, "Unknown status"),
        )
    )
