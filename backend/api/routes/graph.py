"""
INDUS AI — Graph Routes
Knowledge graph data and node inspection endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.core.dependencies import CurrentUser
from backend.core.logging import get_logger
from backend.schemas.base import ApiResponse
from backend.schemas.graph import (
    GraphDataResponse,
    GraphEdgeResponse,
    GraphNodeDetailResponse,
    GraphNodeResponse,
)
from backend.services.graph_service import GraphService

logger = get_logger(__name__)
router = APIRouter(prefix="/graph", tags=["Knowledge Graph"])

graph_service = GraphService()


@router.get("/data", response_model=ApiResponse[GraphDataResponse])
async def get_graph_data(user_id: CurrentUser):
    """Get the full knowledge graph for the current user.

    Returns all document, equipment, and topic nodes with
    their relationship edges.
    """
    data = await graph_service.get_graph_data(user_id)

    nodes = [GraphNodeResponse(**n) for n in data["nodes"]]
    edges = [GraphEdgeResponse(**e) for e in data["edges"]]

    return ApiResponse(
        data=GraphDataResponse(nodes=nodes, edges=edges)
    )


@router.get("/nodes", response_model=ApiResponse[list[GraphNodeResponse]])
async def get_graph_nodes(user_id: CurrentUser):
    """Get all nodes in the knowledge graph."""
    data = await graph_service.get_graph_data(user_id)
    nodes = [GraphNodeResponse(**n) for n in data["nodes"]]
    return ApiResponse(data=nodes)


@router.get("/edges", response_model=ApiResponse[list[GraphEdgeResponse]])
async def get_graph_edges(user_id: CurrentUser):
    """Get all edges in the knowledge graph."""
    data = await graph_service.get_graph_data(user_id)
    edges = [GraphEdgeResponse(**e) for e in data["edges"]]
    return ApiResponse(data=edges)


@router.get("/node/{node_id}", response_model=ApiResponse[GraphNodeDetailResponse])
async def get_node_detail(node_id: str, user_id: CurrentUser):
    """Get detailed information about a node and its connections."""
    detail = await graph_service.get_node_detail(node_id)

    # Build the node response (we need to find the node type)
    node = GraphNodeResponse(
        id=node_id,
        type="unknown",
        label=node_id,
        metadata={},
    )

    connections = [
        GraphEdgeResponse(
            id=e.get("id", ""),
            source=e.get("source_id", ""),
            target=e.get("target_id", ""),
            type=e.get("relationship", "relates_to"),
            label=e.get("relationship", "relates_to").replace("_", " ").title(),
            weight=e.get("weight", 1.0),
        )
        for e in detail.get("connections", [])
    ]

    return ApiResponse(
        data=GraphNodeDetailResponse(
            node=node,
            connections=connections,
            connected_nodes=[],
        )
    )
