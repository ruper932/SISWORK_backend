from __future__ import annotations

import uuid
from datetime import time
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.db.enums import VerificationStatusEnum


class VerificationRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: VerificationStatusEnum
    rejection_reason: Optional[str] = None


class ProfessionalAvailabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool


class SpecialtySimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: Optional[str] = None


class ProfessionalPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_ci: str
    full_name: str
    bio: Optional[str] = None
    experience_years: int
    verification_status: VerificationStatusEnum
    rating_average: float
    rating_count: int
    is_available: bool
    city: Optional[str] = None
    zone: Optional[str] = None
    specialties: List[SpecialtySimpleResponse]
    availabilities: List[ProfessionalAvailabilityResponse]