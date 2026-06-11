import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.enums import VerificationStatusEnum
from app.db.mixins import TimestampMixin, SoftDeleteMixin


class ProfessionalProfile(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "professional_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        unique=True,
        nullable=False,
        index=True,
    )

    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    verification_status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(
            VerificationStatusEnum,
            name="verification_status_enum",
            create_type=True,
        ),
        default=VerificationStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    rating_average: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    rating_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="professional_profile",
    )

    verification_requests = relationship(
        "VerificationRequest",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    specialties = relationship(
        "ProfessionalSpecialty",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    applications = relationship(
        "Application",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    availabilities = relationship(
        "ProfessionalAvailability",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )