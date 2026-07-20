"""
INDUS AI — Middleware
Request logging, timing, and error handling middleware.
"""

from __future__ import annotations

import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from backend.core.exceptions import IndusAIException
from backend.core.logging import get_logger

logger = get_logger(__name__)


def register_middleware(app: FastAPI) -> None:
    """Register all middleware on the FastAPI application."""

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next: Callable) -> Response:
        """Log every request with timing, method, path, and status."""
        request_id = str(uuid.uuid4())[:8]
        start_time = time.perf_counter()

        # Inject request_id into structlog context
        import structlog
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else "unknown",
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                "request_failed",
                method=request.method,
                path=request.url.path,
                duration_ms=duration_ms,
                error=str(exc),
            )
            raise

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=duration_ms,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration_ms}ms"

        return response


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""

    @app.exception_handler(IndusAIException)
    async def indus_exception_handler(request: Request, exc: IndusAIException) -> JSONResponse:
        """Handle all custom INDUS AI exceptions."""
        logger.warning(
            "handled_error",
            status_code=exc.status_code,
            message=exc.message,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "detail": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch-all handler for unhandled exceptions."""
        logger.error(
            "unhandled_error",
            error=str(exc),
            error_type=type(exc).__name__,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "An unexpected error occurred",
                "detail": str(exc) if not isinstance(exc, Exception) else None,
            },
        )

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": f"Route not found: {request.method} {request.url.path}",
            },
        )
