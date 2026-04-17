"""create_admin_tracking_and_support_tables

Revision ID: 7300de26d232
Revises: 0eb04e33798b
Create Date: 2026-04-17 16:12:31.579485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7300de26d232'
down_revision: Union[str, Sequence[str], None] = '0eb04e33798b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


verification_status_enum = sa.Enum(
    "PENDING",
    "IN_REVIEW",
    "APPROVED",
    "REJECTED",
    name="verification_status_enum",
)

audit_action_enum = sa.Enum(
    "LOGIN",
    "LOGOUT",
    "REGISTER",
    "EDIT_PROFILE",
    "CREATE_REQUEST",
    "EDIT_REQUEST",
    "DELETE_REQUEST",
    "APPLY_TO_REQUEST",
    "ACCEPT_APPLICATION",
    "REJECT_APPLICATION",
    "RATE_SERVICE",
    "UPLOAD_CERTIFICATION",
    "VALIDATE_PROFESSIONAL",
    "REJECT_PROFESSIONAL",
    "SUSPEND_USER",
    "ACTIVATE_USER",
    name="audit_action_enum",
)

report_type_enum = sa.Enum(
    "USERS",
    "PROFESSIONALS",
    "REQUESTS",
    "RATINGS",
    "SPECIALTIES",
    "VALIDATIONS",
    "DASHBOARD",
    name="report_type_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    verification_status_enum.create(bind, checkfirst=True)
    audit_action_enum.create(bind, checkfirst=True)
    report_type_enum.create(bind, checkfirst=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS saved_professionals (
        id UUID PRIMARY KEY,
        user_id UUID NOT NULL,
        professional_profile_id UUID NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_saved_professionals_user_id
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT fk_saved_professionals_professional_profile_id
            FOREIGN KEY (professional_profile_id) REFERENCES professional_profiles(id) ON DELETE CASCADE,
        CONSTRAINT uq_saved_professionals_user_profile
            UNIQUE (user_id, professional_profile_id)
    )
    """)

    op.create_index("ix_saved_professionals_user_id", "saved_professionals", ["user_id"], unique=False, if_not_exists=True)
    op.create_index(
        "ix_saved_professionals_professional_profile_id",
        "saved_professionals",
        ["professional_profile_id"],
        unique=False,
        if_not_exists=True,
    )

    op.execute("""
    CREATE TABLE IF NOT EXISTS search_history (
        id UUID PRIMARY KEY,
        user_id UUID,
        search_term VARCHAR(255),
        specialty_id UUID,
        zone VARCHAR(100),
        minimum_rating NUMERIC(2, 1),
        available_now BOOLEAN,
        results_count INTEGER NOT NULL DEFAULT 0,
        searched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_search_history_user_id
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
        CONSTRAINT fk_search_history_specialty_id
            FOREIGN KEY (specialty_id) REFERENCES specialties(id) ON DELETE SET NULL,
        CONSTRAINT ck_search_history_minimum_rating_range
            CHECK (minimum_rating IS NULL OR (minimum_rating >= 0 AND minimum_rating <= 5))
    )
    """)

    op.create_index("ix_search_history_user_id", "search_history", ["user_id"], unique=False, if_not_exists=True)
    op.create_index("ix_search_history_specialty_id", "search_history", ["specialty_id"], unique=False, if_not_exists=True)
    op.create_index("ix_search_history_searched_at", "search_history", ["searched_at"], unique=False, if_not_exists=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS professional_validation_queue (
        id UUID PRIMARY KEY,
        professional_profile_id UUID NOT NULL,
        requested_by_user_id UUID NOT NULL,
        assigned_support_user_id UUID,
        status verification_status_enum NOT NULL DEFAULT 'PENDING',
        submitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        review_started_at TIMESTAMPTZ,
        resolved_at TIMESTAMPTZ,
        rejection_reason TEXT,
        waiting_time_minutes INTEGER,
        review_time_minutes INTEGER,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_prof_validation_queue_profile_id
            FOREIGN KEY (professional_profile_id) REFERENCES professional_profiles(id) ON DELETE CASCADE,
        CONSTRAINT fk_prof_validation_queue_requested_by
            FOREIGN KEY (requested_by_user_id) REFERENCES users(id) ON DELETE RESTRICT,
        CONSTRAINT fk_prof_validation_queue_assigned_support
            FOREIGN KEY (assigned_support_user_id) REFERENCES users(id) ON DELETE SET NULL,
        CONSTRAINT uq_prof_validation_queue_profile_id UNIQUE (professional_profile_id),
        CONSTRAINT ck_prof_validation_queue_waiting_time_non_negative
            CHECK (waiting_time_minutes IS NULL OR waiting_time_minutes >= 0),
        CONSTRAINT ck_prof_validation_queue_review_time_non_negative
            CHECK (review_time_minutes IS NULL OR review_time_minutes >= 0)
    )
    """)

    op.create_index(
        "ix_prof_validation_queue_status",
        "professional_validation_queue",
        ["status"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_prof_validation_queue_assigned_support_user_id",
        "professional_validation_queue",
        ["assigned_support_user_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_prof_validation_queue_submitted_at",
        "professional_validation_queue",
        ["submitted_at"],
        unique=False,
        if_not_exists=True,
    )

    op.execute("""
    CREATE TABLE IF NOT EXISTS administrative_reports (
        id UUID PRIMARY KEY,
        generated_by_user_id UUID NOT NULL,
        report_type report_type_enum NOT NULL,
        parameters_json JSONB,
        generated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        file_url TEXT,
        CONSTRAINT fk_administrative_reports_generated_by
            FOREIGN KEY (generated_by_user_id) REFERENCES users(id) ON DELETE RESTRICT
    )
    """)

    op.create_index(
        "ix_administrative_reports_generated_by_user_id",
        "administrative_reports",
        ["generated_by_user_id"],
        unique=False,
        if_not_exists=True,
    )
    op.create_index(
        "ix_administrative_reports_report_type",
        "administrative_reports",
        ["report_type"],
        unique=False,
        if_not_exists=True,
    )

    op.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id UUID PRIMARY KEY,
        actor_user_id UUID,
        action audit_action_enum NOT NULL,
        entity VARCHAR(100) NOT NULL,
        entity_id UUID,
        previous_values JSONB,
        new_values JSONB,
        ip_address INET,
        user_agent TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_audit_logs_actor_user_id
            FOREIGN KEY (actor_user_id) REFERENCES users(id) ON DELETE SET NULL
    )
    """)

    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"], unique=False, if_not_exists=True)
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"], unique=False, if_not_exists=True)
    op.create_index("ix_audit_logs_entity_entity_id", "audit_logs", ["entity", "entity_id"], unique=False, if_not_exists=True)
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"], unique=False, if_not_exists=True)

    op.execute("""
    CREATE TABLE IF NOT EXISTS administrative_notes (
        id UUID PRIMARY KEY,
        author_user_id UUID NOT NULL,
        related_entity VARCHAR(100) NOT NULL,
        related_entity_id UUID NOT NULL,
        note TEXT NOT NULL,
        is_private BOOLEAN NOT NULL DEFAULT true,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT fk_administrative_notes_author_user_id
            FOREIGN KEY (author_user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS administrative_notes")

    op.drop_index("ix_audit_logs_created_at", table_name="audit_logs", if_exists=True)
    op.drop_index("ix_audit_logs_entity_entity_id", table_name="audit_logs", if_exists=True)
    op.drop_index("ix_audit_logs_action", table_name="audit_logs", if_exists=True)
    op.drop_index("ix_audit_logs_actor_user_id", table_name="audit_logs", if_exists=True)
    op.execute("DROP TABLE IF EXISTS audit_logs")

    op.drop_index("ix_administrative_reports_report_type", table_name="administrative_reports", if_exists=True)
    op.drop_index("ix_administrative_reports_generated_by_user_id", table_name="administrative_reports", if_exists=True)
    op.execute("DROP TABLE IF EXISTS administrative_reports")

    op.drop_index("ix_prof_validation_queue_submitted_at", table_name="professional_validation_queue", if_exists=True)
    op.drop_index("ix_prof_validation_queue_assigned_support_user_id", table_name="professional_validation_queue", if_exists=True)
    op.drop_index("ix_prof_validation_queue_status", table_name="professional_validation_queue", if_exists=True)
    op.execute("DROP TABLE IF EXISTS professional_validation_queue")

    op.drop_index("ix_search_history_searched_at", table_name="search_history", if_exists=True)
    op.drop_index("ix_search_history_specialty_id", table_name="search_history", if_exists=True)
    op.drop_index("ix_search_history_user_id", table_name="search_history", if_exists=True)
    op.execute("DROP TABLE IF EXISTS search_history")

    op.drop_index("ix_saved_professionals_professional_profile_id", table_name="saved_professionals", if_exists=True)
    op.drop_index("ix_saved_professionals_user_id", table_name="saved_professionals", if_exists=True)
    op.execute("DROP TABLE IF EXISTS saved_professionals")

    report_type_enum.drop(op.get_bind(), checkfirst=True)
    audit_action_enum.drop(op.get_bind(), checkfirst=True)
    verification_status_enum.drop(op.get_bind(), checkfirst=True)