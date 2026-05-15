# app/schemas/service_request.py
from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ServiceRequestCreateRequest(BaseModel):
    client_user_id: UUID
    specialty_id: UUID
    title: str
    description: str
    department: str = "La Paz"
    city: str = "La Paz"
    zone: str
    address: str | None = None
    reference: str | None = None
    preferred_date: date | None = None
    preferred_start_time: time | None = None
    preferred_end_time: time | None = None
    minimum_budget: Decimal | None = None
    maximum_budget: Decimal | None = None
    contact_channel: str = "WHATSAPP"
    assigned_professional_profile_id: UUID | None = None
    is_active: bool = True


class ServiceRequestUpdateRequest(BaseModel):
    specialty_id: UUID | None = None
    title: str | None = None
    description: str | None = None
    department: str | None = None
    city: str | None = None
    zone: str | None = None
    address: str | None = None
    reference: str | None = None
    preferred_date: date | None = None
    preferred_start_time: time | None = None
    preferred_end_time: time | None = None
    minimum_budget: Decimal | None = None
    maximum_budget: Decimal | None = None
    status: str | None = None
    assigned_professional_profile_id: UUID | None = None
    contact_channel: str | None = None
    is_active: bool | None = None
    closed_at: datetime | None = None


class ServiceRequestListItemResponse(BaseModel):
    id: UUID
    client_user_id: UUID
    specialty_id: UUID
    title: str
    description: str
    department: str
    city: str
    zone: str
    address: str | None
    reference: str | None
    preferred_date: date | None
    preferred_start_time: time | None
    preferred_end_time: time | None
    minimum_budget: Decimal | None
    maximum_budget: Decimal | None
    status: str
    assigned_professional_profile_id: UUID | None
    contact_channel: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class ServiceRequestDetailResponse(ServiceRequestListItemResponse):
    pass


class ServiceRequestCreateResponse(ServiceRequestListItemResponse):
    pass