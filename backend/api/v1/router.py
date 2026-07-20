from fastapi import APIRouter

from backend.api.v1 import auth, documents, chat, equipment, graph, dashboard, search

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
