"""
INDUS AI — File Utilities
File type detection, validation, and processing helpers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Set

SUPPORTED_EXTENSIONS: Set[str] = {
    ".pdf", ".docx", ".doc", ".xlsx", ".xls",
    ".pptx", ".ppt", ".txt", ".csv",
    ".png", ".jpg", ".jpeg", ".tiff", ".bmp",
}

MIME_TO_TYPE: dict[str, str] = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/msword": "docx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-excel": "xlsx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/vnd.ms-powerpoint": "pptx",
    "text/plain": "txt",
    "text/csv": "csv",
    "image/png": "image",
    "image/jpeg": "image",
    "image/tiff": "image",
    "image/bmp": "image",
}


def get_file_extension(filename: str) -> str:
    """Extract the file extension in lowercase."""
    return Path(filename).suffix.lower()


def get_file_type(filename: str, content_type: str | None = None) -> str:
    """Determine the document type from filename or MIME type."""
    if content_type and content_type in MIME_TO_TYPE:
        return MIME_TO_TYPE[content_type]

    ext = get_file_extension(filename)
    ext_map: dict[str, str] = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".doc": "docx",
        ".xlsx": "xlsx",
        ".xls": "xlsx",
        ".pptx": "pptx",
        ".ppt": "pptx",
        ".txt": "txt",
        ".csv": "csv",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
        ".tiff": "image",
        ".bmp": "image",
    }
    return ext_map.get(ext, "unknown")


def is_supported_file(filename: str) -> bool:
    """Check if the file extension is supported."""
    return get_file_extension(filename) in SUPPORTED_EXTENSIONS


def validate_file_size(size_bytes: int, max_mb: int = 50) -> bool:
    """Validate that file size is within the allowed limit."""
    return size_bytes <= max_mb * 1024 * 1024


def format_file_size(size_bytes: int) -> str:
    """Format bytes into a human-readable string."""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB"]
    k = 1024
    for unit in units:
        if size_bytes < k:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= k
    return f"{size_bytes:.1f} TB"


def sanitize_filename(filename: str) -> str:
    """Remove potentially dangerous characters from filenames."""
    keep = {" ", ".", "-", "_"}
    sanitized = "".join(c for c in filename if c.isalnum() or c in keep)
    return sanitized.strip()
