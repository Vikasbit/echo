"""
Echo — Equipment Schemas
Request and response models for equipment endpoints.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class EquipmentType(str, Enum):
    TURBINE = "turbine"
    COMPRESSOR = "compressor"
    PUMP = "pump"
    VALVE = "valve"
    HEAT_EXCHANGER = "heat_exchanger"
    REACTOR = "reactor"
    BOILER = "boiler"
    TRANSFORMER = "transformer"
    MOTOR = "motor"
    GENERATOR = "generator"


class EquipmentStatus(str, Enum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class EquipmentResponse(BaseModel):
    id: str
    name: str
    type: str
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    status: str = "operational"
    health_score: int = 100
    specifications: Dict[str, str] = Field(default_factory=dict)
    installed_date: Optional[str] = None
    last_inspection: Optional[str] = None
    next_inspection: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class EquipmentCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    type: EquipmentType
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    status: EquipmentStatus = EquipmentStatus.OPERATIONAL
    health_score: int = Field(default=100, ge=0, le=100)
    specifications: Dict[str, str] = Field(default_factory=dict)
    installed_date: Optional[str] = None
    last_inspection: Optional[str] = None
    next_inspection: Optional[str] = None


class EquipmentUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    type: Optional[EquipmentType] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    health_score: Optional[int] = Field(default=None, ge=0, le=100)
    specifications: Optional[Dict[str, str]] = None
    last_inspection: Optional[str] = None
    next_inspection: Optional[str] = None


class MaintenanceEventResponse(BaseModel):
    id: str
    equipment_id: str
    event_type: str
    description: str
    technician: Optional[str] = None
    status: str = "scheduled"
    event_date: Optional[str] = None
    created_at: Optional[str] = None


class MaintenanceCreateRequest(BaseModel):
    event_type: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=1000)
    technician: Optional[str] = None
    status: str = "scheduled"
    event_date: str
