from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ServiceRatingCreateRequest(BaseModel):
    service_request_id: UUID
    client_user_id: UUID
    professional_profile_id: UUID
    score: int
    comment: str | None = None
    is_verified: bool = True


class ServiceRatingUpdateRequest(BaseModel):
    score: int | None = None
    comment: str | None = None
    is_verified: bool | None = None


class ServiceRatingResponse(BaseModel):
    id: UUID
    service_request_id: UUID
    client_user_id: UUID
    professional_profile_id: UUID
    score: int
    comment: str | None
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)