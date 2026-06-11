# SISWORK BACKEND - AI CONTEXT

Generated on: vie 22 may 2026 11:56:56 -04

## PROJECT STRUCTURE
```
.
├── AI_READY_CONTEXT.md
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 08a5dd61225b_add_birth_date_validation.py
│       ├── 1160505b3d4d_add_marketplace_system.py
│       ├── 313fa34836f3_initial_schema.py
│       ├── 71720a3c289c_marketplace_module.py
│       └── 8552ba5e40e1_add_verification_system.py
├── alembic.ini
├── app
│   ├── api
│   │   ├── deps
│   │   │   └── auth.py
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── admin.py
│   │       ├── applications.py
│   │       ├── auth.py
│   │       ├── endpoints
│   │       │   └── __init__.py
│   │       ├── __init__.py
│   │       ├── professionals.py
│   │       ├── requests.py
│   │       ├── support.py
│   │       └── users.py
│   ├── config.py
│   ├── core
│   │   ├── __init__.py
│   │   └── security.py
│   ├── db
│   │   ├── database.py
│   │   ├── enums.py
│   │   ├── __init__.py
│   │   ├── mixins.py
│   │   └── session.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── application.py
│   │   ├── audit_log.py
│   │   ├── file.py
│   │   ├── __init__.py
│   │   ├── mixins.py
│   │   ├── professional_availability.py
│   │   ├── professional_profile.py
│   │   ├── professional_specialty.py
│   │   ├── request.py
│   │   ├── review.py
│   │   ├── role.py
│   │   ├── specialty.py
│   │   ├── user.py
│   │   ├── user_role.py
│   │   ├── verification_document.py
│   │   ├── verification.py
│   │   └── verification_request.py
│   ├── repositories
│   │   ├── application_repository.py
│   │   ├── __init__.py
│   │   ├── request_repository.py
│   │   ├── role_repository.py
│   │   └── user_repository.py
│   ├── schemas
│   │   ├── application.py
│   │   ├── __init__.py
│   │   ├── professional.py
│   │   ├── request.py
│   │   ├── token.py
│   │   └── user.py
│   ├── services
│   │   ├── application_service.py
│   │   ├── auth_service.py
│   │   ├── __init__.py
│   │   ├── professional_service.py
│   │   ├── request_service.py
│   │   └── verification_service.py
│   └── utils
│       └── __init__.py
├── README.md
├── requirements.txt
├── scripts
│   ├── generate_ai_context.sh
│   └── seed.py
└── tests
    └── __init__.py

17 directories, 71 files
```

## REQUIREMENTS
```txt
alembic==1.18.4
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.13.0
bcrypt==5.0.0
click==8.4.1
ecdsa==0.19.2
fastapi==0.136.1
greenlet==3.5.1
h11==0.16.0
idna==3.16
Mako==1.3.12
MarkupSafe==3.0.3
passlib==1.7.4
psycopg2-binary==2.9.12
pyasn1==0.6.3
pydantic==2.13.4
pydantic-settings==2.14.1
pydantic_core==2.46.4
python-dotenv==1.2.2
python-jose==3.5.0
python-multipart==0.0.29
rsa==4.9.1
six==1.17.0
SQLAlchemy==2.0.49
starlette==1.0.1
typing-inspection==0.4.2
typing_extensions==4.15.0
uvicorn==0.47.0
```

## ENVIRONMENT VARIABLES
```env
DATABASE_URL=postgresql://ruper:demons312es@localhost:5432/siswork_api
JWT_SECRET_KEY=***
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24```

## FASTAPI ROUTES DETECTED

