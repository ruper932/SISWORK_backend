from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ServiceRating(Base):
    __tablename__ = "serviceratings"

    __table_args__ = (
        UniqueConstraint("service_request_id", name="uq_service_ratings_service_request_id"),
        CheckConstraint("score >= 1 AND score <= 5", name="ck_service_ratings_score_range"),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_request_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("servicerequests.id", ondelete="CASCADE"),
        nullable=False,
    )
    client_user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    professional_profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    service_request = relationship("ServiceRequest")
    client_user = relationship("User", foreign_keys=[client_user_id])
    professional_profile = relationship("ProfessionalProfile")