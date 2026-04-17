"""create_specialties_and_professional_specialties

Revision ID: 3e36a71779cc
Revises: a443fad4a422
Create Date: 2026-04-17 16:03:32.258983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e36a71779cc'
down_revision: Union[str, Sequence[str], None] = 'a443fad4a422'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

specialty_level_enum = sa.Enum(
    "BASIC",
    "INTERMEDIATE",
    "ADVANCED",
    "EXPERT",
    name="specialty_level_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    specialty_level_enum.create(bind, checkfirst=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS specialties (
        id UUID PRIMARY KEY,
        code VARCHAR(50) NOT NULL UNIQUE,
        name VARCHAR(100) NOT NULL UNIQUE,
        description TEXT,
        is_active BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS professional_specialties (
        id UUID PRIMARY KEY,
        professional_profile_id UUID NOT NULL,
        specialty_id UUID NOT NULL,
        level specialty_level_enum NOT NULL DEFAULT 'BASIC',
        years_experience INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_professional_specialties_profile_id
            FOREIGN KEY (professional_profile_id)
            REFERENCES professional_profiles(id)
            ON DELETE CASCADE,
        CONSTRAINT fk_professional_specialties_specialty_id
            FOREIGN KEY (specialty_id)
            REFERENCES specialties(id)
            ON DELETE RESTRICT,
        CONSTRAINT uq_professional_specialty_profile_specialty
            UNIQUE (professional_profile_id, specialty_id),
        CONSTRAINT ck_professional_specialties_years_experience_non_negative
            CHECK (years_experience >= 0)
    )
    """)

    op.create_index(
        "ix_professional_specialties_profile_id",
        "professional_specialties",
        ["professional_profile_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_professional_specialties_specialty_id",
        "professional_specialties",
        ["specialty_id"],
        unique=False,
        if_not_exists=True,
    )

    op.execute("""
    INSERT INTO specialties (id, code, name, description, is_active, created_at)
    VALUES
        (gen_random_uuid(), 'plomeria', 'Plomería', 'Servicios de plomería y gasfitería', true, now()),
        (gen_random_uuid(), 'electricidad', 'Electricidad', 'Instalaciones y reparaciones eléctricas', true, now()),
        (gen_random_uuid(), 'carpinteria', 'Carpintería', 'Trabajos en madera', true, now()),
        (gen_random_uuid(), 'albanileria', 'Albañilería', 'Obra gruesa y refacciones', true, now()),
        (gen_random_uuid(), 'mecanicaautomotriz', 'Mecánica automotriz', 'Diagnóstico y reparación automotriz', true, now()),
        (gen_random_uuid(), 'reparacionelectrodomesticos', 'Reparación de electrodomésticos', 'Servicio técnico de electrodomésticos', true, now()),
        (gen_random_uuid(), 'pintura', 'Pintura', 'Pintado de interiores y exteriores', true, now()),
        (gen_random_uuid(), 'limpieza', 'Limpieza', 'Servicios de limpieza', true, now()),
        (gen_random_uuid(), 'jardineria', 'Jardinería', 'Mantenimiento de jardines', true, now())
    ON CONFLICT (code) DO NOTHING
    """)


def downgrade() -> None:
    op.drop_index("ix_professional_specialties_specialty_id", table_name="professional_specialties", if_exists=True)
    op.drop_index("ix_professional_specialties_profile_id", table_name="professional_specialties", if_exists=True)

    op.execute("DROP TABLE IF EXISTS professional_specialties")
    op.execute("DROP TABLE IF EXISTS specialties")

    specialty_level_enum.drop(op.get_bind(), checkfirst=True)