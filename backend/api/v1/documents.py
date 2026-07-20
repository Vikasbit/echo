"""
INDUS AI — Documents API
Endpoints for document management.
"""

from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from backend.schemas.documents import DocumentResponse, UploadStatusResponse
from backend.schemas.base import ApiResponse, PaginatedResponse
from backend.services.document_service import DocumentService
from backend.db.repositories.document_repo import DocumentRepository
from backend.core.dependencies import get_current_user_id

router = APIRouter()
doc_repo = DocumentRepository()


@router.post("/upload", response_model=ApiResponse[dict])
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    service = DocumentService()
    result = await service.upload_document(file, user_id)
    doc = result["doc"]
    
    # Queue processing
    background_tasks.add_task(
        service.process_document_background,
        document_id=doc["id"],
        file_bytes=result["file_bytes"],
        filename=file.filename or "",
        user_id=user_id
    )
    
    return ApiResponse(data={"document_id": doc["id"], "status": "processing"}, message="Upload accepted")


@router.get("", response_model=PaginatedResponse[DocumentResponse])
async def list_documents(
    page: int = 1,
    page_size: int = 20,
    user_id: str = Depends(get_current_user_id)
):
    result = await doc_repo.list_by_user(user_id, page=page, page_size=page_size)
    return PaginatedResponse(
        data=result["data"],
        total=result["total"],
        page=page,
        page_size=page_size
    )


@router.get("/{document_id}/status", response_model=ApiResponse[UploadStatusResponse])
async def get_document_status(
    document_id: str,
    user_id: str = Depends(get_current_user_id)
):
    doc = await doc_repo.get_by_id(document_id)
    if not doc or doc.get("user_id") != user_id:
        return ApiResponse(success=False, message="Document not found")
        
    return ApiResponse(data={
        "document_id": doc["id"],
        "status": doc["status"],
        "progress": 100 if doc["status"] == "indexed" else 50,
        "message": doc.get("error_message", ""),
        "metadata": doc.get("metadata", {})
    })


@router.delete("/{document_id}", response_model=ApiResponse[dict])
async def delete_document(
    document_id: str,
    user_id: str = Depends(get_current_user_id)
):
    doc = await doc_repo.get_by_id(document_id)
    if not doc or doc.get("user_id") != user_id:
        return ApiResponse(success=False, message="Document not found")
        
    await doc_repo.delete(document_id)
    return ApiResponse(message="Deleted successfully")
