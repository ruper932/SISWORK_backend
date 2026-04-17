"""create_user_addresses_and_professional_profiles

Revision ID: a443fad4a422
Revises: 87106e2d1a3c
Create Date: 2026-04-17 15:39:25.362591
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a443fad4a422"
down_revision: Union[str, Sequence[str], None] = "87106e2d1a3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


verification_status_enum = sa.Enum(
    "PENDING",
    "IN_REVIEW",
    "APPROVED",
    "REJECTED",
    name="verification_status_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    verification_status_enum.create(bind, checkfirst=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS user_addresses (
        id UUID PRIMARY KEY,
        user_id UUID NOT NULL,
        department VARCHAR(100) NOT NULL DEFAULT 'La Paz',
        city VARCHAR(100) NOT NULL DEFAULT 'La Paz',
        zone VARCHAR(100) NOT NULL,
        address VARCHAR(255),
        reference TEXT,
        latitude NUMERIC(10, 7),
        longitude NUMERIC(10, 7),
        is_primary BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_user_addresses_user_id_users
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    op.create_index(
        "ix_user_addresses_user_id",
        "user_addresses",
        ["user_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_user_addresses_zone",
        "user_addresses",
        ["zone"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "uq_user_addresses_primary_per_user",
        "user_addresses",
        ["user_id"],
        unique=True,
        if_not_exists=True,
        postgresql_where=sa.text("is_primary = true"),
    )

    op.execute("""
    CREATE TABLE IF NOT EXISTS professional_profiles (
        id UUID PRIMARY KEY,
        user_id UUID NOT NULL,
        bio TEXT,
        years_experience INTEGER NOT NULL DEFAULT 0,
        main_zone VARCHAR(100) NOT NULL,
        service_radius_km NUMERIC(5, 2) NOT NULL DEFAULT 5.00,
        work_reference TEXT,
        identity_document_url TEXT,
        verification_status verification_status_enum NOT NULL DEFAULT 'PENDING',
        verification_requested_at TIMESTAMPTZ,
        verification_resolved_at TIMESTAMPTZ,
        verified_by_user_id UUID,
        average_rating NUMERIC(3, 2) NOT NULL DEFAULT 0.00,
        ratings_count INTEGER NOT NULL DEFAULT 0,
        completed_services_count INTEGER NOT NULL DEFAULT 0,
        available_now BOOLEAN NOT NULL DEFAULT false,
        public_contact_enabled BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_professional_profiles_user_id_users
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT fk_professional_profiles_verified_by_user_id_users
            FOREIGN KEY (verified_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
        CONSTRAINT uq_professional_profiles_user_id UNIQUE (user_id),
        CONSTRAINT ck_professional_profiles_years_experience_non_negative
            CHECK (years_experience >= 0),
        CONSTRAINT ck_professional_profiles_average_rating_range
            CHECK (average_rating >= 0 AND average_rating <= 5)
    )
    """)

    op.create_index(
        "ix_professional_profiles_user_id",
        "professional_profiles",
        ["user_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_professional_profiles_verification_status",
        "professional_profiles",
        ["verification_status"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_professional_profiles_main_zone",
        "professional_profiles",
        ["main_zone"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_professional_profiles_available_now",
        "professional_profiles",
        ["available_now"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_professional_profiles_average_rating",
        "professional_profiles",
        ["average_rating"],
        unique=False,
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_index("ix_professional_profiles_average_rating", table_name="professional_profiles", if_exists=True)
    op.drop_index("ix_professional_profiles_available_now", table_name="professional_profiles", if_exists=True)
    op.drop_index("ix_professional_profiles_main_zone", table_name="professional_profiles", if_exists=True)
    op.drop_index("ix_professional_profiles_verification_status", table_name="professional_profiles", if_exists=True)
    op.drop_index("ix_professional_profiles_user_id", table_name="professional_profiles", if_exists=True)
    op.execute("DROP TABLE IF EXISTS professional_profiles")

    op.drop_index("uq_user_addresses_primary_per_user", table_name="user_addresses", if_exists=True)
    op.drop_index("ix_user_addresses_zone", table_name="user_addresses", if_exists=True)
    op.drop_index("ix_user_addresses_user_id", table_name="user_addresses", if_exists=True)
    op.execute("DROP TABLE IF EXISTS user_addresses")

    verification_status_enum.drop(op.get_bind(), checkfirst=True)