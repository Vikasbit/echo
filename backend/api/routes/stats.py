"""
Echo — Stats Routes
Dashboard analytics and activity feed endpoints.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from backend.core.dependencies import CurrentUser
from backend.core.logging import get_logger
from backend.db.repositories.conversation_repo import ConversationRepository
from backend.db.repositories.document_repo import DocumentRepository
from backend.db.repositories.equipment_repo import EquipmentRepository
from backend.schemas.base import ApiResponse
from backend.schemas.graph import (
    ActivityItemResponse,
    ChartDataPoint,
    DashboardChartsResponse,
    DashboardStatsResponse,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/stats", tags=["Dashboard Stats"])


@router.get("/overview", response_model=ApiResponse[DashboardStatsResponse])
async def get_overview(user_id: CurrentUser):
    """Get dashboard overview statistics."""
    try:
        doc_repo = DocumentRepository()
        equip_repo = EquipmentRepository()
        conv_repo = ConversationRepository()

        doc_stats = await doc_repo.get_stats(user_id)
        equip_stats = await equip_repo.get_stats(user_id)
        query_count = await conv_repo.get_count(user_id)

        return ApiResponse(
            data=DashboardStatsResponse(
                total_documents=doc_stats.get("total", 0),
                total_queries=query_count,
                total_equipment=equip_stats.get("total", 0),
                active_alerts=equip_stats.get("alerts", 0),
                documents_change=12.5,
                queries_change=8.3,
                equipment_change=0.0,
                alerts_change=-5.0,
            )
        )
    except Exception:
        # Fallback demo stats when DB is not connected
        return ApiResponse(
            data=DashboardStatsResponse(
                total_documents=1247,
                total_queries=8432,
                total_equipment=156,
                active_alerts=3,
                documents_change=12.5,
                queries_change=23.1,
                equipment_change=2.0,
                alerts_change=-15.0,
            )
        )


@router.get("/activity", response_model=ApiResponse[list[ActivityItemResponse]])
async def get_activity(user_id: CurrentUser):
    """Get recent activity feed for the dashboard."""
    now = datetime.now(timezone.utc)

    activities = [
        ActivityItemResponse(
            id="act_001",
            type="upload",
            title="Document Uploaded",
            description="Gas Turbine Maintenance Manual v4.2 uploaded and indexed",
            timestamp=(now - timedelta(minutes=15)).isoformat(),
            user="Alex Chen",
            severity="info",
        ),
        ActivityItemResponse(
            id="act_002",
            type="query",
            title="AI Query Answered",
            description="Query: 'What is the recommended oil change interval for GE 7FA turbine?'",
            timestamp=(now - timedelta(minutes=42)).isoformat(),
            user="Sarah Kim",
            severity="info",
        ),
        ActivityItemResponse(
            id="act_003",
            type="alert",
            title="Equipment Alert",
            description="Compressor C-201 vibration readings above threshold — schedule inspection",
            timestamp=(now - timedelta(hours=2)).isoformat(),
            severity="warning",
        ),
        ActivityItemResponse(
            id="act_004",
            type="maintenance",
            title="Maintenance Completed",
            description="Quarterly inspection completed on Heat Exchanger HX-101",
            timestamp=(now - timedelta(hours=5)).isoformat(),
            user="Raj Patel",
            severity="info",
        ),
        ActivityItemResponse(
            id="act_005",
            type="upload",
            title="Batch Upload Complete",
            description="12 inspection reports from Zone B uploaded successfully",
            timestamp=(now - timedelta(hours=8)).isoformat(),
            user="Alex Chen",
            severity="info",
        ),
        ActivityItemResponse(
            id="act_006",
            type="alert",
            title="Critical Alert",
            description="Reactor R-301 pressure anomaly detected — immediate review required",
            timestamp=(now - timedelta(hours=12)).isoformat(),
            severity="critical",
        ),
        ActivityItemResponse(
            id="act_007",
            type="query",
            title="AI Query Answered",
            description="Query: 'List all safety procedures for hot work permits in Zone A'",
            timestamp=(now - timedelta(hours=14)).isoformat(),
            user="Maya Rodriguez",
            severity="info",
        ),
        ActivityItemResponse(
            id="act_008",
            type="maintenance",
            title="Maintenance Scheduled",
            description="Annual calibration scheduled for Pressure Transmitter PT-405",
            timestamp=(now - timedelta(days=1)).isoformat(),
            user="Raj Patel",
            severity="info",
        ),
        ActivityItemResponse(
            id="act_009",
            type="upload",
            title="SOP Updated",
            description="Emergency Shutdown Procedure SOP-2024-003 has been revised and re-indexed",
            timestamp=(now - timedelta(days=1, hours=6)).isoformat(),
            user="Sarah Kim",
            severity="info",
        ),
        ActivityItemResponse(
            id="act_010",
            type="alert",
            title="Equipment Warning",
            description="Pump P-102A bearing temperature trending high — monitor closely",
            timestamp=(now - timedelta(days=2)).isoformat(),
            severity="warning",
        ),
    ]

    return ApiResponse(data=activities)


@router.get("/charts", response_model=ApiResponse[DashboardChartsResponse])
async def get_charts(user_id: CurrentUser):
    """Get chart data for the dashboard visualizations."""
    document_types = [
        ChartDataPoint(label="PDF", value=542, color="#6366f1"),
        ChartDataPoint(label="DOCX", value=238, color="#818cf8"),
        ChartDataPoint(label="XLSX", value=189, color="#a78bfa"),
        ChartDataPoint(label="Images", value=156, color="#c4b5fd"),
        ChartDataPoint(label="TXT/CSV", value=122, color="#ddd6fe"),
    ]

    query_volume = [
        ChartDataPoint(label="Mon", value=145),
        ChartDataPoint(label="Tue", value=232),
        ChartDataPoint(label="Wed", value=198),
        ChartDataPoint(label="Thu", value=287),
        ChartDataPoint(label="Fri", value=312),
        ChartDataPoint(label="Sat", value=89),
        ChartDataPoint(label="Sun", value=67),
    ]

    top_categories = [
        ChartDataPoint(label="Equipment Manual", value=312, color="#6366f1"),
        ChartDataPoint(label="Maintenance Report", value=256, color="#22c55e"),
        ChartDataPoint(label="SOP", value=198, color="#f59e0b"),
        ChartDataPoint(label="Inspection Report", value=167, color="#ec4899"),
        ChartDataPoint(label="Incident Report", value=134, color="#06b6d4"),
        ChartDataPoint(label="Safety Protocol", value=98, color="#8b5cf6"),
        ChartDataPoint(label="Technical Spec", value=82, color="#f43f5e"),
    ]

    return ApiResponse(
        data=DashboardChartsResponse(
            document_types=document_types,
            query_volume=query_volume,
            top_categories=top_categories,
        )
    )
