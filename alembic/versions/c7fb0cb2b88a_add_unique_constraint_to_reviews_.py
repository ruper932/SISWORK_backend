"""add unique constraint to reviews application reviewer

Revision ID: c7fb0cb2b88a
Revises: 64242a0ede24
Create Date: 2026-06-12 01:40:07.066829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7fb0cb2b88a'
down_revision: Union[str, Sequence[str], None] = '64242a0ede24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_review_application_reviewer",
        "reviews",
        ["application_id", "reviewer_ci"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_review_application_reviewer",
        "reviews",
        type_="unique",
    )