from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ServiceApplicationCreateRequest(BaseModel):
    service_request_id: UUID
    professional_profile_id: UUID
    proposal_message: str | None = None
    estimated_price: Decimal | None = None


class ServiceApplicationUpdateRequest(BaseModel):
    proposal_message: str | None = None
    estimated_price: Decimal | None = None
    status: str | None = None
    responded_at: datetime | None = None
    cancelled_at: datetime | None = None


class ServiceApplicationResponse(BaseModel):
    id: UUID
    service_request_id: UUID
    professional_profile_id: UUID
    proposal_message: str | None
    estimated_price: Decimal | None
    status: str
    applied_at: datetime
    responded_at: datetime | None
    cancelled_at: datetime | None

    model_config = ConfigDict(from_attributes=True)