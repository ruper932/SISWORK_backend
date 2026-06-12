import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.db.enums import ProfessionalRequestStatusEnum


class ProfessionalRequestCreate(BaseModel):
    bio: str | None = Field(default=None, max_length=1000)
    experience_years: int = Field(default=0, ge=0, le=80)
    motivation: str | None = Field(default=None, max_length=5000)


class ProfessionalRequestReject(BaseModel):
    rejection_reason: str = Field(min_length=5, max_length=1000)


class ProfessionalRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_ci: str
    bio: str | None = None
    experience_years: int
    motivation: str | None = None
    status: ProfessionalRequestStatusEnum
    rejection_reason: str | None = None
    reviewed_by_ci: str | None = None
    created_at: datetime
    updated_at: datetime


class ProfessionalRequestListResponse(BaseModel):
    items: list[ProfessionalRequestResponse]
    total: int
    skip: int
    limit: int