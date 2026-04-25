from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import UserGender, UserRole, UserStatus


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"),
        nullable=False,
        default=UserRole.CLIENT,
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status_enum"),
        nullable=False,
        default=UserStatus.ACTIVE,
    )

    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    whatsapp_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    profile_photo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    gender: Mapped[UserGender | None] = mapped_column(
        Enum(UserGender, name="user_gender_enum"),
        nullable=True,
    )

    password_reset_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    password_reset_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    failed_login_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    two_factor: Mapped["UserTwoFactor"] = relationship(
        "UserTwoFactor",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )