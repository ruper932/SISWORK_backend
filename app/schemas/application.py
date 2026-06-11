from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.db.enums import ApplicationStatusEnum


class ApplicationCreate(BaseModel):
    request_id: uuid.UUID
    proposal_message: str = Field(min_length=10)
    proposed_price: Optional[Decimal] = None
    estimated_time_hours: Optional[int] = Field(default=None, ge=1)

    @field_validator("proposed_price")
    @classmethod
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Proposed price must be positive")
        return v


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    request_id: uuid.UUID
    professional_profile_id: uuid.UUID
    proposal_message: str
    proposed_price: Optional[Decimal] = None
    estimated_time_hours: Optional[int] = None
    status: ApplicationStatusEnum
    created_at: datetime
    updated_at: datetime


class ApplicationListResponse(BaseModel):
    items: List[ApplicationResponse]
    total: int