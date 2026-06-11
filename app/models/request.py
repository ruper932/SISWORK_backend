import uuid

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Numeric,
    DateTime,
    Enum,
    Boolean,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.models.mixins import TimestampMixin
from app.db.enums import (
    RequestStatusEnum,
    UrgencyLevelEnum,
)


class Request(
    Base,
    TimestampMixin,
):
    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    client_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    specialty_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("specialties.id"),
        nullable=False,
        index=True,
    )

    assigned_professional_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professional_profiles.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    budget: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    proposed_final_price: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    scheduled_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    zone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    urgency: Mapped[UrgencyLevelEnum] = mapped_column(
        Enum(
            UrgencyLevelEnum,
            name="urgency_level_enum",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        default=UrgencyLevelEnum.MEDIUM,
        nullable=False,
    )

    status: Mapped[RequestStatusEnum] = mapped_column(
        Enum(
            RequestStatusEnum,
            name="request_status_enum",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        default=RequestStatusEnum.OPEN,
        nullable=False,
        index=True,
    )

    is_review_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    cancellation_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    client = relationship(
        "User",
        foreign_keys=[client_ci],
    )

    specialty = relationship(
        "Specialty",
    )

    assigned_professional = relationship(
        "ProfessionalProfile",
        foreign_keys=[assigned_professional_profile_id],
    )

    applications = relationship(
        "Application",
        back_populates="request",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "idx_request_location",
            "city",
            "zone",
        ),
    )