"""seed_initial_admin_and_support_users

Revision ID: 8bc478457236
Revises: 69ba0404a919
Create Date: 2026-04-17 16:19:19.730573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc478457236'
down_revision: Union[str, Sequence[str], None] = '69ba0404a919'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    INSERT INTO users (
        id,
        first_name,
        last_name,
        email,
        password_hash,
        role,
        status,
        phone,
        whatsapp_number,
        is_active,
        email_verified_at,
        failed_login_attempts,
        created_at,
        updated_at
    )
    VALUES
    (
        gen_random_uuid(),
        'Admin',
        'SISWORK',
        'admin@siswork.local',
        '<ADMIN_PASSWORD_HASH>',
        'ADMIN',
        'ACTIVE',
        '70000000',
        '70000000',
        true,
        now(),
        0,
        now(),
        now()
    ),
    (
        gen_random_uuid(),
        'Soporte',
        'SISWORK',
        'soporte@siswork.local',
        '<SUPPORT_PASSWORD_HASH>',
        'SUPPORT',
        'ACTIVE',
        '71111111',
        '71111111',
        true,
        now(),
        0,
        now(),
        now()
    )
    ON CONFLICT (email) DO NOTHING
    """)


def downgrade() -> None:
    op.execute("""
    DELETE FROM users
    WHERE email IN ('admin@siswork.local', 'soporte@siswork.local')
    """)