app/api/v1/professionals.py:@router.post(
app/api/v1/admin.py:@router.get("/dashboard")
app/api/v1/users.py:@router.get(
app/api/v1/support.py:@router.post(
app/api/v1/support.py:@router.post(
app/api/v1/auth.py:@router.post(
app/api/v1/auth.py:@router.post(

## SQLALCHEMY TABLES

app/models/role.py:    __tablename__ = "roles"
app/models/specialty.py:    __tablename__ = "specialties"
app/models/application.py:    __tablename__ = "applications"
app/models/professional_profile.py:    __tablename__ = "professional_profiles"
app/models/user_role.py:    __tablename__ = "user_roles"
app/models/review.py:    __tablename__ = "reviews"
app/models/professional_availability.py:    __tablename__ = "professional_availabilities"
app/models/verification_document.py:    __tablename__ = "verification_documents"
app/models/file.py:    __tablename__ = "files"
app/models/user.py:    __tablename__ = "users"
app/models/request.py:    __tablename__ = "requests"
app/models/professional_specialty.py:    __tablename__ = "professional_specialties"
app/models/verification_request.py:    __tablename__ = "verification_requests"

## ENUMS

```python
import enum

from enum import Enum

class RoleEnum(str, Enum):
    CLIENT = "CLIENT"
    PROFESSIONAL = "PROFESSIONAL"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    SUPERADMIN = "SUPERADMIN"


class VerificationStatusEnum(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class RequestStatusEnum(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ApplicationStatusEnum(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    COMPLETED = "COMPLETED"


class VerificationDocumentTypeEnum(str, Enum):
    ID_CARD_FRONT = "ID_CARD_FRONT"
    ID_CARD_BACK = "ID_CARD_BACK"
    SELFIE = "SELFIE"
    CERTIFICATE = "CERTIFICATE"
    PDF_CERTIFICATION = "PDF_CERTIFICATION"

class RequestStatusEnum(str, enum.Enum):

    PENDING = "PENDING"

    ASSIGNED = "ASSIGNED"

    IN_PROGRESS = "IN_PROGRESS"

    COMPLETED = "COMPLETED"

    CANCELLED = "CANCELLED"


class ApplicationStatusEnum(str, enum.Enum):

    PENDING = "PENDING"

    ACCEPTED = "ACCEPTED"

    REJECTED = "REJECTED"

    CANCELLED = "CANCELLED"


class UrgencyLevelEnum(str, enum.Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"```

## SOURCE CODE


---

## FILE: alembic/env.py

```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

from app.config import settings
from app.db.database import Base

# IMPORTAR MODELOS
from app.models import *


# Alembic Config object
config = context.config

# INYECTAR DATABASE_URL DESDE .env
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL
)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()```


---

## FILE: alembic/versions/08a5dd61225b_add_birth_date_validation.py

```python
"""add birth date validation

Revision ID: 08a5dd61225b
Revises: 1160505b3d4d
Create Date: 2026-05-22 10:55:38.724134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08a5dd61225b'
down_revision: Union[str, Sequence[str], None] = '1160505b3d4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'birth_date',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'birth_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###
```


---

## FILE: alembic/versions/1160505b3d4d_add_marketplace_system.py

```python
"""add marketplace system

Revision ID: 1160505b3d4d
Revises: 8552ba5e40e1
Create Date: 2026-05-22 10:46:51.053272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1160505b3d4d'
down_revision: Union[str, Sequence[str], None] = '8552ba5e40e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('client_ci', sa.String(length=20), nullable=False),
    sa.Column('specialty_id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('zone', sa.String(length=100), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('budget_min', sa.Integer(), nullable=True),
    sa.Column('budget_max', sa.Integer(), nullable=True),
    sa.Column('status', postgresql.ENUM('OPEN', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', 'EXPIRED', name='request_status_enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['client_ci'], ['users.ci'], name=op.f('fk_requests_client_ci_requests')),
    sa.ForeignKeyConstraint(['specialty_id'], ['specialties.id'], name=op.f('fk_requests_specialty_id_requests')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_requests'))
    )
    op.create_index(op.f('ix_requests_city'), 'requests', ['city'], unique=False)
    op.create_index(op.f('ix_requests_client_ci'), 'requests', ['client_ci'], unique=False)
    op.create_index(op.f('ix_requests_specialty_id'), 'requests', ['specialty_id'], unique=False)
    op.create_index(op.f('ix_requests_status'), 'requests', ['status'], unique=False)
    op.create_index(op.f('ix_requests_zone'), 'requests', ['zone'], unique=False)
    op.create_table('applications',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('request_id', sa.UUID(), nullable=False),
    sa.Column('professional_profile_id', sa.UUID(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('proposed_price', sa.Integer(), nullable=True),
    sa.Column('status', postgresql.ENUM('PENDING', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', 'COMPLETED', name='application_status_enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['professional_profile_id'], ['professional_profiles.id'], name=op.f('fk_applications_professional_profile_id_applications')),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], name=op.f('fk_applications_request_id_applications')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_applications')),
    sa.UniqueConstraint('request_id', 'professional_profile_id', name='uq_request_professional_application')
    )
    op.create_index(op.f('ix_applications_professional_profile_id'), 'applications', ['professional_profile_id'], unique=False)
    op.create_index(op.f('ix_applications_request_id'), 'applications', ['request_id'], unique=False)
    op.create_index(op.f('ix_applications_status'), 'applications', ['status'], unique=False)
    op.create_table('professional_availabilities',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('professional_profile_id', sa.UUID(), nullable=False),
    sa.Column('day_of_week', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['professional_profile_id'], ['professional_profiles.id'], name=op.f('fk_professional_availabilities_professional_profile_id_professional_availabilities')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_professional_availabilities')),
    sa.UniqueConstraint('professional_profile_id', 'day_of_week', name='uq_professional_day')
    )
    op.create_index(op.f('ix_professional_availabilities_professional_profile_id'), 'professional_availabilities', ['professional_profile_id'], unique=False)
    op.create_table('reviews',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('request_id', sa.UUID(), nullable=False),
    sa.Column('application_id', sa.UUID(), nullable=False),
    sa.Column('reviewer_ci', sa.String(length=20), nullable=False),
    sa.Column('professional_profile_id', sa.UUID(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint('rating >= 1 AND rating <= 5', name=op.f('ck_reviews_check_review_rating')),
    sa.ForeignKeyConstraint(['application_id'], ['applications.id'], name=op.f('fk_reviews_application_id_reviews')),
    sa.ForeignKeyConstraint(['professional_profile_id'], ['professional_profiles.id'], name=op.f('fk_reviews_professional_profile_id_reviews')),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], name=op.f('fk_reviews_request_id_reviews')),
    sa.ForeignKeyConstraint(['reviewer_ci'], ['users.ci'], name=op.f('fk_reviews_reviewer_ci_reviews')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_reviews'))
    )
    op.create_index(op.f('ix_reviews_application_id'), 'reviews', ['application_id'], unique=False)
    op.create_index(op.f('ix_reviews_professional_profile_id'), 'reviews', ['professional_profile_id'], unique=False)
    op.create_index(op.f('ix_reviews_request_id'), 'reviews', ['request_id'], unique=False)
    op.create_index(op.f('ix_reviews_reviewer_ci'), 'reviews', ['reviewer_ci'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reviews_reviewer_ci'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_request_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_professional_profile_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_application_id'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_index(op.f('ix_professional_availabilities_professional_profile_id'), table_name='professional_availabilities')
    op.drop_table('professional_availabilities')
    op.drop_index(op.f('ix_applications_status'), table_name='applications')
    op.drop_index(op.f('ix_applications_request_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_professional_profile_id'), table_name='applications')
    op.drop_table('applications')
    op.drop_index(op.f('ix_requests_zone'), table_name='requests')
    op.drop_index(op.f('ix_requests_status'), table_name='requests')
    op.drop_index(op.f('ix_requests_specialty_id'), table_name='requests')
    op.drop_index(op.f('ix_requests_client_ci'), table_name='requests')
    op.drop_index(op.f('ix_requests_city'), table_name='requests')
    op.drop_table('requests')
    # ### end Alembic commands ###
```


---

## FILE: alembic/versions/313fa34836f3_initial_schema.py

```python
"""initial_schema

Revision ID: 313fa34836f3
Revises: 
Create Date: 2026-05-22 10:39:28.002946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '313fa34836f3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles'))
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    op.create_table('users',
    sa.Column('ci', sa.String(length=20), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('mother_last_name', sa.String(length=100), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=False),
    sa.Column('whatsapp_enabled', sa.Boolean(), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('profile_photo_path', sa.String(length=500), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('zone', sa.String(length=100), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
    sa.Column('failed_login_attempts', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('ci', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_ci'), 'users', ['ci'], unique=False)
    op.create_index(op.f('ix_users_city'), 'users', ['city'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    op.create_index(op.f('ix_users_zone'), 'users', ['zone'], unique=False)
    op.create_table('professional_profiles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_ci', sa.String(length=20), nullable=False),
    sa.Column('bio', sa.String(length=1000), nullable=True),
    sa.Column('experience_years', sa.Integer(), nullable=False),
    sa.Column('verification_status', postgresql.ENUM('PENDING', 'UNDER_REVIEW', 'APPROVED', 'REJECTED', name='verification_status_enum'), nullable=False),
    sa.Column('rating_average', sa.Float(), nullable=False),
    sa.Column('rating_count', sa.Integer(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_ci'], ['users.ci'], name=op.f('fk_professional_profiles_user_ci_professional_profiles')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_professional_profiles'))
    )
    op.create_index(op.f('ix_professional_profiles_user_ci'), 'professional_profiles', ['user_ci'], unique=True)
    op.create_index(op.f('ix_professional_profiles_verification_status'), 'professional_profiles', ['verification_status'], unique=False)
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_ci', sa.String(length=20), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_user_roles_role_id_user_roles')),
    sa.ForeignKeyConstraint(['user_ci'], ['users.ci'], name=op.f('fk_user_roles_user_ci_user_roles')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_roles')),
    sa.UniqueConstraint('user_ci', 'role_id', name='uq_user_role')
    )
    op.create_index(op.f('ix_user_roles_role_id'), 'user_roles', ['role_id'], unique=False)
    op.create_index(op.f('ix_user_roles_user_ci'), 'user_roles', ['user_ci'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_roles_user_ci'), table_name='user_roles')
    op.drop_index(op.f('ix_user_roles_role_id'), table_name='user_roles')
    op.drop_table('user_roles')
    op.drop_index(op.f('ix_professional_profiles_verification_status'), table_name='professional_profiles')
    op.drop_index(op.f('ix_professional_profiles_user_ci'), table_name='professional_profiles')
    op.drop_table('professional_profiles')
    op.drop_index(op.f('ix_users_zone'), table_name='users')
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_city'), table_name='users')
    op.drop_index(op.f('ix_users_ci'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
```


---

## FILE: alembic/versions/71720a3c289c_marketplace_module.py

```python
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
    op.drop_column('applications', 'proposal_message')```


---

## FILE: alembic/versions/8552ba5e40e1_add_verification_system.py

```python
"""add verification system

Revision ID: 8552ba5e40e1
Revises: 313fa34836f3
Create Date: 2026-05-22 10:42:56.888193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8552ba5e40e1'
down_revision: Union[str, Sequence[str], None] = '313fa34836f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('specialties',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_specialties'))
    )
    op.create_index(op.f('ix_specialties_name'), 'specialties', ['name'], unique=True)
    op.create_table('files',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('uploaded_by_ci', sa.String(length=20), nullable=False),
    sa.Column('original_filename', sa.String(length=255), nullable=False),
    sa.Column('stored_filename', sa.String(length=255), nullable=False),
    sa.Column('file_path', sa.String(length=500), nullable=False),
    sa.Column('mime_type', sa.String(length=100), nullable=False),
    sa.Column('file_size', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['uploaded_by_ci'], ['users.ci'], name=op.f('fk_files_uploaded_by_ci_files')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_files')),
    sa.UniqueConstraint('stored_filename', name=op.f('uq_files_stored_filename'))
    )
    op.create_index(op.f('ix_files_uploaded_by_ci'), 'files', ['uploaded_by_ci'], unique=False)
    op.create_table('professional_specialties',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('professional_profile_id', sa.UUID(), nullable=False),
    sa.Column('specialty_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['professional_profile_id'], ['professional_profiles.id'], name=op.f('fk_professional_specialties_professional_profile_id_professional_specialties')),
    sa.ForeignKeyConstraint(['specialty_id'], ['specialties.id'], name=op.f('fk_professional_specialties_specialty_id_professional_specialties')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_professional_specialties')),
    sa.UniqueConstraint('professional_profile_id', 'specialty_id', name='uq_professional_specialty')
    )
    op.create_index(op.f('ix_professional_specialties_professional_profile_id'), 'professional_specialties', ['professional_profile_id'], unique=False)
    op.create_index(op.f('ix_professional_specialties_specialty_id'), 'professional_specialties', ['specialty_id'], unique=False)
    op.create_table('verification_requests',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('professional_profile_id', sa.UUID(), nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'UNDER_REVIEW', 'APPROVED', 'REJECTED', name='verification_request_status_enum'), nullable=False),
    sa.Column('rejection_reason', sa.String(length=1000), nullable=True),
    sa.Column('reviewed_by_ci', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['professional_profile_id'], ['professional_profiles.id'], name=op.f('fk_verification_requests_professional_profile_id_verification_requests')),
    sa.ForeignKeyConstraint(['reviewed_by_ci'], ['users.ci'], name=op.f('fk_verification_requests_reviewed_by_ci_verification_requests')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_verification_requests'))
    )
    op.create_index(op.f('ix_verification_requests_professional_profile_id'), 'verification_requests', ['professional_profile_id'], unique=False)
    op.create_index(op.f('ix_verification_requests_status'), 'verification_requests', ['status'], unique=False)
    op.create_table('verification_documents',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('verification_request_id', sa.UUID(), nullable=False),
    sa.Column('file_id', sa.UUID(), nullable=False),
    sa.Column('document_type', postgresql.ENUM('ID_CARD_FRONT', 'ID_CARD_BACK', 'SELFIE', 'CERTIFICATE', 'PDF_CERTIFICATION', name='verification_document_type_enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], name=op.f('fk_verification_documents_file_id_verification_documents')),
    sa.ForeignKeyConstraint(['verification_request_id'], ['verification_requests.id'], name=op.f('fk_verification_documents_verification_request_id_verification_documents')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_verification_documents'))
    )
    op.create_index(op.f('ix_verification_documents_file_id'), 'verification_documents', ['file_id'], unique=False)
    op.create_index(op.f('ix_verification_documents_verification_request_id'), 'verification_documents', ['verification_request_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_verification_documents_verification_request_id'), table_name='verification_documents')
    op.drop_index(op.f('ix_verification_documents_file_id'), table_name='verification_documents')
    op.drop_table('verification_documents')
    op.drop_index(op.f('ix_verification_requests_status'), table_name='verification_requests')
    op.drop_index(op.f('ix_verification_requests_professional_profile_id'), table_name='verification_requests')
    op.drop_table('verification_requests')
    op.drop_index(op.f('ix_professional_specialties_specialty_id'), table_name='professional_specialties')
    op.drop_index(op.f('ix_professional_specialties_professional_profile_id'), table_name='professional_specialties')
    op.drop_table('professional_specialties')
    op.drop_index(op.f('ix_files_uploaded_by_ci'), table_name='files')
    op.drop_table('files')
    op.drop_index(op.f('ix_specialties_name'), table_name='specialties')
    op.drop_table('specialties')
    # ### end Alembic commands ###
```


---

## FILE: app/api/deps/auth.py

```python
from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from app.repositories.role_repository import RoleRepository

from sqlalchemy.orm import Session

from app.core.security import decode_token

from app.db.session import get_db

from app.models.user import User

from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    ci = payload.get("sub")

    if not ci:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = UserRepository.get_by_ci(
        db,
        ci,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

def require_roles(
    allowed_roles: list[str],
):

    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):

        user_roles = RoleRepository.get_user_roles(
            db,
            current_user.ci,
        )

        has_permission = any(
            role in allowed_roles
            for role in user_roles
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker```


---

## FILE: app/api/__init__.py

```python
```


---

## FILE: app/api/v1/admin.py

```python
from fastapi import (
    APIRouter,
    Depends,
)

from app.api.deps.auth import require_roles

from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_roles(
            ["ADMIN", "SUPERADMIN"],
        )
    ),
):

    return {
        "message": "Welcome admin",
        "user": current_user.ci,
    }```


---

## FILE: app/api/v1/applications.py

```python
```


---

## FILE: app/api/v1/auth.py

```python
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    OAuth2PasswordRequestForm,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.schemas.token import Token

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    try:

        user = AuthService.register(
            db,
            user_data,
        )

        return user

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    try:

        token = AuthService.login(
            db,
            form_data.username,
            form_data.password,
        )

        if not token:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    except Exception as e:

        raise HTTPException(
            status_code=401,
            detail=str(e),
        )```


---

## FILE: app/api/v1/endpoints/__init__.py

```python
```


---

## FILE: app/api/v1/__init__.py

```python
```


---

## FILE: app/api/v1/professionals.py

```python
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user

from app.db.session import get_db

from app.models.user import User

from app.schemas.professional import (
    VerificationRequestResponse,
)

from app.services.professional_service import (
    ProfessionalService,
)


router = APIRouter(
    prefix="/professionals",
    tags=["Professionals"],
)


@router.post(
    "/request-verification",
    response_model=VerificationRequestResponse,
)
async def request_verification(
    ci_photo: UploadFile = File(...),
    selfie_photo: UploadFile = File(...),
    certificate_pdf: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    verification_request = (
        await ProfessionalService.request_verification(
            db=db,
            current_user=current_user,
            ci_photo=ci_photo,
            selfie_photo=selfie_photo,
            certificate_pdf=certificate_pdf,
        )
    )

    return verification_request```


---

## FILE: app/api/v1/requests.py

```python
```


---

## FILE: app/api/v1/support.py

```python
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.api.deps.auth import require_roles

from app.db.session import get_db

from app.models.user import User

from app.services.verification_service import (
    VerificationService,
)


router = APIRouter(
    prefix="/support",
    tags=["Support"],
)


@router.post(
    "/approve/{verification_request_id}",
)
def approve_verification(
    verification_request_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "SUPPORT",
                "ADMIN",
                "SUPERADMIN",
            ]
        )
    ),
):

    try:

        result = (
            VerificationService.approve_verification(
                db,
                verification_request_id,
                current_user.ci,
            )
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/reject/{verification_request_id}",
)
def reject_verification(
    verification_request_id: UUID,
    rejection_reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "SUPPORT",
                "ADMIN",
                "SUPERADMIN",
            ]
        )
    ),
):

    try:

        result = (
            VerificationService.reject_verification(
                db,
                verification_request_id,
                current_user.ci,
                rejection_reason,
            )
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )```


---

## FILE: app/api/v1/users.py

```python
from fastapi import (
    APIRouter,
    Depends,
)

from app.api.deps.auth import get_current_user

from app.models.user import User

from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):

    roles = [
        user_role.role.name
        for user_role in current_user.user_roles
    ]

    return {
        "ci": current_user.ci,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "mother_last_name": current_user.mother_last_name,
        "birth_date": current_user.birth_date,
        "email": current_user.email,
        "phone": current_user.phone,
        "city": current_user.city,
        "zone": current_user.zone,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "roles": roles,
    }```


---

## FILE: app/config.py

```python
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_HOURS: int

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()```


---

## FILE: app/core/__init__.py

```python
```


---

## FILE: app/core/security.py

```python
from datetime import datetime, timedelta, UTC

from jose import jwt
from jose import JWTError

from pwdlib import PasswordHash

from app.config import settings


password_hash = PasswordHash.recommended()


def hash_password(
    password: str,
) -> str:

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
):

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            hours=settings.ACCESS_TOKEN_EXPIRE_HOURS
        )

    to_encode = {
        "sub": subject,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


def decode_token(
    token: str,
):

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        return payload

    except JWTError:
        return None```


---

## FILE: app/db/database.py

```python
from sqlalchemy import create_engine

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

from app.config import settings


DATABASE_URL = settings.DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    echo=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()```


---

## FILE: app/db/enums.py

```python
import enum

from enum import Enum

class RoleEnum(str, Enum):
    CLIENT = "CLIENT"
    PROFESSIONAL = "PROFESSIONAL"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    SUPERADMIN = "SUPERADMIN"


class VerificationStatusEnum(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class RequestStatusEnum(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ApplicationStatusEnum(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    COMPLETED = "COMPLETED"


class VerificationDocumentTypeEnum(str, Enum):
    ID_CARD_FRONT = "ID_CARD_FRONT"
    ID_CARD_BACK = "ID_CARD_BACK"
    SELFIE = "SELFIE"
    CERTIFICATE = "CERTIFICATE"
    PDF_CERTIFICATION = "PDF_CERTIFICATION"

class RequestStatusEnum(str, enum.Enum):

    PENDING = "PENDING"

    ASSIGNED = "ASSIGNED"

    IN_PROGRESS = "IN_PROGRESS"

    COMPLETED = "COMPLETED"

    CANCELLED = "CANCELLED"


class ApplicationStatusEnum(str, enum.Enum):

    PENDING = "PENDING"

    ACCEPTED = "ACCEPTED"

    REJECTED = "REJECTED"

    CANCELLED = "CANCELLED"


class UrgencyLevelEnum(str, enum.Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"```


---

## FILE: app/db/__init__.py

```python
```


---

## FILE: app/db/mixins.py

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class SoftDeleteMixin:

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class UUIDMixin:

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )```


---

## FILE: app/db/session.py

```python
from app.db.database import SessionLocal


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()```


---

## FILE: app/__init__.py

```python
```


---

## FILE: app/main.py

```python
from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.admin import router as admin_router

from app.api.v1.professionals import (
    router as professionals_router,
)

from app.api.v1.support import (
    router as support_router,
)


app = FastAPI(
    title="SISWORK API",
)


app.include_router(auth_router)

app.include_router(users_router)

app.include_router(admin_router)

app.include_router(professionals_router)

app.include_router(support_router)```


---

## FILE: app/models/application.py

```python
import uuid

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Numeric,
    Integer,
    Enum,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

from app.models.mixins import TimestampMixin

from app.db.enums import (
    ApplicationStatusEnum,
)


class Application(
    Base,
    TimestampMixin,
):

    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("requests.id"),
        nullable=False,
        index=True,
    )

    professional_profile_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    proposal_message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    proposed_price: Mapped[
        float | None
    ] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    estimated_time_hours: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[
        ApplicationStatusEnum
    ] = mapped_column(
        Enum(
            ApplicationStatusEnum,
            name="application_status_enum",
        ),
        default=ApplicationStatusEnum.PENDING,
        nullable=False,
    )

    request = relationship(
        "Request",
        back_populates="applications",
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="applications",
    )

    __table_args__ = (
        UniqueConstraint(
            "request_id",
            "professional_profile_id",
            name="uq_application_request_professional",
        ),
    )```


---

## FILE: app/models/audit_log.py

```python
```


---

## FILE: app/models/file.py

```python
import uuid

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class File(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    uploaded_by_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    uploaded_by = relationship(
        "User",
    )```


---

## FILE: app/models/__init__.py

```python
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole

from app.models.file import File

from app.models.specialty import Specialty
from app.models.professional_specialty import ProfessionalSpecialty

from app.models.professional_profile import ProfessionalProfile
from app.models.professional_availability import ProfessionalAvailability

from app.models.verification_request import VerificationRequest
from app.models.verification_document import VerificationDocument

from app.models.request import Request
from app.models.application import Application

from app.models.review import Review```


---

## FILE: app/models/mixins.py

```python
from datetime import datetime, UTC

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import DateTime


class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )```


---

## FILE: app/models/professional_availability.py

```python
import uuid
from datetime import time

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Time,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class ProfessionalAvailability(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "professional_availabilities"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "day_of_week",
            name="uq_professional_day",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="availabilities",
    )```


---

## FILE: app/models/professional_profile.py

```python
import uuid

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.dialects.postgresql import ENUM, UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.enums import VerificationStatusEnum
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class ProfessionalProfile(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "professional_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        unique=True,
        nullable=False,
        index=True,
    )

    bio: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    verification_status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(
            VerificationStatusEnum,
            name="verification_status_enum",
            create_type=True,
        ),
        default=VerificationStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    rating_average: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    rating_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="professional_profile",
    )
    verification_requests = relationship(
        "VerificationRequest",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    specialties = relationship(
        "ProfessionalSpecialty",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    applications = relationship(
        "Application",
        cascade="all, delete-orphan",
    )

    reviews = relationship(
        "Review",
        cascade="all, delete-orphan",
    )

    availabilities = relationship(
        "ProfessionalAvailability",
        cascade="all, delete-orphan",
    )
    applications = relationship(
        "Application",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )```


---

## FILE: app/models/professional_specialty.py

```python
import uuid

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import TimestampMixin


class ProfessionalSpecialty(
    Base,
    TimestampMixin,
):
    __tablename__ = "professional_specialties"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "specialty_id",
            name="uq_professional_specialty",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    specialty_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("specialties.id"),
        nullable=False,
        index=True,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
    )

    specialty = relationship(
        "Specialty",
        back_populates="professional_specialties",
    )```


---

## FILE: app/models/request.py

```python
import uuid

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Numeric,
    DateTime,
    Enum,
    Boolean,
    Index,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

from app.models.mixins import TimestampMixin

from app.db.enums import (
    RequestStatusEnum,
    UrgencyLevelEnum,
)


class Request(
    Base,
    TimestampMixin,
):

    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    client_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    specialty_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("specialties.id"),
        nullable=False,
        index=True,
    )

    assigned_professional_profile_id: Mapped[
        uuid.UUID | None
    ] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professional_profiles.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    budget: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    proposed_final_price: Mapped[
        float | None
    ] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    scheduled_date: Mapped[
        DateTime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    zone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    urgency: Mapped[UrgencyLevelEnum] = mapped_column(
        Enum(
            UrgencyLevelEnum,
            name="urgency_level_enum",
        ),
        default=UrgencyLevelEnum.MEDIUM,
    )

    status: Mapped[RequestStatusEnum] = mapped_column(
        Enum(
            RequestStatusEnum,
            name="request_status_enum",
        ),
        default=RequestStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    is_review_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    cancellation_reason: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    client = relationship(
        "User",
        foreign_keys=[client_ci],
    )

    specialty = relationship(
        "Specialty",
    )

    assigned_professional = relationship(
        "ProfessionalProfile",
    )

    applications = relationship(
        "Application",
        back_populates="request",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "idx_request_location",
            "city",
            "zone",
        ),
    )```


---

## FILE: app/models/review.py

```python
import uuid

from sqlalchemy import (
    String,
    Text,
    Integer,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

from app.models.mixins import TimestampMixin


class Review(
    Base,
    TimestampMixin,
):

    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id"),
        nullable=False,
        index=True,
    )

    reviewer_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
    )

    reviewed_user_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    application = relationship(
        "Application",
    )

    reviewer = relationship(
        "User",
        foreign_keys=[reviewer_ci],
    )

    reviewed_user = relationship(
        "User",
        foreign_keys=[reviewed_user_ci],
    )```


---

## FILE: app/models/role.py

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    user_roles = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )```


---

## FILE: app/models/specialty.py

```python
import uuid

from sqlalchemy import (
    Boolean,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class Specialty(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "specialties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    professional_specialties = relationship(
        "ProfessionalSpecialty",
        back_populates="specialty",
        cascade="all, delete-orphan",
    )```


---

## FILE: app/models/user.py

```python
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class User(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "users"

    ci: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    mother_last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    whatsapp_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    profile_photo_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    zone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    user_roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )```


---

## FILE: app/models/user_role.py

```python
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import TimestampMixin


class UserRole(
    Base,
    TimestampMixin,
):
    __tablename__ = "user_roles"

    __table_args__ = (
        UniqueConstraint(
            "user_ci",
            "role_id",
            name="uq_user_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="user_roles",
    )

    role = relationship(
        "Role",
        back_populates="user_roles",
    )```


---

## FILE: app/models/verification_document.py

```python
import uuid

from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import (
    ENUM,
    UUID,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.enums import VerificationDocumentTypeEnum
from app.db.mixins import TimestampMixin


class VerificationDocument(
    Base,
    TimestampMixin,
):
    __tablename__ = "verification_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    verification_request_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("verification_requests.id"),
        nullable=False,
        index=True,
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("files.id"),
        nullable=False,
        index=True,
    )

    document_type: Mapped[VerificationDocumentTypeEnum] = mapped_column(
        ENUM(
            VerificationDocumentTypeEnum,
            name="verification_document_type_enum",
            create_type=True,
        ),
        nullable=False,
    )

    verification_request = relationship(
        "VerificationRequest",
        back_populates="documents",
    )

    file = relationship(
        "File",
    )```


---

## FILE: app/models/verification.py

```python
```


---

## FILE: app/models/verification_request.py

```python
import uuid

from sqlalchemy import (
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import (
    ENUM,
    UUID,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.enums import VerificationStatusEnum
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class VerificationRequest(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "verification_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(
            VerificationStatusEnum,
            name="verification_request_status_enum",
            create_type=True,
        ),
        default=VerificationStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    reviewed_by_ci: Mapped[str | None] = mapped_column(
        ForeignKey("users.ci"),
        nullable=True,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
    )

    reviewed_by = relationship(
        "User",
    )

    documents = relationship(
        "VerificationDocument",
        back_populates="verification_request",
        cascade="all, delete-orphan",
    )```


---

## FILE: app/repositories/application_repository.py

```python
```


---

## FILE: app/repositories/__init__.py

```python
```


---

## FILE: app/repositories/request_repository.py

```python
```


---

## FILE: app/repositories/role_repository.py

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_role import UserRole
from app.models.role import Role


class RoleRepository:

    @staticmethod
    def get_user_roles(
        db: Session,
        user_ci: str,
    ):

        stmt = (
            select(Role.name)
            .join(
                UserRole,
                UserRole.role_id == Role.id,
            )
            .where(
                UserRole.user_ci == user_ci,
            )
        )

        result = db.execute(stmt)

        return result.scalars().all()
    
    @staticmethod
    def get_by_name(
        db: Session,
        role_name: str,
    ):

        stmt = select(Role).where(
            Role.name == role_name,
        )

        return db.scalar(stmt)```


---

## FILE: app/repositories/user_repository.py

```python

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User

from sqlalchemy.orm import joinedload

from app.models.user_role import UserRole
from app.models.role import Role
from sqlalchemy import or_

class UserRepository:

    @staticmethod
    def get_by_ci(
        db: Session,
        ci: str,
    ):
        stmt = (
            select(User)
            .options(
                joinedload(User.user_roles)
                .joinedload(UserRole.role)
            )
            .where(
                User.ci == ci,
                User.deleted_at.is_(None),
            )
        )

        return db.scalar(stmt)

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ):
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )

        return db.scalar(stmt)

    @staticmethod
    def create(
        db: Session,
        user: User,
    ):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    @staticmethod
    def get_by_ci_or_email(
        db: Session,
        identifier: str,
    ):

        stmt = (
            select(User)
            .where(
                or_(
                    User.ci == identifier,
                    User.email == identifier,
                ),
                User.deleted_at.is_(None),
            )
        )

        return db.scalar(stmt)```


---

## FILE: app/schemas/application.py

```python
```


---

## FILE: app/schemas/__init__.py

```python
```


---

## FILE: app/schemas/professional.py

```python
from uuid import UUID

from pydantic import BaseModel


class VerificationRequestResponse(BaseModel):

    id: UUID

    status: str

    rejection_reason: str | None = None

    class Config:
        from_attributes = True```


---

## FILE: app/schemas/request.py

```python
```


---

## FILE: app/schemas/token.py

```python
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"```


---

## FILE: app/schemas/user.py

```python
from datetime import date
from datetime import UTC
from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)


class UserCreate(BaseModel):

    ci: str

    first_name: str
    last_name: str
    mother_last_name: str | None = None

    birth_date: date

    email: EmailStr

    phone: str

    password: str

    city: str | None = None
    zone: str | None = None

    @field_validator("birth_date")
    @classmethod
    def validate_age(
        cls,
        value: date,
    ):

        today = datetime.now(UTC).date()

        age = (
            today.year
            - value.year
            - (
                (today.month, today.day)
                < (value.month, value.day)
            )
        )

        if age < 18:
            raise ValueError(
                "User must be at least 18 years old"
            )

        return value


class UserLogin(BaseModel):

    ci: str
    password: str


class UserResponse(BaseModel):

    ci: str

    first_name: str
    last_name: str
    mother_last_name: str | None = None

    birth_date: date

    email: str

    phone: str

    city: str | None = None
    zone: str | None = None

    is_active: bool
    is_verified: bool

    roles: list[str] = []

    class Config:
        from_attributes = True

    ci: str

    first_name: str
    last_name: str
    mother_last_name: str | None = None

    birth_date: date

    email: str

    phone: str

    city: str | None = None
    zone: str | None = None

    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True```


---

## FILE: app/services/application_service.py

```python
```


---

## FILE: app/services/auth_service.py

```python
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.models.user_role import UserRole

from app.repositories.role_repository import RoleRepository

class AuthService:

    @staticmethod
    def register(
        db,
        user_data,
    ):

        existing_user = UserRepository.get_by_ci(
            db,
            user_data.ci,
        )

        if existing_user:
            raise Exception("CI already registered")

        existing_email = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing_email:
            raise Exception("Email already registered")

        user = User(
            ci=user_data.ci,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            mother_last_name=user_data.mother_last_name,
            birth_date=user_data.birth_date,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hash_password(
                user_data.password
            ),
            city=user_data.city,
            zone=user_data.zone,
        )

        db.add(user)

        client_role = RoleRepository.get_by_name(
            db,
            "CLIENT",
        )

        if not client_role:
            raise Exception(
                "CLIENT role does not exist"
            )

        user_role = UserRole(
            user_ci=user.ci,
            role_id=client_role.id,
        )

        db.add(user_role)

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def login(
        db,
        identifier: str,
        password: str,
    ):

        user = UserRepository.get_by_ci_or_email(
            db,
            identifier,
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        access_token = create_access_token(
            subject=user.ci,
        )

        return access_token```


---

## FILE: app/services/__init__.py

```python
```


---

## FILE: app/services/professional_service.py

```python
import os
import uuid

from fastapi import UploadFile

from sqlalchemy import select

from app.models.file import File

from app.models.professional_profile import ProfessionalProfile

from app.models.verification_request import VerificationRequest

from app.models.verification_document import VerificationDocument

from app.db.enums import (
    VerificationStatusEnum,
    VerificationDocumentTypeEnum,
)


UPLOAD_DIR = "uploads/verification"


class ProfessionalService:

    @staticmethod
    async def request_verification(
        db,
        current_user,
        ci_photo: UploadFile,
        selfie_photo: UploadFile,
        certificate_pdf: UploadFile,
    ):

        existing_profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.user_ci
                == current_user.ci
            )
        )

        if not existing_profile:

            profile = ProfessionalProfile(
                user_ci=current_user.ci,
                verification_status=VerificationStatusEnum.PENDING,
            )

            db.add(profile)

            db.commit()

            db.refresh(profile)

        else:
            profile = existing_profile

        verification_request = VerificationRequest(
            professional_profile_id=profile.id,
            status=VerificationStatusEnum.PENDING,
        )

        db.add(verification_request)

        db.commit()

        db.refresh(verification_request)

        files_data = [
            (
                ci_photo,
                VerificationDocumentTypeEnum.CI_PHOTO,
            ),
            (
                selfie_photo,
                VerificationDocumentTypeEnum.SELFIE,
            ),
            (
                certificate_pdf,
                VerificationDocumentTypeEnum.CERTIFICATE,
            ),
        ]

        for upload_file, doc_type in files_data:

            extension = (
                upload_file.filename.split(".")[-1]
            )

            generated_name = (
                f"{uuid.uuid4()}.{extension}"
            )

            file_path = os.path.join(
                UPLOAD_DIR,
                generated_name,
            )

            with open(file_path, "wb") as buffer:
                content = await upload_file.read()
                buffer.write(content)

            file_record = File(
                uploaded_by_ci=current_user.ci,
                original_filename=upload_file.filename,
                stored_filename=generated_name,
                file_path=file_path,
                mime_type=upload_file.content_type,
                file_size=len(content),
            )

            db.add(file_record)

            db.commit()

            db.refresh(file_record)

            verification_document = VerificationDocument(
                verification_request_id=verification_request.id,
                file_id=file_record.id,
                document_type=doc_type,
            )

            db.add(verification_document)

            db.commit()

        return verification_request```


---

## FILE: app/services/request_service.py

```python
```


---

## FILE: app/services/verification_service.py

```python
from sqlalchemy import select

from app.models.role import Role

from app.models.user_role import UserRole

from app.models.professional_profile import (
    ProfessionalProfile,
)

from app.models.verification_request import (
    VerificationRequest,
)

from app.db.enums import VerificationStatusEnum


class VerificationService:

    @staticmethod
    def approve_verification(
        db,
        verification_request_id,
        reviewer_ci,
    ):

        verification_request = db.scalar(
            select(VerificationRequest).where(
                VerificationRequest.id
                == verification_request_id
            )
        )

        if not verification_request:
            raise Exception(
                "Verification request not found"
            )

        verification_request.status = (
            VerificationStatusEnum.APPROVED
        )

        verification_request.reviewed_by_ci = (
            reviewer_ci
        )

        profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id
                == verification_request.professional_profile_id
            )
        )

        profile.verification_status = (
            VerificationStatusEnum.APPROVED
        )

        role = db.scalar(
            select(Role).where(
                Role.name == "PROFESSIONAL"
            )
        )

        existing_role = db.scalar(
            select(UserRole).where(
                UserRole.user_ci == profile.user_ci,
                UserRole.role_id == role.id,
            )
        )

        if not existing_role:

            user_role = UserRole(
                user_ci=profile.user_ci,
                role_id=role.id,
            )

            db.add(user_role)

        db.commit()

        return verification_request

    @staticmethod
    def reject_verification(
        db,
        verification_request_id,
        reviewer_ci,
        rejection_reason,
    ):

        verification_request = db.scalar(
            select(VerificationRequest).where(
                VerificationRequest.id
                == verification_request_id
            )
        )

        if not verification_request:
            raise Exception(
                "Verification request not found"
            )

        verification_request.status = (
            VerificationStatusEnum.REJECTED
        )

        verification_request.reviewed_by_ci = (
            reviewer_ci
        )

        verification_request.rejection_reason = (
            rejection_reason
        )

        profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id
                == verification_request.professional_profile_id
            )
        )

        profile.verification_status = (
            VerificationStatusEnum.REJECTED
        )

        db.commit()

        return verification_request```


---

## FILE: app/utils/__init__.py

```python
```


---

## FILE: scripts/seed.py

```python
from datetime import date

from sqlalchemy import select

from app.db.session import SessionLocal

from app.core.security import hash_password

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


db = SessionLocal()


def seed_roles():

    roles = [
        "CLIENT",
        "PROFESSIONAL",
        "ADMIN",
        "SUPPORT",
        "SUPERADMIN",
    ]

    for role_name in roles:

        existing = db.scalar(
            select(Role).where(
                Role.name == role_name
            )
        )

        if not existing:

            role = Role(
                name=role_name,
            )

            db.add(role)

    db.commit()

    print("Roles seeded")


def seed_superadmin():

    existing = db.scalar(
        select(User).where(
            User.ci == "SUPERADMIN"
        )
    )

    if existing:
        print("Superadmin already exists")
        return

    user = User(
        ci="SUPERADMIN",
        first_name="Super",
        last_name="Admin",
        mother_last_name="System",
        birth_date=date(1990, 1, 1),
        email="superadmin@siswork.com",
        phone="70000000",
        password_hash=hash_password(
            "demons312es"
        ),
        city="La Paz",
        zone="Central",
        is_verified=True,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    role = db.scalar(
        select(Role).where(
            Role.name == "SUPERADMIN"
        )
    )

    user_role = UserRole(
        user_ci=user.ci,
        role_id=role.id,
    )

    db.add(user_role)

    db.commit()

    print("Superadmin seeded")


def seed_client():

    existing = db.scalar(
        select(User).where(
            User.ci == "CLIENT001"
        )
    )

    if existing:
        print("Client already exists")
        return

    user = User(
        ci="CLIENT001",
        first_name="Test",
        last_name="Client",
        mother_last_name="User",
        birth_date=date(1998, 5, 10),
        email="client@siswork.com",
        phone="71111111",
        password_hash=hash_password(
            "demons312es"
        ),
        city="La Paz",
        zone="Sopocachi",
        is_verified=False,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    role = db.scalar(
        select(Role).where(
            Role.name == "CLIENT"
        )
    )

    user_role = UserRole(
        user_ci=user.ci,
        role_id=role.id,
    )

    db.add(user_role)

    db.commit()

    print("Client seeded")


def run_seed():

    print("Starting seed...")

    seed_roles()

    seed_superadmin()

    seed_client()

    print("Seed completed")


if __name__ == "__main__":
    run_seed()```


---

## FILE: tests/__init__.py

```python
```

## FOREIGN KEYS DETECTED

app/models/application.py:    ForeignKey,
app/models/application.py:        ForeignKey("requests.id"),
app/models/application.py:        ForeignKey("professional_profiles.id"),
app/models/professional_profile.py:    ForeignKey,
app/models/professional_profile.py:        ForeignKey("users.ci"),
app/models/user_role.py:from sqlalchemy import ForeignKey, UniqueConstraint
app/models/user_role.py:        ForeignKey("users.ci"),
app/models/user_role.py:        ForeignKey("roles.id"),
app/models/review.py:    ForeignKey,
app/models/review.py:        ForeignKey("applications.id"),
app/models/review.py:        ForeignKey("users.ci"),
app/models/review.py:        ForeignKey("users.ci"),
app/models/professional_availability.py:    ForeignKey,
app/models/professional_availability.py:        ForeignKey("professional_profiles.id"),
app/models/verification_document.py:from sqlalchemy import ForeignKey
app/models/verification_document.py:        ForeignKey("verification_requests.id"),
app/models/verification_document.py:        ForeignKey("files.id"),
app/models/file.py:    ForeignKey,
app/models/file.py:        ForeignKey("users.ci"),
app/models/request.py:    ForeignKey,
app/models/request.py:        ForeignKey("users.ci"),
app/models/request.py:        ForeignKey("specialties.id"),
app/models/request.py:        ForeignKey("professional_profiles.id"),
app/models/professional_specialty.py:    ForeignKey,
app/models/professional_specialty.py:        ForeignKey("professional_profiles.id"),
app/models/professional_specialty.py:        ForeignKey("specialties.id"),
app/models/verification_request.py:    ForeignKey,
app/models/verification_request.py:        ForeignKey("professional_profiles.id"),
app/models/verification_request.py:        ForeignKey("users.ci"),

## REPOSITORY CLASSES

app/repositories/user_repository.py:class UserRepository:
app/repositories/role_repository.py:class RoleRepository:

## SERVICE CLASSES

app/services/auth_service.py:class AuthService:
app/services/verification_service.py:class VerificationService:
app/services/professional_service.py:class ProfessionalService:

## API ENDPOINT SUMMARY

app/api/v1/professionals.py:@router.post(
router.get /dashboard
app/api/v1/users.py:@router.get(
app/api/v1/support.py:@router.post(
app/api/v1/support.py:@router.post(
app/api/v1/auth.py:@router.post(
app/api/v1/auth.py:@router.post(

