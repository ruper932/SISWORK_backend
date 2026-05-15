from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserAddressCreateRequest(BaseModel):
    user_id: UUID
    department: str = "La Paz"
    city: str = "La Paz"
    zone: str
    address: str | None = None
    reference: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    is_primary: bool = True


class UserAddressUpdateRequest(BaseModel):
    department: str | None = None
    city: str | None = None
    zone: str | None = None
    address: str | None = None
    reference: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    is_primary: bool | None = None


class UserAddressResponse(BaseModel):
    id: UUID
    user_id: UUID
    department: str
    city: str
    zone: str
    address: str | None
    reference: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    is_primary: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)