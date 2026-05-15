# app/schemas/certification.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CertificationCreateRequest(BaseModel):
    professional_profile_id: UUID
    document_type: str = "CERTIFICATE"
    title: str
    institution: str | None = None
    issue_year: int | None = None
    file_url: str


class CertificationUpdateRequest(BaseModel):
    document_type: str | None = None
    title: str | None = None
    institution: str | None = None
    issue_year: int | None = None
    file_url: str | None = None
    is_verified: bool | None = None
    verified_by_user_id: UUID | None = None
    verified_at: datetime | None = None


class CertificationListItemResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    document_type: str
    title: str
    institution: str | None
    issue_year: int | None
    file_url: str
    is_verified: bool
    verified_by_user_id: UUID | None
    verified_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CertificationDetailResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    document_type: str
    title: str
    institution: str | None
    issue_year: int | None
    file_url: str
    is_verified: bool
    verified_by_user_id: UUID | None
    verified_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CertificationCreateResponse(BaseModel):
    id: UUID
    professional_profile_id: UUID
    document_type: str
    title: str
    institution: str | None
    issue_year: int | None
    file_url: str
    is_verified: bool
    verified_by_user_id: UUID | None
    verified_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    