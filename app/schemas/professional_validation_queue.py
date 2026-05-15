from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfessionalValidationQueueCreateRequest(BaseModel):
    professional_profile_id: UUID
    requested_by_user_id: UUID
    assigned_support_user_id: UUID | None = None


class ProfessionalValidationQueueUpdateRequest(BaseModel):
    assigned_support_user_id: UUID | None = None
    status: str | None = None
    review_started_at: datetime | None = None
    resolved_at: datetime | None = None
    rejection_reason: str | None = None
    waiting_time_minutes: int | None = None
    review_time_minutes: int | None = None


class ProfessionalValidationQueueResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    requested_by_user_id: UUID
    assigned_support_user_id: UUID | None
    status: str
    submitted_at: datetime
    review_started_at: datetime | None
    resolved_at: datetime | None
    rejection_reason: str | None
    waiting_time_minutes: int | None
    review_time_minutes: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)