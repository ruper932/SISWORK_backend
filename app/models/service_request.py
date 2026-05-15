# app/models/service_request.py
from datetime import date, datetime, time
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    Time,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ContactChannel, ServiceRequestStatus


class ServiceRequest(Base):
    __tablename__ = "servicerequests"

    __table_args__ = (
        CheckConstraint(
            "(minimum_budget IS NULL AND maximum_budget IS NULL) OR "
            "(minimum_budget IS NOT NULL AND maximum_budget IS NOT NULL AND minimum_budget >= 0 AND maximum_budget >= minimum_budget)",
            name="ck_service_requests_budget_range",
        ),
        CheckConstraint(
            "(preferred_start_time IS NULL AND preferred_end_time IS NULL) OR "
            "(preferred_start_time IS NOT NULL AND preferred_end_time IS NOT NULL AND preferred_start_time < preferred_end_time)",
            name="ck_service_requests_preferred_time_range",
        ),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    client_user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    specialty_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("specialties.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    department: Mapped[str] = mapped_column(String(100), nullable=False, default="La Paz")
    city: Mapped[str] = mapped_column(String(100), nullable=False, default="La Paz")
    zone: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reference: Mapped[str | None] = mapped_column(Text, nullable=True)

    preferred_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    preferred_start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    preferred_end_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    minimum_budget: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    maximum_budget: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    status: Mapped[ServiceRequestStatus] = mapped_column(
        Enum(ServiceRequestStatus, name="service_request_status_enum"),
        nullable=False,
        default=ServiceRequestStatus.OPEN,
        index=True,
    )

    assigned_professional_profile_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    contact_channel: Mapped[ContactChannel] = mapped_column(
        Enum(ContactChannel, name="contact_channel_enum"),
        nullable=False,
        default=ContactChannel.WHATSAPP,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    client_user = relationship("User", foreign_keys=[client_user_id])
    specialty = relationship("Specialty")
    assigned_professional_profile = relationship("ProfessionalProfile", foreign_keys=[assigned_professional_profile_id])