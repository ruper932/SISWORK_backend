from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import VerificationStatus


class ProfessionalValidationQueue(Base):
    __tablename__ = "professionalvalidationqueue"

    __table_args__ = (
        UniqueConstraint("professional_profile_id", name="uq_prof_validation_queue_profile_id"),
        CheckConstraint(
            "waiting_time_minutes IS NULL OR waiting_time_minutes >= 0",
            name="ck_prof_validation_queue_waiting_time_nonnegative",
        ),
        CheckConstraint(
            "review_time_minutes IS NULL OR review_time_minutes >= 0",
            name="ck_prof_validation_queue_review_time_nonnegative",
        ),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    professional_profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    requested_by_user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    assigned_support_user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus, name="verification_status_enum"),
        nullable=False,
        default=VerificationStatus.PENDING,
        index=True,
    )
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    review_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    waiting_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    review_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    professional_profile = relationship("ProfessionalProfile")
    requested_by_user = relationship("User", foreign_keys=[requested_by_user_id])
    assigned_support_user = relationship("User", foreign_keys=[assigned_support_user_id])