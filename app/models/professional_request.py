import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.enums import ProfessionalRequestStatusEnum
from app.db.mixins import TimestampMixin, SoftDeleteMixin


class ProfessionalRequest(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "professional_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    bio: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    motivation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[ProfessionalRequestStatusEnum] = mapped_column(
        ENUM(
            ProfessionalRequestStatusEnum,
            name="professional_request_status_enum",
            create_type=True,
        ),
        default=ProfessionalRequestStatusEnum.PENDING,
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
        index=True,
    )

    user = relationship(
        "User",
        foreign_keys=[user_ci],
    )

    reviewed_by = relationship(
        "User",
        foreign_keys=[reviewed_by_ci],
    )