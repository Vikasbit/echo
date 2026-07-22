""""
Echo — Main Application Entry Point
FastAPI app configuration, middleware injection, and router mounting.
"""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from core.logging import setup_logging
from core.middleware import RequestLoggingMiddleware
from api.v1.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the FastAPI application."""
    setup_logging(
        log_level="DEBUG" if settings.app_debug else "INFO",
        json_format=not settings.app_debug,
    )

    logger = structlog.get_logger(__name__)
    logger.info(
        "startup",
        app_name=settings.app_name,
        env=settings.app_env,
    )

    # Initialize database connections, AI models, caches, etc.
    yield

    # Cleanup
    logger.info("shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Industrial Knowledge Intelligence Platform API",
    lifespan=lifespan,
    docs_url="/docs" if settings.app_debug else None,
    redoc_url="/redoc" if settings.app_debug else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
app.add_middleware(RequestLoggingMiddleware)

# API Routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "status": "running",
        "version": settings.app_version,
        "docs": "/docs" if settings.app_debug else "disabled",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.app_env,
    }