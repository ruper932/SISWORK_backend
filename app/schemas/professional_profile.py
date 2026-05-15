# app/schemas/professional_profile.py
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProfessionalProfileCreateRequest(BaseModel):
    user_id: UUID
    bio: Optional[str] = None
    years_experience: int = 0
    main_zone: str
    service_radius_km: Decimal = Decimal("5.00")
    work_reference: Optional[str] = None
    identity_document_url: Optional[str] = None
    verification_status: str = "PENDING"
    available_now: bool = False
    public_contact_enabled: bool = True


class ProfessionalProfileUpdateRequest(BaseModel):
    bio: Optional[str] = None
    years_experience: Optional[int] = None
    main_zone: Optional[str] = None
    service_radius_km: Optional[Decimal] = None
    work_reference: Optional[str] = None
    identity_document_url: Optional[str] = None
    verification_status: Optional[str] = None
    verification_requested_at: Optional[datetime] = None
    verification_resolved_at: Optional[datetime] = None
    verified_by_user_id: Optional[UUID] = None
    available_now: Optional[bool] = None
    public_contact_enabled: Optional[bool] = None


class ProfessionalProfileListItemResponse(BaseModel):
    id: UUID
    user_id: UUID
    bio: Optional[str]
    years_experience: int
    main_zone: str
    service_radius_km: Decimal
    verification_status: str
    average_rating: Decimal
    ratings_count: int
    completed_services_count: int
    available_now: bool
    public_contact_enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalProfileDetailResponse(BaseModel):
    id: UUID
    user_id: UUID
    bio: Optional[str]
    years_experience: int
    main_zone: str
    service_radius_km: Decimal
    work_reference: Optional[str]
    identity_document_url: Optional[str]
    verification_status: str
    verification_requested_at: Optional[datetime]
    verification_resolved_at: Optional[datetime]
    verified_by_user_id: Optional[UUID]
    average_rating: Decimal
    ratings_count: int
    completed_services_count: int
    available_now: bool
    public_contact_enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalProfileCreateResponse(BaseModel):
    id: UUID
    user_id: UUID
    bio: Optional[str]
    years_experience: int
    main_zone: str
    service_radius_km: Decimal
    verification_status: str
    available_now: bool
    public_contact_enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)