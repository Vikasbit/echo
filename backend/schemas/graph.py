"""
INDUS AI — Graph & Stats Schemas
Request and response models for knowledge graph and dashboard stats.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ── Knowledge Graph ───────────────────────────────────────────────

class GraphNodeResponse(BaseModel):
    id: str
    type: str  # document | equipment | topic | person
    label: str
    metadata: Dict[str, str] = Field(default_factory=dict)


class GraphEdgeResponse(BaseModel):
    id: str
    source: str
    target: str
    type: str  # references | relates_to | maintained_by | authored_by
    label: str
    weight: float = 1.0


class GraphDataResponse(BaseModel):
    nodes: List[GraphNodeResponse] = Field(default_factory=list)
    edges: List[GraphEdgeResponse] = Field(default_factory=list)


class GraphNodeDetailResponse(BaseModel):
    node: GraphNodeResponse
    connections: List[GraphEdgeResponse] = Field(default_factory=list)
    connected_nodes: List[GraphNodeResponse] = Field(default_factory=list)


# ── Dashboard Stats ───────────────────────────────────────────────

class DashboardStatsResponse(BaseModel):
    total_documents: int = 0
    total_queries: int = 0
    total_equipment: int = 0
    active_alerts: int = 0
    documents_change: float = 0.0
    queries_change: float = 0.0
    equipment_change: float = 0.0
    alerts_change: float = 0.0


class ActivityItemResponse(BaseModel):
    id: str
    type: str  # upload | query | alert | maintenance
    title: str
    description: str
    timestamp: str
    user: Optional[str] = None
    severity: Optional[str] = None  # info | warning | critical


class ChartDataPoint(BaseModel):
    label: str
    value: float
    color: Optional[str] = None


class DashboardChartsResponse(BaseModel):
    document_types: List[ChartDataPoint] = Field(default_factory=list)
    query_volume: List[ChartDataPoint] = Field(default_factory=list)
    top_categories: List[ChartDataPoint] = Field(default_factory=list)
