"""
INDUS AI — Dashboard API
Endpoints for the dashboard stats and charts.
"""

from fastapi import APIRouter, Depends
from backend.schemas.graph import DashboardStatsResponse, DashboardChartsResponse
from backend.schemas.base import ApiResponse
from backend.services.dashboard_service import DashboardService
from backend.core.dependencies import get_current_user_id

router = APIRouter()


@router.get("/stats", response_model=ApiResponse[DashboardStatsResponse])
async def get_stats(user_id: str = Depends(get_current_user_id)):
    service = DashboardService()
    stats = await service.get_stats(user_id)
    return ApiResponse(data=stats)


@router.get("/activity", response_model=ApiResponse[dict])
async def get_activity(limit: int = 10, user_id: str = Depends(get_current_user_id)):
    service = DashboardService()
    activity = await service.get_activity(user_id, limit)
    return ApiResponse(data=activity)


@router.get("/charts", response_model=ApiResponse[DashboardChartsResponse])
async def get_charts(user_id: str = Depends(get_current_user_id)):
    service = DashboardService()
    charts = await service.get_charts(user_id)
    return ApiResponse(data=charts)
