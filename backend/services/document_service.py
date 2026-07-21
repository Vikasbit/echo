"""
Echo — Document Service
Async document processing pipeline.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict

from fastapi import UploadFile

from backend.core.config import get_settings
from backend.core.logging import get_logger
from backend.db.repositories.document_repo import DocumentRepository, ChunkRepository
from backend.db.supabase import get_supabase_client
from backend.services.ocr_service import OCRService
from backend.services.embedding_service import EmbeddingService
from backend.utils.file_utils import get_file_type
from backend.utils.text_utils import chunk_text

logger = get_logger(__name__)
settings = get_settings()


class DocumentService:
    def __init__(self) -> None:
        self.doc_repo = DocumentRepository()
        self.chunk_repo = ChunkRepository()
        self.ocr_service = OCRService()
        self.embedding_service = EmbeddingService()
        self.client = get_supabase_client()

    async def process_document_background(self, document_id: str, file_bytes: bytes, filename: str, user_id: str) -> None:
        """
        Background task to run OCR, AI analysis, chunking, and embedding.
        """
        try:
            logger.info("starting_document_processing", document_id=document_id)
            await self.doc_repo.update_status(document_id, "processing")
            
            # Extract Text
            file_type = get_file_type(filename)
            await self.doc_repo.update_status(document_id, "ocr")
            extracted_text, page_count = await self.ocr_service.extract_text(file_bytes, file_type)
            
            if not extracted_text.strip():
                raise ValueError("No text could be extracted from the document.")

            # AI Document Analysis (Metadata Extraction)
            await self.doc_repo.update_status(document_id, "analyzing")
            from openai import AsyncOpenAI
            openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
            
            # Use gpt-4o-mini for speed/cost on analysis
            system_prompt = (
                "You are an AI document analysis engine. Analyze the following document text "
                "and extract the requested information as a JSON object with the exact keys: "
                "DocumentType, DocumentTitle, EquipmentName, EquipmentID, Manufacturer, Department, "
                "Summary, Keywords, Components, ErrorCodes, MaintenanceActions, SafetyWarnings, Dates, RevisionNumber. "
                "If a field is not found or not applicable, use null or an empty list. "
                "Return valid JSON only."
            )
            
            # We only send the first ~8000 chars to save cost and time for metadata extraction
            analysis_text = extracted_text[:8000]
            
            completion = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": analysis_text}
                ],
                response_format={ "type": "json_object" },
                temperature=0.1
            )
            
            import json
            try:
                ai_metadata = json.loads(completion.choices[0].message.content or "{}")
            except json.JSONDecodeError:
                ai_metadata = {}

            # Chunk Text with page preservation
            from backend.utils.text_utils import chunk_document_pages
            chunks_with_pages = chunk_document_pages(
                extracted_text, 
                chunk_size=settings.chunk_size, 
                chunk_overlap=settings.chunk_overlap
            )
            
            if not chunks_with_pages:
                raise ValueError("Document yielded zero chunks.")

            # Embed and Store Chunks
            await self.doc_repo.update_status(document_id, "embedding")
            chunk_contents = [c["content"] for c in chunks_with_pages]
            embeddings = await self.embedding_service.embed_batch(chunk_contents)
            
            chunk_records = []
            for i, (chunk_data, embedding) in enumerate(zip(chunks_with_pages, embeddings)):
                chunk_records.append({
                    "document_id": document_id,
                    "user_id": user_id,
                    "chunk_index": i,
                    "content": chunk_data["content"],
                    "page_number": chunk_data["page_number"],
                    "embedding": embedding
                })
            
            await self.chunk_repo.create_many(chunk_records)
            
            await self.doc_repo.update(document_id, {
                "status": "indexed",
                "page_count": page_count,
                "summary": ai_metadata.get("Summary") or (extracted_text[:200] + "..."),
                "metadata": ai_metadata,
                "error_message": None
            })
            
            logger.info("document_processing_complete", document_id=document_id)
            
        except Exception as e:
            logger.error("document_processing_failed", document_id=document_id, error=str(e))
            await self.doc_repo.update(document_id, {
                "status": "failed",
                "error_message": str(e)
            })

    async def upload_document(self, file: UploadFile, user_id: str) -> Dict[str, Any]:
        file_bytes = await file.read()
        file_type = get_file_type(file.filename or "")
        
        doc_data = {
            "user_id": user_id,
            "title": file.filename or "Untitled",
            "file_type": file_type,
            "file_size": len(file_bytes),
            "status": "uploading"
        }
        
        doc = await self.doc_repo.create(doc_data)
        
        return {"doc": doc, "file_bytes": file_bytes}
