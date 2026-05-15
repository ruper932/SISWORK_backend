# app/models/professional_availability.py
from datetime import datetime, time
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Time, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import Weekday


class ProfessionalAvailability(Base):
    __tablename__ = "professionalavailabilities"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "weekday",
            "start_time",
            "end_time",
            name="uq_professional_availability_profile_weekday_start_end",
        ),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    professional_profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    weekday: Mapped[Weekday] = mapped_column(
        Enum(Weekday, name="weekday_enum"),
        nullable=False,
        index=True,
    )

    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

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

    professional_profile = relationship("ProfessionalProfile")