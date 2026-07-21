"""
Echo — Custom Exceptions
Application-specific error classes with HTTP status mapping.
"""

from __future__ import annotations

from typing import Any, Optional


class IndusAIException(Exception):
    """Base exception for all Echo errors."""

    def __init__(
        self,
        message: str = "An unexpected error occurred",
        status_code: int = 500,
        detail: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


class AuthenticationError(IndusAIException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message=message, status_code=401)


class AuthorizationError(IndusAIException):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message=message, status_code=403)


class NotFoundError(IndusAIException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str = "Resource", resource_id: str = "") -> None:
        msg = f"{resource} not found"
        if resource_id:
            msg = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=msg, status_code=404)


class ValidationError(IndusAIException):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation failed", detail: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=422, detail=detail)


class ConflictError(IndusAIException):
    """Raised when a resource already exists."""

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(message=message, status_code=409)


class RateLimitError(IndusAIException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded. Please try again later.") -> None:
        super().__init__(message=message, status_code=429)


class ExternalServiceError(IndusAIException):
    """Raised when an external API call fails (OpenAI, Supabase, etc.)."""

    def __init__(self, service: str, message: str = "") -> None:
        msg = f"External service error: {service}"
        if message:
            msg = f"{msg} — {message}"
        super().__init__(message=msg, status_code=502)


class FileProcessingError(IndusAIException):
    """Raised when document processing fails (OCR, chunking, embedding)."""

    def __init__(self, message: str = "File processing failed", detail: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=500, detail=detail)


class FileTooLargeError(IndusAIException):
    """Raised when upload exceeds size limit."""

    def __init__(self, max_mb: int = 50) -> None:
        super().__init__(
            message=f"File exceeds maximum size of {max_mb}MB",
            status_code=413,
        )


class UnsupportedFileTypeError(IndusAIException):
    """Raised when file type is not supported."""

    def __init__(self, file_type: str) -> None:
        super().__init__(
            message=f"Unsupported file type: {file_type}",
            status_code=415,
        )
