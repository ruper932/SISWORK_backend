# app/models/professional_specialty.py
from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import SpecialtyLevel


class ProfessionalSpecialty(Base):
    __tablename__ = "professionalspecialties"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "specialty_id",
            name="uq_professional_specialty_profile_specialty",
        ),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    professional_profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    specialty_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("specialties.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    level: Mapped[SpecialtyLevel] = mapped_column(
        Enum(SpecialtyLevel, name="specialty_level_enum"),
        nullable=False,
        default=SpecialtyLevel.BASIC,
    )

    years_experience: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    professional_profile = relationship("ProfessionalProfile")
    specialty = relationship("Specialty")