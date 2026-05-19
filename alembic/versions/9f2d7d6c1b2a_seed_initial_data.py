"""seed initial demo data es schema

Revision ID: 9f2d7d6c1b2a
Revises: 8bc478457236
Create Date: 2026-05-08 16:16:00
"""

from alembic import op
from sqlalchemy import sql

revision = "9f2d7d6c1b2a"
down_revision = "8bc478457236"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Clientes y Profesionales adicionales
    op.execute(sql.text("""
    INSERT INTO public.users (
        id, first_name, last_name, email, password_hash, phone, whatsapp_number, 
        birth_date, gender, role, status, email_verified_at, is_active, 
        failed_login_attempts, created_at, updated_at
    ) VALUES
        ('33333333-3333-4333-8333-333333333333', 'Carlos', 'Mamani', 'carlos@siswork.local', crypt('Carlos123*', gen_salt('bf')), '73000001', '73000001', '1995-06-10', 'MALE', 'CLIENT', 'ACTIVE', now(), true, 0, now(), now()),
        ('44444444-4444-4444-8444-444444444444', 'Lucia', 'Quispe', 'lucia@siswork.local', crypt('Lucia123*', gen_salt('bf')), '73000002', '73000002', '1998-11-02', 'FEMALE', 'CLIENT', 'ACTIVE', now(), true, 0, now(), now()),
        ('55555555-5555-4555-8555-555555555555', 'Juan', 'Perez', 'juan.pro@siswork.local', crypt('Juan123*', gen_salt('bf')), '72000001', '72000001', '1989-04-14', 'MALE', 'PROFESSIONAL', 'ACTIVE', now(), true, 0, now(), now()),
        ('66666666-6666-4666-8666-666666666666', 'Maria', 'Choque', 'maria.pro@siswork.local', crypt('Maria123*', gen_salt('bf')), '72000002', '72000002', '1991-09-08', 'FEMALE', 'PROFESSIONAL', 'ACTIVE', now(), true, 0, now(), now())
    ON CONFLICT (email) DO NOTHING;
    """))

    # 2. Perfiles Profesionales
    op.execute(sql.text("""
    INSERT INTO public.professional_profiles (
        id, user_id, bio, years_experience, main_zone, service_radius_km, 
        verification_status, verified_by_user_id, average_rating, ratings_count,
        completed_services_count, available_now, created_at, updated_at
    ) VALUES
        ('77777777-7777-4777-8777-777777777777', '55555555-5555-4555-8555-555555555555', 'Experto en plomería y grifería.', 8, 'Sopocachi', 7.5, 'APPROVED', '11111111-1111-4111-8111-111111111111', 4.7, 1, 1, true, now(), now()),
        ('88888888-8888-4888-8888-888888888888', '66666666-6666-4666-8666-666666666666', 'Electricista domiciliario.', 6, 'Miraflores', 6.0, 'PENDING', NULL, 0.0, 0, 0, true, now(), now())
    ON CONFLICT (user_id) DO NOTHING;
    """))

    # 3. Especialidades Profesional - Usando subconsultas para obtener los IDs reales
    op.execute(sql.text("""
    INSERT INTO public.professional_specialties (id, professional_profile_id, specialty_id, level, years_experience, created_at)
    VALUES
        (gen_random_uuid(), '77777777-7777-4777-8777-777777777777', (SELECT id FROM specialties WHERE code = 'plomeria'), 'EXPERT', 8, now()),
        (gen_random_uuid(), '88888888-8888-4888-8888-888888888888', (SELECT id FROM specialties WHERE code = 'electricidad'), 'ADVANCED', 6, now())
    ON CONFLICT DO NOTHING;
    """))

    # 4. Zonas Profesional
    op.execute(sql.text("""
    INSERT INTO public.professional_zones (id, professional_profile_id, department, city, zone, created_at)
    VALUES
        (gen_random_uuid(), '77777777-7777-4777-8777-777777777777', 'La Paz', 'La Paz', 'Sopocachi', now()),
        (gen_random_uuid(), '77777777-7777-4777-8777-777777777777', 'La Paz', 'La Paz', 'San Pedro', now()),
        (gen_random_uuid(), '88888888-8888-4888-8888-888888888888', 'La Paz', 'La Paz', 'Miraflores', now())
    ON CONFLICT DO NOTHING;
    """))

    # 5. Direcciones Usuario
    op.execute(sql.text("""
    INSERT INTO public.user_addresses (id, user_id, department, city, zone, address, reference, latitude, longitude, is_primary, created_at, updated_at)
    VALUES
        ('ccccccc1-cccc-4ccc-8ccc-ccccccccccc1', '33333333-3333-4333-8333-333333333333', 'La Paz', 'La Paz', 'Obrajes', 'Av. Costanera #123', 'Frente a la plaza', -16.5335, -68.0873, TRUE, now(), now()),
        ('ccccccc2-cccc-4ccc-8ccc-ccccccccccc2', '44444444-4444-4444-8444-444444444444', 'La Paz', 'La Paz', 'Calacoto', 'Calle 21 #45', 'Cerca de la iglesia', -16.5398, -68.0779, TRUE, now(), now())
    ON CONFLICT (id) DO NOTHING;
    """))

    # 6. Solicitudes de Servicio - Usando subconsultas para los specialty_id
    # Nota: Los nombres correctos de las columnas de presupuesto son minimum_budget y maximum_budget
    op.execute(sql.text("""
    INSERT INTO public.service_requests (
        id, client_user_id, specialty_id, title, description, department, city, zone,
        address, reference, preferred_date, preferred_start_time, preferred_end_time,
        minimum_budget, maximum_budget, status, assigned_professional_profile_id,
        contact_channel, is_active, created_at, updated_at
    ) VALUES
        ('ddddddd1-dddd-4ddd-8ddd-ddddddddddd1', '33333333-3333-4333-8333-333333333333', (SELECT id FROM specialties WHERE code = 'plomeria'), 'Reparación de fuga', 'Existe fuga debajo del lavaplatos.', 'La Paz', 'La Paz', 'Obrajes', 'Av. Costanera', 'Edificio azul', CURRENT_DATE + 1, '09:00', '11:00', 80.0, 150.0, 'COMPLETED', '77777777-7777-4777-8777-777777777777', 'WHATSAPP', TRUE, now(), now()),
        ('ddddddd2-dddd-4ddd-8ddd-ddddddddddd2', '44444444-4444-4444-8444-444444444444', (SELECT id FROM specialties WHERE code = 'electricidad'), 'Lámparas LED', 'Instalar 4 lámparas LED.', 'La Paz', 'La Paz', 'Calacoto', 'Calle 21', 'Timbre 2B', CURRENT_DATE + 2, '15:00', '18:00', 120.0, 220.0, 'OPEN', NULL, 'PHONE', TRUE, now(), now())
    ON CONFLICT (id) DO NOTHING;
    """))

    # 7. Calificaciones
    op.execute(sql.text("""
    INSERT INTO public.service_ratings (id, service_request_id, client_user_id, professional_profile_id, score, comment, is_verified, created_at, updated_at)
    VALUES
        ('abababa1-abab-4aba-8aba-abababababa1', 'ddddddd1-dddd-4ddd-8ddd-ddddddddddd1', '33333333-3333-4333-8333-333333333333', '77777777-7777-4777-8777-777777777777', 5, 'Trabajo rápido y puntual.', TRUE, now(), now())
    ON CONFLICT (service_request_id) DO NOTHING;
    """))


def downgrade() -> None:
    op.execute(sql.text("DELETE FROM public.service_ratings;"))
    op.execute(sql.text("DELETE FROM public.service_requests;"))
    op.execute(sql.text("DELETE FROM public.user_addresses;"))
    op.execute(sql.text("DELETE FROM public.professional_zones;"))
    op.execute(sql.text("DELETE FROM public.professional_specialties;"))
    op.execute(sql.text("DELETE FROM public.professional_profiles;"))
    op.execute(sql.text("DELETE FROM public.users WHERE email LIKE '%@siswork.local';"))