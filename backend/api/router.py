"""
INDUS AI — API Router
Aggregates all route modules into a single versioned router.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.routes.auth import router as auth_router
from backend.api.routes.chat import router as chat_router
from backend.api.routes.documents import router as documents_router
from backend.api.routes.equipment import router as equipment_router
from backend.api.routes.graph import router as graph_router
from backend.api.routes.stats import router as stats_router
from backend.api.routes.upload import router as upload_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(documents_router)
api_router.include_router(upload_router)
api_router.include_router(chat_router)
api_router.include_router(equipment_router)
api_router.include_router(graph_router)
api_router.include_router(stats_router)
