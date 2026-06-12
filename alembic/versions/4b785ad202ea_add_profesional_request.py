"""add_profesional_request

Revision ID: 4b785ad202ea
Revises: c7fb0cb2b88a
Create Date: 2026-06-12 10:40:26.875475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4b785ad202ea'
down_revision: Union[str, Sequence[str], None] = 'c7fb0cb2b88a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

professional_request_status_enum = postgresql.ENUM(
    "PENDING",
    "APPROVED",
    "REJECTED",
    name="professional_request_status_enum",
)


def upgrade() -> None:
    professional_request_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "professional_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_ci", sa.String(length=20), nullable=False),
        sa.Column("bio", sa.String(length=1000), nullable=True),
        sa.Column("experience_years", sa.Integer(), nullable=False),
        sa.Column("motivation", sa.Text(), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM(
                "PENDING",
                "APPROVED",
                "REJECTED",
                name="professional_request_status_enum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("rejection_reason", sa.String(length=1000), nullable=True),
        sa.Column("reviewed_by_ci", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["reviewed_by_ci"], ["users.ci"]),
        sa.ForeignKeyConstraint(["user_ci"], ["users.ci"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_professional_requests_user_ci"),
        "professional_requests",
        ["user_ci"],
        unique=False,
    )
    op.create_index(
        op.f("ix_professional_requests_reviewed_by_ci"),
        "professional_requests",
        ["reviewed_by_ci"],
        unique=False,
    )
    op.create_index(
        op.f("ix_professional_requests_status"),
        "professional_requests",
        ["status"],
        unique=False,
    )

    op.execute(
        """
        CREATE UNIQUE INDEX uq_professional_requests_pending_per_user
        ON professional_requests (user_ci)
        WHERE status = 'PENDING' AND deleted_at IS NULL
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_professional_requests_pending_per_user")
    op.drop_index(op.f("ix_professional_requests_status"), table_name="professional_requests")
    op.drop_index(op.f("ix_professional_requests_reviewed_by_ci"), table_name="professional_requests")
    op.drop_index(op.f("ix_professional_requests_user_ci"), table_name="professional_requests")
    op.drop_table("professional_requests")
    professional_request_status_enum.drop(op.get_bind(), checkfirst=True)