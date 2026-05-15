# app/schemas/professional_specialty.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfessionalSpecialtyCreateRequest(BaseModel):
    professional_profile_id: UUID
    specialty_id: UUID
    level: str = "BASIC"
    years_experience: int = 0


class ProfessionalSpecialtyUpdateRequest(BaseModel):
    level: str | None = None
    years_experience: int | None = None


class ProfessionalSpecialtyListItemResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    specialty_id: UUID
    level: str
    years_experience: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalSpecialtyDetailResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    specialty_id: UUID
    level: str
    years_experience: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalSpecialtyCreateResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    specialty_id: UUID
    level: str
    years_experience: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)