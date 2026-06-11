import uuid

from sqlalchemy import (
    Text,
    ForeignKey,
    Numeric,
    Integer,
    Enum,
    UniqueConstraint,
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
    ApplicationStatusEnum,
)


class Application(
    Base,
    TimestampMixin,
):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("requests.id"),
        nullable=False,
        index=True,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    proposal_message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    proposed_price: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    estimated_time_hours: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[ApplicationStatusEnum] = mapped_column(
        Enum(
            ApplicationStatusEnum,
            name="application_status_enum",
        ),
        default=ApplicationStatusEnum.PENDING,
        nullable=False,
    )

    request = relationship(
        "Request",
        back_populates="applications",
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="applications",
    )

    reviews = relationship(
        "Review",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "request_id",
            "professional_profile_id",
            name="uq_application_request_professional",
        ),
    )