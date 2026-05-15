# app/schemas/professional_zone.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfessionalZoneCreateRequest(BaseModel):
    professional_profile_id: UUID
    department: str = "La Paz"
    city: str = "La Paz"
    zone: str


class ProfessionalZoneUpdateRequest(BaseModel):
    department: str | None = None
    city: str | None = None
    zone: str | None = None


class ProfessionalZoneListItemResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    department: str
    city: str
    zone: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalZoneDetailResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    department: str
    city: str
    zone: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalZoneCreateResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    department: str
    city: str
    zone: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)