from datetime import datetime, UTC

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import DateTime


class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )