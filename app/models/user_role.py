from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import TimestampMixin


class UserRole(
    Base,
    TimestampMixin,
):
    __tablename__ = "user_roles"

    __table_args__ = (
        UniqueConstraint(
            "user_ci",
            "role_id",
            name="uq_user_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="user_roles",
    )

    role = relationship(
        "Role",
        back_populates="user_roles",
    )