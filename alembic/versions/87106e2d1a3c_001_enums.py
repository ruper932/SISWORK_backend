"""extend users for siswork

Revision ID: 87106e2d1a3c
Revises: 4aaeceb6ae56
Create Date: 2026-04-17 15:30:06.223231
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "87106e2d1a3c"
down_revision: Union[str, Sequence[str], None] = "4aaeceb6ae56"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


gender_enum = sa.Enum(
    "MALE",
    "FEMALE",
    "OTHER",
    "PREFER_NOT_TO_SAY",
    name="user_gender_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    gender_enum.create(bind, checkfirst=True)

    op.add_column(
        "users",
        sa.Column("phone", sa.String(length=20), nullable=True),
        if_not_exists=True,
    )
    op.add_column(
        "users",
        sa.Column("whatsapp_number", sa.String(length=20), nullable=True),
        if_not_exists=True,
    )
    op.add_column(
        "users",
        sa.Column("profile_photo_url", sa.Text(), nullable=True),
        if_not_exists=True,
    )
    op.add_column(
        "users",
        sa.Column("birth_date", sa.Date(), nullable=True),
        if_not_exists=True,
    )
    op.add_column(
        "users",
        sa.Column("gender", gender_enum, nullable=True),
        if_not_exists=True,
    )
    op.add_column(
        "users",
        sa.Column("password_reset_token", sa.String(length=255), nullable=True),
        if_not_exists=True,
    )
    op.add_column(
        "users",
        sa.Column("password_reset_expires_at", sa.DateTime(timezone=True), nullable=True),
        if_not_exists=True,
    )
    op.add_column(
        "users",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        if_not_exists=True,
    )

    op.create_index("ix_users_role", "users", ["role"], unique=False, if_not_exists=True)
    op.create_index("ix_users_status", "users", ["status"], unique=False, if_not_exists=True)
    op.create_index("ix_users_created_at", "users", ["created_at"], unique=False, if_not_exists=True)


def downgrade() -> None:
    op.drop_index("ix_users_created_at", table_name="users", if_exists=True)
    op.drop_index("ix_users_status", table_name="users", if_exists=True)
    op.drop_index("ix_users_role", table_name="users", if_exists=True)

    op.drop_column("users", "deleted_at", if_exists=True)
    op.drop_column("users", "password_reset_expires_at", if_exists=True)
    op.drop_column("users", "password_reset_token", if_exists=True)
    op.drop_column("users", "gender", if_exists=True)
    op.drop_column("users", "birth_date", if_exists=True)
    op.drop_column("users", "profile_photo_url", if_exists=True)
    op.drop_column("users", "whatsapp_number", if_exists=True)
    op.drop_column("users", "phone", if_exists=True)

    gender_enum.drop(op.get_bind(), checkfirst=True)