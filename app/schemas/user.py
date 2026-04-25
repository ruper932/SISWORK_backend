from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserMeResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: str
    email_verified_at: datetime | None
    last_login_at: datetime | None


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    whatsapp_number: str | None = None
    profile_photo_url: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    role: str = "CLIENT"
    status: str = "ACTIVE"
    is_active: bool = True


class UserCreateRequest(UserBase):
    password: str


class UserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    whatsapp_number: str | None = None
    profile_photo_url: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    role: str | None = None
    status: str | None = None
    is_active: bool | None = None


class UserListItemResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    role: str
    status: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    whatsapp_number: str | None
    profile_photo_url: str | None
    birth_date: date | None
    gender: str | None
    role: str
    status: str
    is_active: bool
    email_verified_at: datetime | None
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreateResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True