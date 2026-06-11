import uuid

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import TimestampMixin


class ProfessionalSpecialty(
    Base,
    TimestampMixin,
):
    __tablename__ = "professional_specialties"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "specialty_id",
            name="uq_professional_specialty",
        ),
    )

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

    specialty_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("specialties.id"),
        nullable=False,
        index=True,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
    )

    specialty = relationship(
        "Specialty",
        back_populates="professional_specialties",
    )