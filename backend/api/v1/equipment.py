"""
INDUS AI — Equipment API
Endpoints for equipment management.
"""

from fastapi import APIRouter, Depends
from backend.schemas.equipment import EquipmentCreateRequest, EquipmentResponse
from backend.schemas.base import ApiResponse, PaginatedResponse
from backend.db.repositories.equipment_repo import EquipmentRepository
from backend.core.dependencies import get_current_user_id

router = APIRouter()
equip_repo = EquipmentRepository()


@router.post("", response_model=ApiResponse[EquipmentResponse])
async def create_equipment(
    request: EquipmentCreateRequest,
    user_id: str = Depends(get_current_user_id)
):
    data = request.model_dump(exclude_unset=True)
    data["user_id"] = user_id
    
    equip = await equip_repo.create(data)
    return ApiResponse(data=equip)


@router.get("", response_model=PaginatedResponse[EquipmentResponse])
async def list_equipment(
    page: int = 1,
    page_size: int = 20,
    user_id: str = Depends(get_current_user_id)
):
    result = await equip_repo.list_by_user(user_id, page=page, page_size=page_size)
    return PaginatedResponse(
        data=result["data"],
        total=result["total"],
        page=page,
        page_size=page_size
    )


@router.get("/{equipment_id}", response_model=ApiResponse[EquipmentResponse])
async def get_equipment(
    equipment_id: str,
    user_id: str = Depends(get_current_user_id)
):
    equip = await equip_repo.get_by_id(equipment_id)
    if not equip or equip.get("user_id") != user_id:
        return ApiResponse(success=False, message="Equipment not found")
        
    return ApiResponse(data=equip)
