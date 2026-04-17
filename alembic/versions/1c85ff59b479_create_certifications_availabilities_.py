"""create_certifications_availabilities_and_zones

Revision ID: 1c85ff59b479
Revises: 3e36a71779cc
Create Date: 2026-04-17 16:06:29.327100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c85ff59b479'
down_revision: Union[str, Sequence[str], None] = '3e36a71779cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


document_type_enum = sa.Enum(
    "CI",
    "CERTIFICATE",
    "LICENSE",
    "BACKGROUND_CHECK",
    "OTHER",
    name="document_type_enum",
)

weekday_enum = sa.Enum(
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY",
    name="weekday_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    document_type_enum.create(bind, checkfirst=True)
    weekday_enum.create(bind, checkfirst=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id UUID PRIMARY KEY,
        professional_profile_id UUID NOT NULL,
        document_type document_type_enum NOT NULL DEFAULT 'CERTIFICATE',
        title VARCHAR(200) NOT NULL,
        institution VARCHAR(150),
        issue_year INTEGER,
        file_url TEXT NOT NULL,
        is_verified BOOLEAN NOT NULL DEFAULT false,
        verified_by_user_id UUID,
        verified_at TIMESTAMPTZ,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_certifications_profile_id
            FOREIGN KEY (professional_profile_id)
            REFERENCES professional_profiles(id)
            ON DELETE CASCADE,
        CONSTRAINT fk_certifications_verified_by_user_id
            FOREIGN KEY (verified_by_user_id)
            REFERENCES users(id)
            ON DELETE SET NULL,
        CONSTRAINT ck_certifications_issue_year_valid
            CHECK (
                issue_year IS NULL OR
                (issue_year >= 1950 AND issue_year <= EXTRACT(YEAR FROM CURRENT_DATE) + 1)
            )
    )
    """)

    op.create_index(
        "ix_certifications_profile_id",
        "certifications",
        ["professional_profile_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_certifications_is_verified",
        "certifications",
        ["is_verified"],
        unique=False,
        if_not_exists=True,
    )

    op.execute("""
    CREATE TABLE IF NOT EXISTS professional_availabilities (
        id UUID PRIMARY KEY,
        professional_profile_id UUID NOT NULL,
        weekday weekday_enum NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        is_available BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_professional_availabilities_profile_id
            FOREIGN KEY (professional_profile_id)
            REFERENCES professional_profiles(id)
            ON DELETE CASCADE,
        CONSTRAINT uq_professional_availabilities_profile_weekday_start_end
            UNIQUE (professional_profile_id, weekday, start_time, end_time),
        CONSTRAINT ck_professional_availabilities_time_range
            CHECK (start_time < end_time)
    )
    """)

    op.create_index(
        "ix_professional_availabilities_profile_id",
        "professional_availabilities",
        ["professional_profile_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_professional_availabilities_weekday",
        "professional_availabilities",
        ["weekday"],
        unique=False,
        if_not_exists=True,
    )

    op.execute("""
    CREATE TABLE IF NOT EXISTS professional_zones (
        id UUID PRIMARY KEY,
        professional_profile_id UUID NOT NULL,
        department VARCHAR(100) NOT NULL DEFAULT 'La Paz',
        city VARCHAR(100) NOT NULL DEFAULT 'La Paz',
        zone VARCHAR(100) NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_professional_zones_profile_id
            FOREIGN KEY (professional_profile_id)
            REFERENCES professional_profiles(id)
            ON DELETE CASCADE,
        CONSTRAINT uq_professional_zones_profile_department_city_zone
            UNIQUE (professional_profile_id, department, city, zone)
    )
    """)

    op.create_index(
        "ix_professional_zones_profile_id",
        "professional_zones",
        ["professional_profile_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_professional_zones_zone",
        "professional_zones",
        ["zone"],
        unique=False,
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_index("ix_professional_zones_zone", table_name="professional_zones", if_exists=True)
    op.drop_index("ix_professional_zones_profile_id", table_name="professional_zones", if_exists=True)
    op.execute("DROP TABLE IF EXISTS professional_zones")

    op.drop_index("ix_professional_availabilities_weekday", table_name="professional_availabilities", if_exists=True)
    op.drop_index("ix_professional_availabilities_profile_id", table_name="professional_availabilities", if_exists=True)
    op.execute("DROP TABLE IF EXISTS professional_availabilities")

    op.drop_index("ix_certifications_is_verified", table_name="certifications", if_exists=True)
    op.drop_index("ix_certifications_profile_id", table_name="certifications", if_exists=True)
    op.execute("DROP TABLE IF EXISTS certifications")

    weekday_enum.drop(op.get_bind(), checkfirst=True)
    document_type_enum.drop(op.get_bind(), checkfirst=True)