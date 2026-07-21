"""
Echo — Main Application Entry Point
FastAPI app configuration, middleware injection, and router mounting.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from backend.core.config import get_settings
from backend.core.logging import setup_logging
from backend.core.middleware import RequestLoggingMiddleware
from backend.api.v1.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the FastAPI application."""
    setup_logging(log_level="DEBUG" if settings.app_debug else "INFO", json_format=not settings.app_debug)
    logger = structlog.get_logger(__name__)
    logger.info("startup", app_name=settings.app_name, env=settings.app_env)
    
    # Initialize connections, ML models, etc. if needed here
    
    yield
    
    # Cleanup logic
    logger.info("shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Industrial Knowledge Intelligence Platform API",
    lifespan=lifespan,
    docs_url="/docs" if settings.app_debug else None,
    redoc_url="/redoc" if settings.app_debug else None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Request Logging Middleware
app.add_middleware(RequestLoggingMiddleware)

# API Routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "version": settings.app_version}
