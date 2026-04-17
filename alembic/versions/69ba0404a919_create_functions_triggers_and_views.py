"""create_functions_triggers_and_views

Revision ID: 69ba0404a919
Revises: 7300de26d232
Create Date: 2026-04-17 16:16:38.031914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69ba0404a919'
down_revision: Union[str, Sequence[str], None] = '7300de26d232'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    tables_with_updated_at = [
        "users",
        "user_two_factor",
        "user_addresses",
        "professional_profiles",
        "certifications",
        "service_requests",
        "service_ratings",
        "professional_validation_queue",
    ]

    for table in tables_with_updated_at:
        op.execute(f"""
        DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};
        CREATE TRIGGER trg_{table}_updated_at
        BEFORE UPDATE ON {table}
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
        """)

    op.execute("""
    CREATE OR REPLACE FUNCTION recalculate_professional_rating(profile_id_param UUID)
    RETURNS VOID AS $$
    BEGIN
        UPDATE professional_profiles
        SET
            average_rating = COALESCE(
                (SELECT ROUND(AVG(score)::numeric, 2)
                 FROM service_ratings
                 WHERE professional_profile_id = profile_id_param),
                0.00
            ),
            ratings_count = (
                SELECT COUNT(*)
                FROM service_ratings
                WHERE professional_profile_id = profile_id_param
            )
        WHERE id = profile_id_param;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION trg_recalculate_professional_rating()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'DELETE' THEN
            PERFORM recalculate_professional_rating(OLD.professional_profile_id);
            RETURN OLD;
        ELSE
            PERFORM recalculate_professional_rating(NEW.professional_profile_id);
            IF TG_OP = 'UPDATE'
               AND OLD.professional_profile_id IS NOT NULL
               AND OLD.professional_profile_id <> NEW.professional_profile_id THEN
                PERFORM recalculate_professional_rating(OLD.professional_profile_id);
            END IF;
            RETURN NEW;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    DROP TRIGGER IF EXISTS trg_service_ratings_recalculate_professional_rating ON service_ratings;
    CREATE TRIGGER trg_service_ratings_recalculate_professional_rating
    AFTER INSERT OR UPDATE OR DELETE ON service_ratings
    FOR EACH ROW
    EXECUTE FUNCTION trg_recalculate_professional_rating();
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION recalculate_completed_services(profile_id_param UUID)
    RETURNS VOID AS $$
    BEGIN
        UPDATE professional_profiles
        SET completed_services_count = (
            SELECT COUNT(*)
            FROM service_requests
            WHERE assigned_professional_profile_id = profile_id_param
              AND status = 'COMPLETED'
        )
        WHERE id = profile_id_param;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    CREATE OR REPLACE FUNCTION trg_recalculate_completed_services()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'DELETE' THEN
            IF OLD.assigned_professional_profile_id IS NOT NULL THEN
                PERFORM recalculate_completed_services(OLD.assigned_professional_profile_id);
            END IF;
            RETURN OLD;
        ELSE
            IF NEW.assigned_professional_profile_id IS NOT NULL THEN
                PERFORM recalculate_completed_services(NEW.assigned_professional_profile_id);
            END IF;

            IF TG_OP = 'UPDATE'
               AND OLD.assigned_professional_profile_id IS NOT NULL
               AND OLD.assigned_professional_profile_id <> NEW.assigned_professional_profile_id THEN
                PERFORM recalculate_completed_services(OLD.assigned_professional_profile_id);
            END IF;

            RETURN NEW;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    DROP TRIGGER IF EXISTS trg_service_requests_recalculate_completed_services ON service_requests;
    CREATE TRIGGER trg_service_requests_recalculate_completed_services
    AFTER INSERT OR UPDATE OR DELETE ON service_requests
    FOR EACH ROW
    EXECUTE FUNCTION trg_recalculate_completed_services();
    """)

    op.execute("""
    CREATE OR REPLACE VIEW public_professional_profiles_view AS
    SELECT
        pp.id AS professional_profile_id,
        u.id AS user_id,
        u.first_name,
        u.last_name,
        CONCAT(u.first_name, ' ', u.last_name) AS full_name,
        pp.bio,
        pp.years_experience,
        pp.main_zone,
        pp.average_rating,
        pp.ratings_count,
        pp.completed_services_count,
        pp.available_now,
        u.phone,
        u.whatsapp_number,
        (
            SELECT string_agg(s.name, ', ' ORDER BY s.name)
            FROM professional_specialties ps
            JOIN specialties s ON s.id = ps.specialty_id
            WHERE ps.professional_profile_id = pp.id
        ) AS specialties,
        pp.verification_status
    FROM professional_profiles pp
    JOIN users u ON u.id = pp.user_id
    WHERE u.status = 'ACTIVE'
      AND pp.verification_status = 'APPROVED'
      AND pp.public_contact_enabled = true;
    """)

    op.execute("""
    CREATE OR REPLACE VIEW admin_dashboard_summary_view AS
    SELECT
        (SELECT COUNT(*) FROM users WHERE deleted_at IS NULL) AS total_users,
        (SELECT COUNT(*) FROM users WHERE role = 'CLIENT' AND deleted_at IS NULL) AS total_clients,
        (SELECT COUNT(*) FROM users WHERE role = 'PROFESSIONAL' AND deleted_at IS NULL) AS total_professionals,
        (SELECT COUNT(*) FROM service_requests) AS total_service_requests,
        (SELECT COUNT(*) FROM service_requests WHERE status = 'OPEN') AS open_service_requests,
        (SELECT COUNT(*) FROM service_requests WHERE status = 'COMPLETED') AS completed_service_requests,
        (
            SELECT COUNT(*)
            FROM professional_validation_queue
            WHERE status IN ('PENDING', 'IN_REVIEW')
        ) AS pending_validations,
        (
            SELECT ROUND(AVG(score)::numeric, 2)
            FROM service_ratings
        ) AS platform_average_rating;
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS admin_dashboard_summary_view")
    op.execute("DROP VIEW IF EXISTS public_professional_profiles_view")

    op.execute("DROP TRIGGER IF EXISTS trg_service_requests_recalculate_completed_services ON service_requests")
    op.execute("DROP FUNCTION IF EXISTS trg_recalculate_completed_services()")
    op.execute("DROP FUNCTION IF EXISTS recalculate_completed_services(UUID)")

    op.execute("DROP TRIGGER IF EXISTS trg_service_ratings_recalculate_professional_rating ON service_ratings")
    op.execute("DROP FUNCTION IF EXISTS trg_recalculate_professional_rating()")
    op.execute("DROP FUNCTION IF EXISTS recalculate_professional_rating(UUID)")

    for table in [
        "professional_validation_queue",
        "service_ratings",
        "service_requests",
        "certifications",
        "professional_profiles",
        "user_addresses",
        "user_two_factor",
        "users",
    ]:
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table}")

    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")