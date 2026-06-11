import uuid
from datetime import time

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Time,
    UniqueConstraint,
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


class ProfessionalAvailability(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "professional_availabilities"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "day_of_week",
            name="uq_professional_day",
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

    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="availabilities",
    )