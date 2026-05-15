# app/schemas/professional_availability.py
from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfessionalAvailabilityCreateRequest(BaseModel):
    professional_profile_id: UUID
    weekday: str
    start_time: time
    end_time: time
    is_available: bool = True


class ProfessionalAvailabilityUpdateRequest(BaseModel):
    weekday: str | None = None
    start_time: time | None = None
    end_time: time | None = None
    is_available: bool | None = None


class ProfessionalAvailabilityListItemResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    weekday: str
    start_time: time
    end_time: time
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalAvailabilityDetailResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    weekday: str
    start_time: time
    end_time: time
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalAvailabilityCreateResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    weekday: str
    start_time: time
    end_time: time
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)