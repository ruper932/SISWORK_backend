from datetime import UTC, date, datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    ci: str
    first_name: str
    last_name: str
    mother_last_name: str | None = None
    birth_date: date
    email: EmailStr
    phone: str
    password: str
    city: str | None = None
    zone: str | None = None

    @field_validator("birth_date")
    @classmethod
    def validate_age(cls, value: date):
        today = datetime.now(UTC).date()
        age = today.year - value.year - (
            ((today.month, today.day) < (value.month, value.day))
        )
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        return value


class UserLogin(BaseModel):
    ci: str
    password: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    mother_last_name: str | None = None
    birth_date: date | None = None
    email: EmailStr | None = None
    phone: str | None = None
    password: str | None = None
    city: str | None = None
    zone: str | None = None
    whatsapp_enabled: bool | None = None
    profile_photo_path: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None
    is_verified: bool | None = None

    @field_validator("birth_date")
    @classmethod
    def validate_age(cls, value: date | None):
        if value is None:
            return value
        today = datetime.now(UTC).date()
        age = today.year - value.year - (
            ((today.month, today.day) < (value.month, value.day))
        )
        if age < 18:
            raise ValueError("User must be at least 18 years old")
        return value


class UserResponse(BaseModel):
    ci: str
    first_name: str
    last_name: str
    mother_last_name: str | None = None
    birth_date: date
    email: str
    phone: str
    city: str | None = None
    zone: str | None = None
    is_active: bool
    is_verified: bool
    roles: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    skip: int
    limit: int