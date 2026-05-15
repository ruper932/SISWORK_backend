from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


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



class UserRoleEnum(str, Enum):
    CLIENT = "CLIENT"
    PROFESSIONAL = "PROFESSIONAL"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"


class UserStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class UserGenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    PREFERNOTTOSAY = "PREFERNOTTOSAY"


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: Optional[str] = None
    whatsappnumber: Optional[str] = None
    profilephotourl: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[UserGenderEnum] = None


class UserCreate(UserBase):
    password: str
    role: UserRoleEnum = UserRoleEnum.CLIENT


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    whatsappnumber: Optional[str] = None
    profilephotourl: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[UserGenderEnum] = None
    status: Optional[UserStatusEnum] = None
    isactive: Optional[bool] = None


class UserRead(UserBase):
    id: UUID
    role: UserRoleEnum
    status: UserStatusEnum
    emailverifiedat: Optional[datetime] = None
    lastloginat: Optional[datetime] = None
    failedloginattempts: int
    isactive: bool
    createdat: datetime
    updatedat: datetime
    deletedat: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)