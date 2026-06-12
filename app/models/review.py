import uuid

from sqlalchemy import (
    String,
    Text,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.models.mixins import TimestampMixin


class Review(
    Base,
    TimestampMixin,
):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id"),
        nullable=False,
        index=True,
    )

    reviewer_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    reviewed_user_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    application = relationship(
        "Application",
        back_populates="reviews",
    )

    reviewer = relationship(
        "User",
        foreign_keys=[reviewer_ci],
    )

    reviewed_user = relationship(
        "User",
        foreign_keys=[reviewed_user_ci],
    )

    __table_args__ = (
        UniqueConstraint(
            "application_id",
            "reviewer_ci",
            name="uq_review_application_reviewer",
        ),
    )