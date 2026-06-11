import uuid

from sqlalchemy import (
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import (
    ENUM,
    UUID,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.enums import VerificationStatusEnum
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class VerificationRequest(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "verification_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(
            VerificationStatusEnum,
            name="verification_request_status_enum",
            create_type=True,
        ),
        default=VerificationStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    reviewed_by_ci: Mapped[str | None] = mapped_column(
        ForeignKey("users.ci"),
        nullable=True,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
    )

    reviewed_by = relationship(
        "User",
    )

    documents = relationship(
        "VerificationDocument",
        back_populates="verification_request",
        cascade="all, delete-orphan",
    )