from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ServiceContactCreateRequest(BaseModel):
    service_request_id: UUID | None = None
    client_user_id: UUID
    professional_profile_id: UUID
    channel: str = "WHATSAPP"
    note: str | None = None


class ServiceContactUpdateRequest(BaseModel):
    channel: str | None = None
    note: str | None = None


class ServiceContactResponse(BaseModel):
    id: UUID
    service_request_id: UUID | None
    client_user_id: UUID
    professional_profile_id: UUID
    channel: str
    contacted_at: datetime
    note: str | None

    model_config = ConfigDict(from_attributes=True)