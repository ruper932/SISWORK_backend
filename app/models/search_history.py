from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SearchHistory(Base):
    __tablename__ = "searchhistory"

    __table_args__ = (
        CheckConstraint(
            "minimum_rating IS NULL OR (minimum_rating >= 0 AND minimum_rating <= 5)",
            name="ck_search_history_minimum_rating_range",
        ),
    )

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    search_term: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specialty_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("specialties.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    zone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    minimum_rating: Mapped[Decimal | None] = mapped_column(Numeric(2, 1), nullable=True)
    available_now: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    results_count: Mapped[int] = mapped_column(nullable=False, default=0)
    searched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)

    user = relationship("User")
    specialty = relationship("Specialty")