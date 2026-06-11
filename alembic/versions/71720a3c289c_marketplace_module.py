"""marketplace module

Revision ID: 71720a3c289c
Revises: 08a5dd61225b
Create Date: 2026-05-22 11:47:32.413368

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '71720a3c289c'
down_revision: Union[str, Sequence[str], None] = '08a5dd61225b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


urgency_enum = postgresql.ENUM(
    'LOW',
    'MEDIUM',
    'HIGH',
    name='urgency_level_enum'
)


def upgrade() -> None:
    """Upgrade schema."""

    # Create ENUM type first
    urgency_enum.create(op.get_bind(), checkfirst=True)

    # ---------------- APPLICATIONS ----------------

    op.add_column(
        'applications',
        sa.Column('proposal_message', sa.Text(), nullable=False)
    )

    op.add_column(
        'applications',
        sa.Column('estimated_time_hours', sa.Integer(), nullable=True)
    )

    op.alter_column(
        'applications',
        'proposed_price',
        existing_type=sa.INTEGER(),
        type_=sa.Numeric(precision=10, scale=2),
        existing_nullable=True
    )

    op.drop_index(
        op.f('ix_applications_status'),
        table_name='applications'
    )

    op.drop_constraint(
        op.f('uq_request_professional_application'),
        'applications',
        type_='unique'
    )

    op.create_unique_constraint(
        'uq_application_request_professional',
        'applications',
        ['request_id', 'professional_profile_id']
    )

    op.drop_column('applications', 'message')
    op.drop_column('applications', 'deleted_at')

    # ---------------- REQUESTS ----------------

    op.add_column(
        'requests',
        sa.Column(
            'assigned_professional_profile_id',
            sa.UUID(),
            nullable=True
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'budget',
            sa.Numeric(precision=10, scale=2),
            nullable=True
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'proposed_final_price',
            sa.Numeric(precision=10, scale=2),
            nullable=True
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'scheduled_date',
            sa.DateTime(timezone=True),
            nullable=True
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'urgency',
            urgency_enum,
            nullable=False,
            server_default='LOW'
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'is_review_enabled',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true')
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'cancellation_reason',
            sa.Text(),
            nullable=True
        )
    )

    op.alter_column(
        'requests',
        'zone',
        existing_type=sa.VARCHAR(length=100),
        nullable=True
    )

    op.drop_index(
        op.f('ix_requests_city'),
        table_name='requests'
    )

    op.drop_index(
        op.f('ix_requests_zone'),
        table_name='requests'
    )

    op.create_index(
        'idx_request_location',
        'requests',
        ['city', 'zone'],
        unique=False
    )

    op.create_foreign_key(
        'fk_requests_assigned_professional_profile',
        'requests',
        'professional_profiles',
        ['assigned_professional_profile_id'],
        ['id']
    )

    op.drop_column('requests', 'budget_max')
    op.drop_column('requests', 'deleted_at')
    op.drop_column('requests', 'budget_min')

    # ---------------- REVIEWS ----------------

    op.add_column(
        'reviews',
        sa.Column(
            'reviewed_user_ci',
            sa.String(),
            nullable=False
        )
    )

    op.drop_index(
        op.f('ix_reviews_professional_profile_id'),
        table_name='reviews'
    )

    op.drop_index(
        op.f('ix_reviews_request_id'),
        table_name='reviews'
    )

    op.drop_index(
        op.f('ix_reviews_reviewer_ci'),
        table_name='reviews'
    )

    op.drop_constraint(
        op.f('fk_reviews_professional_profile_id_reviews'),
        'reviews',
        type_='foreignkey'
    )

    op.drop_constraint(
        op.f('fk_reviews_request_id_reviews'),
        'reviews',
        type_='foreignkey'
    )

    op.create_foreign_key(
        'fk_reviews_reviewed_user_ci_users',
        'reviews',
        'users',
        ['reviewed_user_ci'],
        ['ci']
    )

    op.drop_column('reviews', 'professional_profile_id')
    op.drop_column('reviews', 'deleted_at')
    op.drop_column('reviews', 'request_id')

    # Remove temporary defaults
    op.alter_column('requests', 'urgency', server_default=None)
    op.alter_column('requests', 'is_review_enabled', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""

    # ---------------- REVIEWS ----------------

    op.add_column(
        'reviews',
        sa.Column(
            'request_id',
            sa.UUID(),
            autoincrement=False,
            nullable=False
        )
    )

    op.add_column(
        'reviews',
        sa.Column(
            'deleted_at',
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True
        )
    )

    op.add_column(
        'reviews',
        sa.Column(
            'professional_profile_id',
            sa.UUID(),
            autoincrement=False,
            nullable=False
        )
    )

    op.drop_constraint(
        'fk_reviews_reviewed_user_ci_users',
        'reviews',
        type_='foreignkey'
    )

    op.create_foreign_key(
        op.f('fk_reviews_request_id_reviews'),
        'reviews',
        'requests',
        ['request_id'],
        ['id']
    )

    op.create_foreign_key(
        op.f('fk_reviews_professional_profile_id_reviews'),
        'reviews',
        'professional_profiles',
        ['professional_profile_id'],
        ['id']
    )

    op.create_index(
        op.f('ix_reviews_reviewer_ci'),
        'reviews',
        ['reviewer_ci'],
        unique=False
    )

    op.create_index(
        op.f('ix_reviews_request_id'),
        'reviews',
        ['request_id'],
        unique=False
    )

    op.create_index(
        op.f('ix_reviews_professional_profile_id'),
        'reviews',
        ['professional_profile_id'],
        unique=False
    )

    op.drop_column('reviews', 'reviewed_user_ci')

    # ---------------- REQUESTS ----------------

    op.add_column(
        'requests',
        sa.Column(
            'budget_min',
            sa.INTEGER(),
            autoincrement=False,
            nullable=True
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'deleted_at',
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True
        )
    )

    op.add_column(
        'requests',
        sa.Column(
            'budget_max',
            sa.INTEGER(),
            autoincrement=False,
            nullable=True
        )
    )

    op.drop_constraint(
        'fk_requests_assigned_professional_profile',
        'requests',
        type_='foreignkey'
    )

    op.drop_index('idx_request_location', table_name='requests')

    op.create_index(
        op.f('ix_requests_zone'),
        'requests',
        ['zone'],
        unique=False
    )

    op.create_index(
        op.f('ix_requests_city'),
        'requests',
        ['city'],
        unique=False
    )

    op.alter_column(
        'requests',
        'zone',
        existing_type=sa.VARCHAR(length=100),
        nullable=False
    )

    op.drop_column('requests', 'cancellation_reason')
    op.drop_column('requests', 'is_review_enabled')
    op.drop_column('requests', 'urgency')
    op.drop_column('requests', 'scheduled_date')
    op.drop_column('requests', 'proposed_final_price')
    op.drop_column('requests', 'budget')
    op.drop_column('requests', 'assigned_professional_profile_id')

    # Drop ENUM type
    urgency_enum.drop(op.get_bind(), checkfirst=True)

    # ---------------- APPLICATIONS ----------------

    op.add_column(
        'applications',
        sa.Column(
            'deleted_at',
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True
        )
    )

    op.add_column(
        'applications',
        sa.Column(
            'message',
            sa.TEXT(),
            autoincrement=False,
            nullable=True
        )
    )

    op.drop_constraint(
        'uq_application_request_professional',
        'applications',
        type_='unique'
    )

    op.create_unique_constraint(
        op.f('uq_request_professional_application'),
        'applications',
        ['request_id', 'professional_profile_id'],
        postgresql_nulls_not_distinct=False
    )

    op.create_index(
        op.f('ix_applications_status'),
        'applications',
        ['status'],
        unique=False
    )

    op.alter_column(
        'applications',
        'proposed_price',
        existing_type=sa.Numeric(precision=10, scale=2),
        type_=sa.INTEGER(),
        existing_nullable=True
    )

    op.drop_column('applications', 'estimated_time_hours')
    op.drop_column('applications', 'proposal_message')