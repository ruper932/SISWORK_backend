from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field

from app.db.enums import RequestStatusEnum, UrgencyLevelEnum


class RequestCreate(BaseModel):
    specialty_id: uuid.UUID
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10)
    budget: Optional[Decimal] = None
    proposed_final_price: Optional[Decimal] = None
    scheduled_date: Optional[datetime] = None
    city: str = Field(min_length=2, max_length=100)
    zone: Optional[str] = Field(default=None, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    urgency: UrgencyLevelEnum = UrgencyLevelEnum.MEDIUM

    @field_validator("budget", "proposed_final_price")
    @classmethod
    def validate_amounts(cls, v):
        if v is not None and v < 0:
            raise ValueError("Amount must be positive")
        return v


class RequestUpdate(BaseModel):
    specialty_id: Optional[uuid.UUID] = None
    title: Optional[str] = Field(default=None, min_length=3, max_length=255)
    description: Optional[str] = Field(default=None, min_length=10)
    budget: Optional[Decimal] = None
    proposed_final_price: Optional[Decimal] = None
    scheduled_date: Optional[datetime] = None
    city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    zone: Optional[str] = Field(default=None, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    urgency: Optional[UrgencyLevelEnum] = None

    @field_validator("budget", "proposed_final_price")
    @classmethod
    def validate_amounts(cls, v):
        if v is not None and v < 0:
            raise ValueError("Amount must be positive")
        return v


class RequestCancel(BaseModel):
    cancellation_reason: Optional[str] = Field(default=None, max_length=1000)


class AssignedProfessionalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_ci: str
    bio: Optional[str] = None
    experience_years: int
    verification_status: str
    rating_average: float
    rating_count: int
    is_available: bool


class RequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    client_ci: str
    specialty_id: uuid.UUID
    assigned_professional_profile_id: Optional[uuid.UUID] = None
    assigned_professional: Optional[AssignedProfessionalResponse] = None
    title: str
    description: str
    budget: Optional[Decimal] = None
    proposed_final_price: Optional[Decimal] = None
    scheduled_date: Optional[datetime] = None
    city: str
    zone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    urgency: UrgencyLevelEnum
    status: RequestStatusEnum
    is_review_enabled: bool
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def can_review(self) -> bool:
        return (
            self.status == RequestStatusEnum.COMPLETED
            and self.is_review_enabled
            and self.assigned_professional_profile_id is not None
        )


class RequestListResponse(BaseModel):
    items: List[RequestResponse]
    total: int
    skip: int
    limit: int