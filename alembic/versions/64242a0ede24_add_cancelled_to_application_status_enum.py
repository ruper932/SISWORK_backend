"""add cancelled to application status enum

Revision ID: 64242a0ede24
Revises: 71720a3c289c
Create Date: 2026-06-11 23:48:22.734197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64242a0ede24'
down_revision: Union[str, Sequence[str], None] = '71720a3c289c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            "ALTER TYPE application_status_enum ADD VALUE IF NOT EXISTS 'CANCELLED'"
        )

def downgrade() -> None:
    """Downgrade schema."""
    pass
