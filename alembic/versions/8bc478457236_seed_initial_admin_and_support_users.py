"""seed_initial_admin_and_support_users
Revision ID: 8bc478457236
Revises: 69ba0404a919
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '8bc478457236'
down_revision: Union[str, Sequence[str], None] = '69ba0404a919'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Usamos IDs fijos para garantizar la integridad referencial en otras tablas
    op.execute("""
    INSERT INTO users (
        id, first_name, last_name, email, password_hash, role, status, 
        phone, whatsapp_number, is_active, email_verified_at, 
        failed_login_attempts, created_at, updated_at
    )
    VALUES
    (
        '11111111-1111-4111-8111-111111111111', 
        'Admin', 'SISWORK', 'admin@siswork.local', crypt('Admin123*', gen_salt('bf')), 
        'ADMIN', 'ACTIVE', '70000000', '70000000', true, now(), 0, now(), now()
    ),
    (
        '22222222-2222-4222-8222-222222222222', 
        'Soporte', 'SISWORK', 'soporte@siswork.local', crypt('Soporte123*', gen_salt('bf')), 
        'SUPPORT', 'ACTIVE', '71111111', '71111111', true, now(), 0, now(), now()
    )
    ON CONFLICT (email) DO NOTHING;
    """)

def downgrade() -> None:
    op.execute("DELETE FROM users WHERE email IN ('admin@siswork.local', 'soporte@siswork.local')")