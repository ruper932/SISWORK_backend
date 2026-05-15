from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ApplicationStatus


class ServiceApplication(Base):
    __tablename__ = "serviceapplications"

    __table_args__ = (
        UniqueConstraint(
            "service_request_id",
            "professional_profile_id",
            name="uq_service_applications_request_professional",
        ),
        CheckConstraint(
            "estimated_price IS NULL OR estimated_price >= 0",
            name="ck_service_applications_estimated_price_nonnegative",
        ),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_request_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("servicerequests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    professional_profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    proposal_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status_enum"),
        nullable=False,
        default=ApplicationStatus.PENDING,
        index=True,
    )
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    service_request = relationship("ServiceRequest")
    professional_profile = relationship("ProfessionalProfile")