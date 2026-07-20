"""
INDUS AI — API Middleware
Request logging, error handling, and CORS.
"""

from __future__ import annotations

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

from backend.core.logging import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.perf_counter()

        # Add context to logger
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time

            logger.info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(process_time * 1000, 2),
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except Exception as e:
            process_time = time.perf_counter() - start_time
            logger.error(
                "request_failed",
                error=str(e),
                duration_ms=round(process_time * 1000, 2),
                exc_info=True,
            )
            raise
        finally:
            structlog.contextvars.clear_contextvars()
