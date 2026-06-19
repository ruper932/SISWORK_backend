from __future__ import annotations

import uuid
from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field

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


class ProfessionalSpecialtyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    specialty: SpecialtySimpleResponse

    @computed_field
    @property
    def id(self) -> uuid.UUID:
        return self.specialty.id

    @computed_field
    @property
    def name(self) -> str:
        return self.specialty.name

    @computed_field
    @property
    def description(self) -> Optional[str]:
        return self.specialty.description


class ProfessionalPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_ci: str
    bio: Optional[str] = None
    experience_years: int
    verification_status: VerificationStatusEnum
    rating_average: float
    rating_count: int
    is_available: bool
    specialties: list[SpecialtySimpleResponse]
    availabilities: list[ProfessionalAvailabilityResponse]

    @computed_field
    @property
    def full_name(self) -> str:
        user = getattr(self, "user", None)
        if not user:
            return ""

        parts = [
            getattr(user, "first_name", None),
            getattr(user, "last_name", None),
            getattr(user, "mother_last_name", None),
        ]
        return " ".join(part for part in parts if part)

    @computed_field
    @property
    def city(self) -> Optional[str]:
        user = getattr(self, "user", None)
        return getattr(user, "city", None) if user else None

    @computed_field
    @property
    def zone(self) -> Optional[str]:
        user = getattr(self, "user", None)
        return getattr(user, "zone", None) if user else None