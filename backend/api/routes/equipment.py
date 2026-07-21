"""
Echo — Equipment Routes
CRUD and maintenance history endpoints for industrial equipment.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query

from backend.core.dependencies import CurrentUser
from backend.core.exceptions import NotFoundError
from backend.core.logging import get_logger
from backend.db.repositories.equipment_repo import EquipmentRepository, MaintenanceRepository
from backend.schemas.base import ApiResponse, PaginatedResponse
from backend.schemas.equipment import (
    EquipmentCreateRequest,
    EquipmentResponse,
    EquipmentUpdateRequest,
    MaintenanceCreateRequest,
    MaintenanceEventResponse,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/equipment", tags=["Equipment"])

equip_repo = EquipmentRepository()
maint_repo = MaintenanceRepository()


@router.get("", response_model=PaginatedResponse[EquipmentResponse])
async def list_equipment(
    user_id: CurrentUser,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    type: Optional[str] = Query(default=None, alias="equipment_type"),
    status: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
):
    """List equipment with pagination and filters."""
    result = await equip_repo.list_by_user(
        user_id=user_id,
        page=page,
        page_size=page_size,
        equipment_type=type,
        status=status,
        search=search,
    )

    equipment = [EquipmentResponse(**e) for e in result["data"]]
    total_pages = (result["total"] + page_size - 1) // page_size

    return PaginatedResponse(
        data=equipment,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=total_pages,
    )


@router.get("/{equipment_id}", response_model=ApiResponse[EquipmentResponse])
async def get_equipment(equipment_id: str, user_id: CurrentUser):
    """Get equipment details by ID."""
    equip = await equip_repo.get_by_id(equipment_id)
    if not equip:
        raise NotFoundError("Equipment", equipment_id)
    return ApiResponse(data=EquipmentResponse(**equip))


@router.post("", response_model=ApiResponse[EquipmentResponse])
async def create_equipment(request: EquipmentCreateRequest, user_id: CurrentUser):
    """Add new equipment."""
    data = request.model_dump()
    data["user_id"] = user_id
    data["type"] = data["type"].value if hasattr(data["type"], "value") else data["type"]
    data["status"] = data["status"].value if hasattr(data["status"], "value") else data["status"]

    equip = await equip_repo.create(data)
    return ApiResponse(
        data=EquipmentResponse(**equip),
        message="Equipment added successfully",
    )


@router.patch("/{equipment_id}", response_model=ApiResponse[EquipmentResponse])
async def update_equipment(
    equipment_id: str,
    request: EquipmentUpdateRequest,
    user_id: CurrentUser,
):
    """Update equipment details."""
    update_data = request.model_dump(exclude_none=True)

    # Convert enums to values
    for key in ("type", "status"):
        if key in update_data and hasattr(update_data[key], "value"):
            update_data[key] = update_data[key].value

    equip = await equip_repo.update(equipment_id, update_data)
    return ApiResponse(
        data=EquipmentResponse(**equip),
        message="Equipment updated",
    )


@router.get("/{equipment_id}/maintenance", response_model=ApiResponse[list[MaintenanceEventResponse]])
async def get_maintenance_history(equipment_id: str, user_id: CurrentUser):
    """Get maintenance event history for a piece of equipment."""
    events = await maint_repo.get_by_equipment(equipment_id)

    return ApiResponse(
        data=[MaintenanceEventResponse(**e) for e in events]
    )


@router.post("/{equipment_id}/maintenance", response_model=ApiResponse[MaintenanceEventResponse])
async def add_maintenance_event(
    equipment_id: str,
    request: MaintenanceCreateRequest,
    user_id: CurrentUser,
):
    """Add a maintenance event to equipment."""
    data = request.model_dump()
    data["equipment_id"] = equipment_id

    event = await maint_repo.create(data)
    return ApiResponse(
        data=MaintenanceEventResponse(**event),
        message="Maintenance event recorded",
    )
