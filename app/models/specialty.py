import uuid

from sqlalchemy import (
    Boolean,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class Specialty(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "specialties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    professional_specialties = relationship(
        "ProfessionalSpecialty",
        back_populates="specialty",
        cascade="all, delete-orphan",
    )