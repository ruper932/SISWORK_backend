"""create_service_requests_applications_contacts_and_ratings

Revision ID: 0eb04e33798b
Revises: 1c85ff59b479
Create Date: 2026-04-17 16:08:49.377329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eb04e33798b'
down_revision: Union[str, Sequence[str], None] = '1c85ff59b479'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


service_request_status_enum = sa.Enum(
    "OPEN",
    "IN_PROGRESS",
    "ASSIGNED",
    "COMPLETED",
    "CANCELLED",
    name="service_request_status_enum",
)

application_status_enum = sa.Enum(
    "PENDING",
    "ACCEPTED",
    "REJECTED",
    "CANCELLED",
    name="application_status_enum",
)

contact_channel_enum = sa.Enum(
    "WHATSAPP",
    "PHONE",
    "INTERNAL_CHAT",
    "OTHER",
    name="contact_channel_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    service_request_status_enum.create(bind, checkfirst=True)
    application_status_enum.create(bind, checkfirst=True)
    contact_channel_enum.create(bind, checkfirst=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS service_requests (
        id UUID PRIMARY KEY,
        client_user_id UUID NOT NULL,
        specialty_id UUID NOT NULL,
        title VARCHAR(200) NOT NULL,
        description TEXT NOT NULL,
        department VARCHAR(100) NOT NULL DEFAULT 'La Paz',
        city VARCHAR(100) NOT NULL DEFAULT 'La Paz',
        zone VARCHAR(100) NOT NULL,
        address VARCHAR(255),
        reference TEXT,
        preferred_date DATE,
        preferred_start_time TIME,
        preferred_end_time TIME,
        minimum_budget NUMERIC(10, 2),
        maximum_budget NUMERIC(10, 2),
        status service_request_status_enum NOT NULL DEFAULT 'OPEN',
        assigned_professional_profile_id UUID,
        contact_channel contact_channel_enum NOT NULL DEFAULT 'WHATSAPP',
        is_active BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        closed_at TIMESTAMPTZ,
        CONSTRAINT fk_service_requests_client_user_id
            FOREIGN KEY (client_user_id) REFERENCES users(id) ON DELETE RESTRICT,
        CONSTRAINT fk_service_requests_specialty_id
            FOREIGN KEY (specialty_id) REFERENCES specialties(id) ON DELETE RESTRICT,
        CONSTRAINT fk_service_requests_assigned_professional_profile_id
            FOREIGN KEY (assigned_professional_profile_id) REFERENCES professional_profiles(id) ON DELETE SET NULL,
        CONSTRAINT ck_service_requests_budget_range
            CHECK (
                (minimum_budget IS NULL AND maximum_budget IS NULL)
                OR
                (minimum_budget IS NOT NULL AND maximum_budget IS NOT NULL AND minimum_budget >= 0 AND maximum_budget >= minimum_budget)
            ),
        CONSTRAINT ck_service_requests_preferred_time_range
            CHECK (
                (preferred_start_time IS NULL AND preferred_end_time IS NULL)
                OR
                (preferred_start_time IS NOT NULL AND preferred_end_time IS NOT NULL AND preferred_start_time < preferred_end_time)
            )
    )
    """)

    op.create_index("ix_service_requests_client_user_id", "service_requests", ["client_user_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_requests_specialty_id", "service_requests", ["specialty_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_requests_status", "service_requests", ["status"], unique=False, if_not_exists=True)
    op.create_index("ix_service_requests_zone", "service_requests", ["zone"], unique=False, if_not_exists=True)
    op.create_index("ix_service_requests_created_at", "service_requests", ["created_at"], unique=False, if_not_exists=True)
    op.create_index(
        "ix_service_requests_assigned_professional_profile_id",
        "service_requests",
        ["assigned_professional_profile_id"],
        unique=False,
        if_not_exists=True,
    )

    op.execute("""
    CREATE TABLE IF NOT EXISTS service_applications (
        id UUID PRIMARY KEY,
        service_request_id UUID NOT NULL,
        professional_profile_id UUID NOT NULL,
        proposal_message TEXT,
        estimated_price NUMERIC(10, 2),
        status application_status_enum NOT NULL DEFAULT 'PENDING',
        applied_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        responded_at TIMESTAMPTZ,
        cancelled_at TIMESTAMPTZ,
        CONSTRAINT fk_service_applications_service_request_id
            FOREIGN KEY (service_request_id) REFERENCES service_requests(id) ON DELETE CASCADE,
        CONSTRAINT fk_service_applications_professional_profile_id
            FOREIGN KEY (professional_profile_id) REFERENCES professional_profiles(id) ON DELETE CASCADE,
        CONSTRAINT uq_service_applications_request_professional
            UNIQUE (service_request_id, professional_profile_id),
        CONSTRAINT ck_service_applications_estimated_price_non_negative
            CHECK (estimated_price IS NULL OR estimated_price >= 0)
    )
    """)

    op.create_index("ix_service_applications_service_request_id", "service_applications", ["service_request_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_applications_professional_profile_id", "service_applications", ["professional_profile_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_applications_status", "service_applications", ["status"], unique=False, if_not_exists=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS service_contacts (
        id UUID PRIMARY KEY,
        service_request_id UUID,
        client_user_id UUID NOT NULL,
        professional_profile_id UUID NOT NULL,
        channel contact_channel_enum NOT NULL DEFAULT 'WHATSAPP',
        contacted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        note TEXT,
        CONSTRAINT fk_service_contacts_service_request_id
            FOREIGN KEY (service_request_id) REFERENCES service_requests(id) ON DELETE SET NULL,
        CONSTRAINT fk_service_contacts_client_user_id
            FOREIGN KEY (client_user_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT fk_service_contacts_professional_profile_id
            FOREIGN KEY (professional_profile_id) REFERENCES professional_profiles(id) ON DELETE CASCADE
    )
    """)

    op.create_index("ix_service_contacts_service_request_id", "service_contacts", ["service_request_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_contacts_client_user_id", "service_contacts", ["client_user_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_contacts_professional_profile_id", "service_contacts", ["professional_profile_id"], unique=False, if_not_exists=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS service_ratings (
        id UUID PRIMARY KEY,
        service_request_id UUID NOT NULL,
        client_user_id UUID NOT NULL,
        professional_profile_id UUID NOT NULL,
        score INTEGER NOT NULL,
        comment TEXT,
        is_verified BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT uq_service_ratings_service_request_id UNIQUE (service_request_id),
        CONSTRAINT fk_service_ratings_service_request_id
            FOREIGN KEY (service_request_id) REFERENCES service_requests(id) ON DELETE CASCADE,
        CONSTRAINT fk_service_ratings_client_user_id
            FOREIGN KEY (client_user_id) REFERENCES users(id) ON DELETE RESTRICT,
        CONSTRAINT fk_service_ratings_professional_profile_id
            FOREIGN KEY (professional_profile_id) REFERENCES professional_profiles(id) ON DELETE RESTRICT,
        CONSTRAINT ck_service_ratings_score_range CHECK (score BETWEEN 1 AND 5)
    )
    """)

    op.create_index("ix_service_ratings_professional_profile_id", "service_ratings", ["professional_profile_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_ratings_client_user_id", "service_ratings", ["client_user_id"], unique=False, if_not_exists=True)
    op.create_index("ix_service_ratings_score", "service_ratings", ["score"], unique=False, if_not_exists=True)


def downgrade() -> None:
    op.drop_index("ix_service_ratings_score", table_name="service_ratings", if_exists=True)
    op.drop_index("ix_service_ratings_client_user_id", table_name="service_ratings", if_exists=True)
    op.drop_index("ix_service_ratings_professional_profile_id", table_name="service_ratings", if_exists=True)
    op.execute("DROP TABLE IF EXISTS service_ratings")

    op.drop_index("ix_service_contacts_professional_profile_id", table_name="service_contacts", if_exists=True)
    op.drop_index("ix_service_contacts_client_user_id", table_name="service_contacts", if_exists=True)
    op.drop_index("ix_service_contacts_service_request_id", table_name="service_contacts", if_exists=True)
    op.execute("DROP TABLE IF EXISTS service_contacts")

    op.drop_index("ix_service_applications_status", table_name="service_applications", if_exists=True)
    op.drop_index("ix_service_applications_professional_profile_id", table_name="service_applications", if_exists=True)
    op.drop_index("ix_service_applications_service_request_id", table_name="service_applications", if_exists=True)
    op.execute("DROP TABLE IF EXISTS service_applications")

    op.drop_index("ix_service_requests_assigned_professional_profile_id", table_name="service_requests", if_exists=True)
    op.drop_index("ix_service_requests_created_at", table_name="service_requests", if_exists=True)
    op.drop_index("ix_service_requests_zone", table_name="service_requests", if_exists=True)
    op.drop_index("ix_service_requests_status", table_name="service_requests", if_exists=True)
    op.drop_index("ix_service_requests_specialty_id", table_name="service_requests", if_exists=True)
    op.drop_index("ix_service_requests_client_user_id", table_name="service_requests", if_exists=True)
    op.execute("DROP TABLE IF EXISTS service_requests")

    contact_channel_enum.drop(op.get_bind(), checkfirst=True)
    application_status_enum.drop(op.get_bind(), checkfirst=True)
    service_request_status_enum.drop(op.get_bind(), checkfirst=True)