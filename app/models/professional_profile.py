# app/models/professional_profile.py
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import VerificationStatus


class ProfessionalProfile(Base):
    __tablename__ = "professionalprofiles"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    years_experience: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    main_zone: Mapped[str] = mapped_column(String(100), nullable=False)
    service_radius_km: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("5.00"))
    work_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    identity_document_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus, name="verification_status_enum"),
        nullable=False,
        default=VerificationStatus.PENDING,
        index=True,
    )

    verification_requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    verified_by_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    average_rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), nullable=False, default=Decimal("0.00"))
    ratings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed_services_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    available_now: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    public_contact_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

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

    user = relationship("User", foreign_keys=[user_id])
    verified_by_user = relationship("User", foreign_keys=[verified_by_user_id])