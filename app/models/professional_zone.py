# app/models/professional_zone.py
from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProfessionalZone(Base):
    __tablename__ = "professionalzones"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "department",
            "city",
            "zone",
            name="uq_professional_zone_profile_department_city_zone",
        ),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    professional_profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    department: Mapped[str] = mapped_column(String(100), nullable=False, default="La Paz")
    city: Mapped[str] = mapped_column(String(100), nullable=False, default="La Paz")
    zone: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    professional_profile = relationship("ProfessionalProfile")