"""
Echo — OCR Service
Extracts text from PDFs and images using PyMuPDF and EasyOCR.
"""

from __future__ import annotations

import io
from typing import List, Tuple

from backend.core.logging import get_logger

logger = get_logger(__name__)


class OCRService:
    """Handles text extraction from various document formats."""

    def __init__(self) -> None:
        self._easyocr_reader = None

    @property
    def easyocr_reader(self):
        """Lazy-load EasyOCR reader to avoid startup cost."""
        if self._easyocr_reader is None:
            try:
                import easyocr
                self._easyocr_reader = easyocr.Reader(["en"], gpu=False)
                logger.info("easyocr_initialized")
            except ImportError:
                logger.warning("easyocr_not_installed", message="EasyOCR not available, falling back to PyMuPDF only")
                self._easyocr_reader = None
        return self._easyocr_reader

    async def extract_text_from_pdf(self, file_bytes: bytes) -> Tuple[str, int]:
        """Extract text from a PDF file using PyMuPDF.

        Returns:
            Tuple of (extracted_text, page_count)
        """
        import fitz  # PyMuPDF

        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page_count = len(doc)
        pages_text: List[str] = []

        for page_num in range(page_count):
            page = doc[page_num]
            text = page.get_text("text")

            # If text extraction yields very little, try OCR on the page image
            if len(text.strip()) < 50:
                logger.debug("page_low_text", page=page_num + 1, chars=len(text.strip()))
                ocr_text = await self._ocr_page_image(page)
                if ocr_text:
                    text = ocr_text

            pages_text.append(f"[Page {page_num + 1}]\n{text}")

        doc.close()
        full_text = "\n\n".join(pages_text)
        logger.info("pdf_extracted", pages=page_count, chars=len(full_text))
        return full_text, page_count

    async def _ocr_page_image(self, page) -> str:
        """Run OCR on a PDF page rendered as an image."""
        reader = self.easyocr_reader
        if reader is None:
            return ""

        try:
            # Render page to image at 2x resolution for better OCR
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")

            results = reader.readtext(img_bytes, detail=0, paragraph=True)
            return "\n".join(results)
        except Exception as e:
            logger.warning("ocr_page_failed", error=str(e))
            return ""

    async def extract_text_from_image(self, file_bytes: bytes) -> str:
        """Extract text from an image file using EasyOCR."""
        reader = self.easyocr_reader
        if reader is None:
            logger.warning("ocr_unavailable")
            return ""

        try:
            results = reader.readtext(file_bytes, detail=0, paragraph=True)
            text = "\n".join(results)
            logger.info("image_ocr_completed", chars=len(text))
            return text
        except Exception as e:
            logger.error("image_ocr_failed", error=str(e))
            return ""

    async def extract_text_from_txt(self, file_bytes: bytes) -> str:
        """Extract text from a plain text file."""
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1")
        return text

    async def extract_text_from_csv(self, file_bytes: bytes) -> str:
        """Extract text from a CSV file, converting rows to readable format."""
        import csv

        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1")

        reader = csv.reader(io.StringIO(text))
        rows: List[str] = []
        headers: List[str] = []

        for i, row in enumerate(reader):
            if i == 0:
                headers = row
                rows.append(" | ".join(headers))
                rows.append("-" * 40)
            else:
                if headers:
                    row_text = " | ".join(f"{h}: {v}" for h, v in zip(headers, row))
                else:
                    row_text = " | ".join(row)
                rows.append(row_text)

        return "\n".join(rows)

    async def extract_text(self, file_bytes: bytes, file_type: str) -> Tuple[str, int]:
        """Route to the appropriate extraction method based on file type.

        Returns:
            Tuple of (extracted_text, page_count)
        """
        if file_type == "pdf":
            return await self.extract_text_from_pdf(file_bytes)
        elif file_type == "image":
            text = await self.extract_text_from_image(file_bytes)
            return text, 1
        elif file_type == "txt":
            text = await self.extract_text_from_txt(file_bytes)
            return text, 1
        elif file_type == "csv":
            text = await self.extract_text_from_csv(file_bytes)
            return text, 1
        elif file_type in ("docx", "xlsx", "pptx"):
            # For Office formats, attempt PyMuPDF which supports some
            try:
                import fitz
                doc = fitz.open(stream=file_bytes, filetype=file_type)
                text_parts = []
                for page in doc:
                    text_parts.append(page.get_text("text"))
                doc.close()
                text = "\n\n".join(text_parts)
                return text, len(text_parts)
            except Exception as e:
                logger.warning("office_extraction_failed", file_type=file_type, error=str(e))
                return "", 0
        else:
            logger.warning("unsupported_file_type", file_type=file_type)
            return "", 0
