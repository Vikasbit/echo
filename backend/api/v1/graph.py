"""
Echo — Graph API
Endpoints for the knowledge graph.
"""

from fastapi import APIRouter, Depends
from backend.schemas.graph import GraphDataResponse
from backend.schemas.base import ApiResponse
from backend.services.graph_service import GraphService
from backend.core.dependencies import get_current_user_id

router = APIRouter()


@router.get("", response_model=ApiResponse[GraphDataResponse])
async def get_graph(user_id: str = Depends(get_current_user_id)):
    service = GraphService()
    graph_data = await service.get_full_graph(user_id)
    return ApiResponse(data=graph_data)
