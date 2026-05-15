--
-- PostgreSQL database dump
--

\restrict O3CQbRmiYm4ajDVRXkbPlsxjy9UTVXIZzu5h9mwUP7PeKsflnx5pnsJP4HsEQCV

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: accion_auditoria_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.accion_auditoria_enum AS ENUM (
    'login',
    'logout',
    'registro',
    'editar_perfil',
    'crear_solicitud',
    'editar_solicitud',
    'eliminar_solicitud',
    'postular_solicitud',
    'aceptar_postulacion',
    'rechazar_postulacion',
    'calificar_servicio',
    'subir_certificacion',
    'validar_profesional',
    'rechazar_profesional',
    'suspender_usuario',
    'activar_usuario'
);


ALTER TYPE public.accion_auditoria_enum OWNER TO ruper;

--
-- Name: application_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.application_status_enum AS ENUM (
    'PENDING',
    'ACCEPTED',
    'REJECTED',
    'CANCELLED'
);


ALTER TYPE public.application_status_enum OWNER TO ruper;

--
-- Name: audit_action_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.audit_action_enum AS ENUM (
    'LOGIN',
    'LOGOUT',
    'REGISTER',
    'EDIT_PROFILE',
    'CREATE_REQUEST',
    'EDIT_REQUEST',
    'DELETE_REQUEST',
    'APPLY_TO_REQUEST',
    'ACCEPT_APPLICATION',
    'REJECT_APPLICATION',
    'RATE_SERVICE',
    'UPLOAD_CERTIFICATION',
    'VALIDATE_PROFESSIONAL',
    'REJECT_PROFESSIONAL',
    'SUSPEND_USER',
    'ACTIVATE_USER'
);


ALTER TYPE public.audit_action_enum OWNER TO ruper;

--
-- Name: canal_contacto_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.canal_contacto_enum AS ENUM (
    'whatsapp',
    'telefono',
    'chat_interno',
    'otro'
);


ALTER TYPE public.canal_contacto_enum OWNER TO ruper;

--
-- Name: contact_channel_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.contact_channel_enum AS ENUM (
    'WHATSAPP',
    'PHONE',
    'INTERNAL_CHAT',
    'OTHER'
);


ALTER TYPE public.contact_channel_enum OWNER TO ruper;

--
-- Name: dia_semana_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.dia_semana_enum AS ENUM (
    'lunes',
    'martes',
    'miercoles',
    'jueves',
    'viernes',
    'sabado',
    'domingo'
);


ALTER TYPE public.dia_semana_enum OWNER TO ruper;

--
-- Name: document_type_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.document_type_enum AS ENUM (
    'CI',
    'CERTIFICATE',
    'LICENSE',
    'BACKGROUND_CHECK',
    'OTHER'
);


ALTER TYPE public.document_type_enum OWNER TO ruper;

--
-- Name: estado_postulacion_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.estado_postulacion_enum AS ENUM (
    'pendiente',
    'aceptada',
    'rechazada',
    'cancelada'
);


ALTER TYPE public.estado_postulacion_enum OWNER TO ruper;

--
-- Name: estado_solicitud_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.estado_solicitud_enum AS ENUM (
    'abierta',
    'en_proceso',
    'asignada',
    'completada',
    'cancelada'
);


ALTER TYPE public.estado_solicitud_enum OWNER TO ruper;

--
-- Name: estado_usuario_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.estado_usuario_enum AS ENUM (
    'activo',
    'suspendido',
    'eliminado',
    'bloqueado'
);


ALTER TYPE public.estado_usuario_enum OWNER TO ruper;

--
-- Name: estado_verificacion_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.estado_verificacion_enum AS ENUM (
    'pendiente',
    'en_revision',
    'aprobado',
    'rechazado'
);


ALTER TYPE public.estado_verificacion_enum OWNER TO ruper;

--
-- Name: nivel_especialidad_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.nivel_especialidad_enum AS ENUM (
    'basico',
    'intermedio',
    'avanzado',
    'experto'
);


ALTER TYPE public.nivel_especialidad_enum OWNER TO ruper;

--
-- Name: report_type_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.report_type_enum AS ENUM (
    'USERS',
    'PROFESSIONALS',
    'REQUESTS',
    'RATINGS',
    'SPECIALTIES',
    'VALIDATIONS',
    'DASHBOARD'
);


ALTER TYPE public.report_type_enum OWNER TO ruper;

--
-- Name: rol_usuario_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.rol_usuario_enum AS ENUM (
    'cliente',
    'profesional',
    'administrador',
    'soporte'
);


ALTER TYPE public.rol_usuario_enum OWNER TO ruper;

--
-- Name: service_request_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.service_request_status_enum AS ENUM (
    'OPEN',
    'IN_PROGRESS',
    'ASSIGNED',
    'COMPLETED',
    'CANCELLED'
);


ALTER TYPE public.service_request_status_enum OWNER TO ruper;

--
-- Name: sexo_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.sexo_enum AS ENUM (
    'masculino',
    'femenino',
    'otro',
    'prefiero_no_decir'
);


ALTER TYPE public.sexo_enum OWNER TO ruper;

--
-- Name: specialty_level_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.specialty_level_enum AS ENUM (
    'BASIC',
    'INTERMEDIATE',
    'ADVANCED',
    'EXPERT'
);


ALTER TYPE public.specialty_level_enum OWNER TO ruper;

--
-- Name: tipo_documento_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.tipo_documento_enum AS ENUM (
    'ci',
    'certificado',
    'licencia',
    'antecedente',
    'otro'
);


ALTER TYPE public.tipo_documento_enum OWNER TO ruper;

--
-- Name: tipo_reporte_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.tipo_reporte_enum AS ENUM (
    'usuarios',
    'profesionales',
    'solicitudes',
    'calificaciones',
    'especialidades',
    'validaciones',
    'dashboard'
);


ALTER TYPE public.tipo_reporte_enum OWNER TO ruper;

--
-- Name: user_gender_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.user_gender_enum AS ENUM (
    'MALE',
    'FEMALE',
    'OTHER',
    'PREFER_NOT_TO_SAY'
);


ALTER TYPE public.user_gender_enum OWNER TO ruper;

--
-- Name: user_role_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.user_role_enum AS ENUM (
    'CLIENT',
    'PROFESSIONAL',
    'ADMIN',
    'SUPPORT'
);


ALTER TYPE public.user_role_enum OWNER TO ruper;

--
-- Name: user_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.user_status_enum AS ENUM (
    'ACTIVE',
    'SUSPENDED',
    'BLOCKED',
    'DELETED'
);


ALTER TYPE public.user_status_enum OWNER TO ruper;

--
-- Name: verification_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.verification_status_enum AS ENUM (
    'PENDING',
    'IN_REVIEW',
    'APPROVED',
    'REJECTED'
);


ALTER TYPE public.verification_status_enum OWNER TO ruper;

--
-- Name: weekday_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.weekday_enum AS ENUM (
    'MONDAY',
    'TUESDAY',
    'WEDNESDAY',
    'THURSDAY',
    'FRIDAY',
    'SATURDAY',
    'SUNDAY'
);


ALTER TYPE public.weekday_enum OWNER TO ruper;

--
-- Name: recalculate_completed_services(uuid); Type: FUNCTION; Schema: public; Owner: ruper
--

CREATE FUNCTION public.recalculate_completed_services(profile_id_param uuid) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
    $$;


ALTER FUNCTION public.recalculate_completed_services(profile_id_param uuid) OWNER TO ruper;

--
-- Name: recalculate_professional_rating(uuid); Type: FUNCTION; Schema: public; Owner: ruper
--

CREATE FUNCTION public.recalculate_professional_rating(profile_id_param uuid) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
    $$;


ALTER FUNCTION public.recalculate_professional_rating(profile_id_param uuid) OWNER TO ruper;

--
-- Name: trg_recalculate_completed_services(); Type: FUNCTION; Schema: public; Owner: ruper
--

CREATE FUNCTION public.trg_recalculate_completed_services() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
    $$;


ALTER FUNCTION public.trg_recalculate_completed_services() OWNER TO ruper;

--
-- Name: trg_recalculate_professional_rating(); Type: FUNCTION; Schema: public; Owner: ruper
--

CREATE FUNCTION public.trg_recalculate_professional_rating() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
    $$;


ALTER FUNCTION public.trg_recalculate_professional_rating() OWNER TO ruper;

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: ruper
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO ruper;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: professional_validation_queue; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_validation_queue (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    requested_by_user_id uuid NOT NULL,
    assigned_support_user_id uuid,
    status public.verification_status_enum DEFAULT 'PENDING'::public.verification_status_enum NOT NULL,
    submitted_at timestamp with time zone DEFAULT now() NOT NULL,
    review_started_at timestamp with time zone,
    resolved_at timestamp with time zone,
    rejection_reason text,
    waiting_time_minutes integer,
    review_time_minutes integer,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_prof_validation_queue_review_time_non_negative CHECK (((review_time_minutes IS NULL) OR (review_time_minutes >= 0))),
    CONSTRAINT ck_prof_validation_queue_waiting_time_non_negative CHECK (((waiting_time_minutes IS NULL) OR (waiting_time_minutes >= 0)))
);


ALTER TABLE public.professional_validation_queue OWNER TO ruper;

--
-- Name: service_ratings; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.service_ratings (
    id uuid NOT NULL,
    service_request_id uuid NOT NULL,
    client_user_id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    score integer NOT NULL,
    comment text,
    is_verified boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_service_ratings_score_range CHECK (((score >= 1) AND (score <= 5)))
);


ALTER TABLE public.service_ratings OWNER TO ruper;

--
-- Name: service_requests; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.service_requests (
    id uuid NOT NULL,
    client_user_id uuid NOT NULL,
    specialty_id uuid NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    department character varying(100) DEFAULT 'La Paz'::character varying NOT NULL,
    city character varying(100) DEFAULT 'La Paz'::character varying NOT NULL,
    zone character varying(100) NOT NULL,
    address character varying(255),
    reference text,
    preferred_date date,
    preferred_start_time time without time zone,
    preferred_end_time time without time zone,
    minimum_budget numeric(10,2),
    maximum_budget numeric(10,2),
    status public.service_request_status_enum DEFAULT 'OPEN'::public.service_request_status_enum NOT NULL,
    assigned_professional_profile_id uuid,
    contact_channel public.contact_channel_enum DEFAULT 'WHATSAPP'::public.contact_channel_enum NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    closed_at timestamp with time zone,
    CONSTRAINT ck_service_requests_budget_range CHECK ((((minimum_budget IS NULL) AND (maximum_budget IS NULL)) OR ((minimum_budget IS NOT NULL) AND (maximum_budget IS NOT NULL) AND (minimum_budget >= (0)::numeric) AND (maximum_budget >= minimum_budget)))),
    CONSTRAINT ck_service_requests_preferred_time_range CHECK ((((preferred_start_time IS NULL) AND (preferred_end_time IS NULL)) OR ((preferred_start_time IS NOT NULL) AND (preferred_end_time IS NOT NULL) AND (preferred_start_time < preferred_end_time))))
);


ALTER TABLE public.service_requests OWNER TO ruper;

--
-- Name: users; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role public.user_role_enum NOT NULL,
    status public.user_status_enum NOT NULL,
    email_verified_at timestamp with time zone,
    last_login_at timestamp with time zone,
    failed_login_attempts integer NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    phone character varying(20),
    whatsapp_number character varying(20),
    profile_photo_url text,
    birth_date date,
    gender public.user_gender_enum,
    password_reset_token character varying(255),
    password_reset_expires_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO ruper;

--
-- Name: admin_dashboard_summary_view; Type: VIEW; Schema: public; Owner: ruper
--

CREATE VIEW public.admin_dashboard_summary_view AS
 SELECT ( SELECT count(*) AS count
           FROM public.users
          WHERE (users.deleted_at IS NULL)) AS total_users,
    ( SELECT count(*) AS count
           FROM public.users
          WHERE ((users.role = 'CLIENT'::public.user_role_enum) AND (users.deleted_at IS NULL))) AS total_clients,
    ( SELECT count(*) AS count
           FROM public.users
          WHERE ((users.role = 'PROFESSIONAL'::public.user_role_enum) AND (users.deleted_at IS NULL))) AS total_professionals,
    ( SELECT count(*) AS count
           FROM public.service_requests) AS total_service_requests,
    ( SELECT count(*) AS count
           FROM public.service_requests
          WHERE (service_requests.status = 'OPEN'::public.service_request_status_enum)) AS open_service_requests,
    ( SELECT count(*) AS count
           FROM public.service_requests
          WHERE (service_requests.status = 'COMPLETED'::public.service_request_status_enum)) AS completed_service_requests,
    ( SELECT count(*) AS count
           FROM public.professional_validation_queue
          WHERE (professional_validation_queue.status = ANY (ARRAY['PENDING'::public.verification_status_enum, 'IN_REVIEW'::public.verification_status_enum]))) AS pending_validations,
    ( SELECT round(avg(service_ratings.score), 2) AS round
           FROM public.service_ratings) AS platform_average_rating;


ALTER VIEW public.admin_dashboard_summary_view OWNER TO ruper;

--
-- Name: administrative_notes; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.administrative_notes (
    id uuid NOT NULL,
    author_user_id uuid NOT NULL,
    related_entity character varying(100) NOT NULL,
    related_entity_id uuid NOT NULL,
    note text NOT NULL,
    is_private boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.administrative_notes OWNER TO ruper;

--
-- Name: administrative_reports; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.administrative_reports (
    id uuid NOT NULL,
    generated_by_user_id uuid NOT NULL,
    report_type public.report_type_enum NOT NULL,
    parameters_json jsonb,
    generated_at timestamp with time zone DEFAULT now() NOT NULL,
    file_url text
);


ALTER TABLE public.administrative_reports OWNER TO ruper;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ruper;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.audit_logs (
    id uuid NOT NULL,
    actor_user_id uuid,
    action public.audit_action_enum NOT NULL,
    entity character varying(100) NOT NULL,
    entity_id uuid,
    previous_values jsonb,
    new_values jsonb,
    ip_address inet,
    user_agent text,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.audit_logs OWNER TO ruper;

--
-- Name: certifications; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.certifications (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    document_type public.document_type_enum DEFAULT 'CERTIFICATE'::public.document_type_enum NOT NULL,
    title character varying(200) NOT NULL,
    institution character varying(150),
    issue_year integer,
    file_url text NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    verified_by_user_id uuid,
    verified_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_certifications_issue_year_valid CHECK (((issue_year IS NULL) OR ((issue_year >= 1950) AND ((issue_year)::numeric <= (EXTRACT(year FROM CURRENT_DATE) + (1)::numeric)))))
);


ALTER TABLE public.certifications OWNER TO ruper;

--
-- Name: professional_availabilities; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_availabilities (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    weekday public.weekday_enum NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    is_available boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_professional_availabilities_time_range CHECK ((start_time < end_time))
);


ALTER TABLE public.professional_availabilities OWNER TO ruper;

--
-- Name: professional_profiles; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_profiles (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    bio text,
    years_experience integer DEFAULT 0 NOT NULL,
    main_zone character varying(100) NOT NULL,
    service_radius_km numeric(5,2) DEFAULT 5.00 NOT NULL,
    work_reference text,
    identity_document_url text,
    verification_status public.verification_status_enum DEFAULT 'PENDING'::public.verification_status_enum NOT NULL,
    verification_requested_at timestamp with time zone,
    verification_resolved_at timestamp with time zone,
    verified_by_user_id uuid,
    average_rating numeric(3,2) DEFAULT 0.00 NOT NULL,
    ratings_count integer DEFAULT 0 NOT NULL,
    completed_services_count integer DEFAULT 0 NOT NULL,
    available_now boolean DEFAULT false NOT NULL,
    public_contact_enabled boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_professional_profiles_average_rating_range CHECK (((average_rating >= (0)::numeric) AND (average_rating <= (5)::numeric))),
    CONSTRAINT ck_professional_profiles_years_experience_non_negative CHECK ((years_experience >= 0))
);


ALTER TABLE public.professional_profiles OWNER TO ruper;

--
-- Name: professional_specialties; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_specialties (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    specialty_id uuid NOT NULL,
    level public.specialty_level_enum DEFAULT 'BASIC'::public.specialty_level_enum NOT NULL,
    years_experience integer DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_professional_specialties_years_experience_non_negative CHECK ((years_experience >= 0))
);


ALTER TABLE public.professional_specialties OWNER TO ruper;

--
-- Name: professional_zones; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_zones (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    department character varying(100) DEFAULT 'La Paz'::character varying NOT NULL,
    city character varying(100) DEFAULT 'La Paz'::character varying NOT NULL,
    zone character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.professional_zones OWNER TO ruper;

--
-- Name: specialties; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.specialties (
    id uuid NOT NULL,
    code character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.specialties OWNER TO ruper;

--
-- Name: public_professional_profiles_view; Type: VIEW; Schema: public; Owner: ruper
--

CREATE VIEW public.public_professional_profiles_view AS
 SELECT pp.id AS professional_profile_id,
    u.id AS user_id,
    u.first_name,
    u.last_name,
    concat(u.first_name, ' ', u.last_name) AS full_name,
    pp.bio,
    pp.years_experience,
    pp.main_zone,
    pp.average_rating,
    pp.ratings_count,
    pp.completed_services_count,
    pp.available_now,
    u.phone,
    u.whatsapp_number,
    ( SELECT string_agg((s.name)::text, ', '::text ORDER BY (s.name)::text) AS string_agg
           FROM (public.professional_specialties ps
             JOIN public.specialties s ON ((s.id = ps.specialty_id)))
          WHERE (ps.professional_profile_id = pp.id)) AS specialties,
    pp.verification_status
   FROM (public.professional_profiles pp
     JOIN public.users u ON ((u.id = pp.user_id)))
  WHERE ((u.status = 'ACTIVE'::public.user_status_enum) AND (pp.verification_status = 'APPROVED'::public.verification_status_enum) AND (pp.public_contact_enabled = true));


ALTER VIEW public.public_professional_profiles_view OWNER TO ruper;

--
-- Name: saved_professionals; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.saved_professionals (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.saved_professionals OWNER TO ruper;

--
-- Name: search_history; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.search_history (
    id uuid NOT NULL,
    user_id uuid,
    search_term character varying(255),
    specialty_id uuid,
    zone character varying(100),
    minimum_rating numeric(2,1),
    available_now boolean,
    results_count integer DEFAULT 0 NOT NULL,
    searched_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_search_history_minimum_rating_range CHECK (((minimum_rating IS NULL) OR ((minimum_rating >= (0)::numeric) AND (minimum_rating <= (5)::numeric))))
);


ALTER TABLE public.search_history OWNER TO ruper;

--
-- Name: service_applications; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.service_applications (
    id uuid NOT NULL,
    service_request_id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    proposal_message text,
    estimated_price numeric(10,2),
    status public.application_status_enum DEFAULT 'PENDING'::public.application_status_enum NOT NULL,
    applied_at timestamp with time zone DEFAULT now() NOT NULL,
    responded_at timestamp with time zone,
    cancelled_at timestamp with time zone,
    CONSTRAINT ck_service_applications_estimated_price_non_negative CHECK (((estimated_price IS NULL) OR (estimated_price >= (0)::numeric)))
);


ALTER TABLE public.service_applications OWNER TO ruper;

--
-- Name: service_contacts; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.service_contacts (
    id uuid NOT NULL,
    service_request_id uuid,
    client_user_id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    channel public.contact_channel_enum DEFAULT 'WHATSAPP'::public.contact_channel_enum NOT NULL,
    contacted_at timestamp with time zone DEFAULT now() NOT NULL,
    note text
);


ALTER TABLE public.service_contacts OWNER TO ruper;

--
-- Name: user_addresses; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.user_addresses (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    department character varying(100) DEFAULT 'La Paz'::character varying NOT NULL,
    city character varying(100) DEFAULT 'La Paz'::character varying NOT NULL,
    zone character varying(100) NOT NULL,
    address character varying(255),
    reference text,
    latitude numeric(10,7),
    longitude numeric(10,7),
    is_primary boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.user_addresses OWNER TO ruper;

--
-- Name: user_two_factor; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.user_two_factor (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    is_enabled boolean NOT NULL,
    secret character varying(255),
    backup_codes character varying,
    confirmed_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.user_two_factor OWNER TO ruper;

--
-- Data for Name: administrative_notes; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.administrative_notes (id, author_user_id, related_entity, related_entity_id, note, is_private, created_at) FROM stdin;
\.


--
-- Data for Name: administrative_reports; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.administrative_reports (id, generated_by_user_id, report_type, parameters_json, generated_at, file_url) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.alembic_version (version_num) FROM stdin;
8bc478457236
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.audit_logs (id, actor_user_id, action, entity, entity_id, previous_values, new_values, ip_address, user_agent, created_at) FROM stdin;
\.


--
-- Data for Name: certifications; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.certifications (id, professional_profile_id, document_type, title, institution, issue_year, file_url, is_verified, verified_by_user_id, verified_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: professional_availabilities; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_availabilities (id, professional_profile_id, weekday, start_time, end_time, is_available, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: professional_profiles; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_profiles (id, user_id, bio, years_experience, main_zone, service_radius_km, work_reference, identity_document_url, verification_status, verification_requested_at, verification_resolved_at, verified_by_user_id, average_rating, ratings_count, completed_services_count, available_now, public_contact_enabled, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: professional_specialties; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_specialties (id, professional_profile_id, specialty_id, level, years_experience, created_at) FROM stdin;
\.


--
-- Data for Name: professional_validation_queue; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_validation_queue (id, professional_profile_id, requested_by_user_id, assigned_support_user_id, status, submitted_at, review_started_at, resolved_at, rejection_reason, waiting_time_minutes, review_time_minutes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: professional_zones; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_zones (id, professional_profile_id, department, city, zone, created_at) FROM stdin;
\.


--
-- Data for Name: saved_professionals; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.saved_professionals (id, user_id, professional_profile_id, created_at) FROM stdin;
\.


--
-- Data for Name: search_history; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.search_history (id, user_id, search_term, specialty_id, zone, minimum_rating, available_now, results_count, searched_at) FROM stdin;
\.


--
-- Data for Name: service_applications; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.service_applications (id, service_request_id, professional_profile_id, proposal_message, estimated_price, status, applied_at, responded_at, cancelled_at) FROM stdin;
\.


--
-- Data for Name: service_contacts; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.service_contacts (id, service_request_id, client_user_id, professional_profile_id, channel, contacted_at, note) FROM stdin;
\.


--
-- Data for Name: service_ratings; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.service_ratings (id, service_request_id, client_user_id, professional_profile_id, score, comment, is_verified, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: service_requests; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.service_requests (id, client_user_id, specialty_id, title, description, department, city, zone, address, reference, preferred_date, preferred_start_time, preferred_end_time, minimum_budget, maximum_budget, status, assigned_professional_profile_id, contact_channel, is_active, created_at, updated_at, closed_at) FROM stdin;
\.


--
-- Data for Name: specialties; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.specialties (id, code, name, description, is_active, created_at) FROM stdin;
fcb9b58d-f534-4c2a-94ff-571f8bce5d89	plomeria	Plomería	Servicios de plomería y gasfitería	t	2026-04-17 16:04:58.891489-04
b04795d9-9629-41c6-86e6-b1428f91bb02	electricidad	Electricidad	Instalaciones y reparaciones eléctricas	t	2026-04-17 16:04:58.891489-04
728067a4-f1b7-4df6-bd47-aa69b9342a10	carpinteria	Carpintería	Trabajos en madera	t	2026-04-17 16:04:58.891489-04
7817153a-e1dd-4604-b0e3-9b7cab23f905	albanileria	Albañilería	Obra gruesa y refacciones	t	2026-04-17 16:04:58.891489-04
e92c4bd0-e79b-4d49-beff-723c06ede4b6	mecanicaautomotriz	Mecánica automotriz	Diagnóstico y reparación automotriz	t	2026-04-17 16:04:58.891489-04
5cccadc9-42e3-4a93-b610-4b4f60723330	reparacionelectrodomesticos	Reparación de electrodomésticos	Servicio técnico de electrodomésticos	t	2026-04-17 16:04:58.891489-04
867ff2ad-f28d-4f23-ab0d-02507be5e882	pintura	Pintura	Pintado de interiores y exteriores	t	2026-04-17 16:04:58.891489-04
df3529df-2c23-477e-8404-0792f7d45744	limpieza	Limpieza	Servicios de limpieza	t	2026-04-17 16:04:58.891489-04
412ba633-23fd-4e80-985e-61c622c6cb52	jardineria	Jardinería	Mantenimiento de jardines	t	2026-04-17 16:04:58.891489-04
\.


--
-- Data for Name: user_addresses; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.user_addresses (id, user_id, department, city, zone, address, reference, latitude, longitude, is_primary, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_two_factor; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.user_two_factor (id, user_id, is_enabled, secret, backup_codes, confirmed_at, created_at, updated_at) FROM stdin;
ebf98c3d-0935-4c86-a08f-de3e23b892e7	4eaa0163-084b-493e-845e-d8f652000706	t	ANXEHORVC257URYSN3SVCSVCKW4S3UVM	["$argon2id$v=19$m=65536,t=3,p=4$EbhdlylGkwA2a8mn5yxyPw$n/2JdYp258L9f86xqIL2CJoVOuI50UZ46fZi7uN9dBw", "$argon2id$v=19$m=65536,t=3,p=4$MexzyshN7yw1lSVDG0jVxg$aWFKlfqmyPqZgpuBeee0Ibo0iKW4Smqq2K7H9ZF7FfM", "$argon2id$v=19$m=65536,t=3,p=4$8BjryXPk1ZkyJd86aaN3eA$ZxsMzij0O/5zBqn7dTYTJx8tozh0YB1ea66ZAT6knE0", "$argon2id$v=19$m=65536,t=3,p=4$a9SfAOvKgPGkhgeU5F6UqQ$xXm7sf7mIXDqgDN3FxLVsw9ZJ+dj2/dDheVbSqWEJAs", "$argon2id$v=19$m=65536,t=3,p=4$ZkQPDBCqKG6pOMaJZneVFg$W1dx2j8S4jk2T+0V7jWLT9CM9jkITrkGeGmYIo4vDiY", "$argon2id$v=19$m=65536,t=3,p=4$Ca+xItKJpW7IFwQR1pfKkg$tr7lhgoowuE3rsg0XMMEGBtad6I4E+1AkMgTUj3t4gs", "$argon2id$v=19$m=65536,t=3,p=4$aryvnUj1dR1x8G/VsUxymw$oxOkj5nBat1Dtzk85JTIRfJG+I/xD/2CtU/pPNuYnTw", "$argon2id$v=19$m=65536,t=3,p=4$rF1j+h6TgSA3PYcO9J+K9Q$L2QsrVjshxNgeWd0JLbgY4e7tvVBtF8spG2kAnH6+BU"]	2026-04-24 16:59:46.170213-04	2026-04-24 16:03:11.163729-04	2026-04-24 16:59:46.16605-04
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.users (id, first_name, last_name, email, password_hash, role, status, email_verified_at, last_login_at, failed_login_attempts, is_active, created_at, updated_at, phone, whatsapp_number, profile_photo_url, birth_date, gender, password_reset_token, password_reset_expires_at, deleted_at) FROM stdin;
830e7f61-fa94-47b0-9c3c-78834c941346	ruper	932	limberromero931@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$5xRGIQi1Z7FvQ2LbyEDwNg$Rz6Qo2+vcKLZ4sN57NTG4U61wfPvVXV3blJw9+SZfiQ	CLIENT	ACTIVE	\N	2026-04-24 15:57:03.666607-04	0	t	2026-04-24 15:56:44.316699-04	2026-04-24 15:57:03.54761-04	\N	\N	\N	\N	\N	\N	\N	\N
4fee4eae-6af6-4af1-9d47-0c5cb7e456d4	Admin	Siswork	admin@unifranz.com	$argon2id$v=19$m=65536,t=3,p=4$F16lEjqFLD4W1hZ7uxInaw$gaoNYa8T/n48dx4zvj3DUJNdsalZ6IGL0EnUV/z4378	CLIENT	ACTIVE	\N	2026-04-17 08:27:00.945053-04	0	t	2026-04-17 08:26:49.484779-04	2026-04-24 18:07:33.984544-04	\N	\N	\N	\N	\N	\N	\N	\N
629c5f40-c0c2-4e77-8602-172e5bbfcaf8	Limber2	Romero3	limber2@unifranz.com	$argon2id$v=19$m=65536,t=3,p=4$y/tgE/8eOYjDwyxJ0JEc3Q$+NqmiHCkkZypZOklaAEhgme1nzG/X5i2lNMXW1hC2YY	CLIENT	ACTIVE	\N	\N	0	t	2026-04-17 17:43:49.23102-04	2026-04-24 18:07:33.991679-04	\N	\N	\N	\N	\N	\N	\N	\N
056e94e7-2a7b-4ac9-8e3f-313c213c782b	Soporte	SISWORK	soporte@siswork.com	$argon2id$v=19$m=65536,t=3,p=4$5xRGIQi1Z7FvQ2LbyEDwNg$Rz6Qo2+vcKLZ4sN57NTG4U61wfPvVXV3blJw9+SZfiQ	SUPPORT	ACTIVE	2026-04-17 16:20:48.99046-04	\N	0	t	2026-04-17 16:20:48.99046-04	2026-04-24 18:07:33.993648-04	71111111	71111111	\N	\N	\N	\N	\N	\N
4d2944ba-84d6-4ea1-8287-2441d2538ab4	Limber	Romero	limber@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$cI42TJjl0mhfLMftSMdb9w$YSijb1UwqdfqgHdw3CXWxosmsBpSGv+qdP+keI22yxw	CLIENT	DELETED	\N	2026-04-24 15:58:02.116495-04	0	f	2026-04-17 17:43:09.852536-04	2026-04-24 18:37:10.928156-04	\N	\N	\N	\N	\N	\N	\N	2026-04-24 18:37:10.931008-04
4eaa0163-084b-493e-845e-d8f652000706	Admin	SISWORK	admin.siswork@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$5xRGIQi1Z7FvQ2LbyEDwNg$Rz6Qo2+vcKLZ4sN57NTG4U61wfPvVXV3blJw9+SZfiQ	ADMIN	ACTIVE	2026-04-17 16:20:48.99046-04	2026-05-08 16:05:34.067716-04	0	t	2026-04-17 16:20:48.99046-04	2026-05-08 16:05:34.065207-04	70000000	70000000	\N	\N	\N	\N	\N	\N
\.


--
-- Name: administrative_notes administrative_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.administrative_notes
    ADD CONSTRAINT administrative_notes_pkey PRIMARY KEY (id);


--
-- Name: administrative_reports administrative_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.administrative_reports
    ADD CONSTRAINT administrative_reports_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: certifications certifications_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.certifications
    ADD CONSTRAINT certifications_pkey PRIMARY KEY (id);


--
-- Name: professional_availabilities professional_availabilities_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_availabilities
    ADD CONSTRAINT professional_availabilities_pkey PRIMARY KEY (id);


--
-- Name: professional_profiles professional_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_profiles
    ADD CONSTRAINT professional_profiles_pkey PRIMARY KEY (id);


--
-- Name: professional_specialties professional_specialties_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT professional_specialties_pkey PRIMARY KEY (id);


--
-- Name: professional_validation_queue professional_validation_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_validation_queue
    ADD CONSTRAINT professional_validation_queue_pkey PRIMARY KEY (id);


--
-- Name: professional_zones professional_zones_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_zones
    ADD CONSTRAINT professional_zones_pkey PRIMARY KEY (id);


--
-- Name: saved_professionals saved_professionals_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.saved_professionals
    ADD CONSTRAINT saved_professionals_pkey PRIMARY KEY (id);


--
-- Name: search_history search_history_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.search_history
    ADD CONSTRAINT search_history_pkey PRIMARY KEY (id);


--
-- Name: service_applications service_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_applications
    ADD CONSTRAINT service_applications_pkey PRIMARY KEY (id);


--
-- Name: service_contacts service_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_contacts
    ADD CONSTRAINT service_contacts_pkey PRIMARY KEY (id);


--
-- Name: service_ratings service_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_ratings
    ADD CONSTRAINT service_ratings_pkey PRIMARY KEY (id);


--
-- Name: service_requests service_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_requests
    ADD CONSTRAINT service_requests_pkey PRIMARY KEY (id);


--
-- Name: specialties specialties_code_key; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT specialties_code_key UNIQUE (code);


--
-- Name: specialties specialties_name_key; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT specialties_name_key UNIQUE (name);


--
-- Name: specialties specialties_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT specialties_pkey PRIMARY KEY (id);


--
-- Name: professional_validation_queue uq_prof_validation_queue_profile_id; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_validation_queue
    ADD CONSTRAINT uq_prof_validation_queue_profile_id UNIQUE (professional_profile_id);


--
-- Name: professional_availabilities uq_professional_availabilities_profile_weekday_start_end; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_availabilities
    ADD CONSTRAINT uq_professional_availabilities_profile_weekday_start_end UNIQUE (professional_profile_id, weekday, start_time, end_time);


--
-- Name: professional_profiles uq_professional_profiles_user_id; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_profiles
    ADD CONSTRAINT uq_professional_profiles_user_id UNIQUE (user_id);


--
-- Name: professional_specialties uq_professional_specialty_profile_specialty; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT uq_professional_specialty_profile_specialty UNIQUE (professional_profile_id, specialty_id);


--
-- Name: professional_zones uq_professional_zones_profile_department_city_zone; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_zones
    ADD CONSTRAINT uq_professional_zones_profile_department_city_zone UNIQUE (professional_profile_id, department, city, zone);


--
-- Name: saved_professionals uq_saved_professionals_user_profile; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.saved_professionals
    ADD CONSTRAINT uq_saved_professionals_user_profile UNIQUE (user_id, professional_profile_id);


--
-- Name: service_applications uq_service_applications_request_professional; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_applications
    ADD CONSTRAINT uq_service_applications_request_professional UNIQUE (service_request_id, professional_profile_id);


--
-- Name: service_ratings uq_service_ratings_service_request_id; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_ratings
    ADD CONSTRAINT uq_service_ratings_service_request_id UNIQUE (service_request_id);


--
-- Name: user_addresses user_addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_addresses
    ADD CONSTRAINT user_addresses_pkey PRIMARY KEY (id);


--
-- Name: user_two_factor user_two_factor_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_two_factor
    ADD CONSTRAINT user_two_factor_pkey PRIMARY KEY (id);


--
-- Name: user_two_factor user_two_factor_user_id_key; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_two_factor
    ADD CONSTRAINT user_two_factor_user_id_key UNIQUE (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_administrative_reports_generated_by_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_administrative_reports_generated_by_user_id ON public.administrative_reports USING btree (generated_by_user_id);


--
-- Name: ix_administrative_reports_report_type; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_administrative_reports_report_type ON public.administrative_reports USING btree (report_type);


--
-- Name: ix_audit_logs_action; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_audit_logs_action ON public.audit_logs USING btree (action);


--
-- Name: ix_audit_logs_actor_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_audit_logs_actor_user_id ON public.audit_logs USING btree (actor_user_id);


--
-- Name: ix_audit_logs_created_at; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_audit_logs_created_at ON public.audit_logs USING btree (created_at);


--
-- Name: ix_audit_logs_entity_entity_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_audit_logs_entity_entity_id ON public.audit_logs USING btree (entity, entity_id);


--
-- Name: ix_certifications_is_verified; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_certifications_is_verified ON public.certifications USING btree (is_verified);


--
-- Name: ix_certifications_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_certifications_profile_id ON public.certifications USING btree (professional_profile_id);


--
-- Name: ix_prof_validation_queue_assigned_support_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_prof_validation_queue_assigned_support_user_id ON public.professional_validation_queue USING btree (assigned_support_user_id);


--
-- Name: ix_prof_validation_queue_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_prof_validation_queue_status ON public.professional_validation_queue USING btree (status);


--
-- Name: ix_prof_validation_queue_submitted_at; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_prof_validation_queue_submitted_at ON public.professional_validation_queue USING btree (submitted_at);


--
-- Name: ix_professional_availabilities_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_availabilities_profile_id ON public.professional_availabilities USING btree (professional_profile_id);


--
-- Name: ix_professional_availabilities_weekday; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_availabilities_weekday ON public.professional_availabilities USING btree (weekday);


--
-- Name: ix_professional_profiles_available_now; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_profiles_available_now ON public.professional_profiles USING btree (available_now);


--
-- Name: ix_professional_profiles_average_rating; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_profiles_average_rating ON public.professional_profiles USING btree (average_rating);


--
-- Name: ix_professional_profiles_main_zone; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_profiles_main_zone ON public.professional_profiles USING btree (main_zone);


--
-- Name: ix_professional_profiles_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_profiles_user_id ON public.professional_profiles USING btree (user_id);


--
-- Name: ix_professional_profiles_verification_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_profiles_verification_status ON public.professional_profiles USING btree (verification_status);


--
-- Name: ix_professional_specialties_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_specialties_profile_id ON public.professional_specialties USING btree (professional_profile_id);


--
-- Name: ix_professional_specialties_specialty_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_specialties_specialty_id ON public.professional_specialties USING btree (specialty_id);


--
-- Name: ix_professional_zones_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_zones_profile_id ON public.professional_zones USING btree (professional_profile_id);


--
-- Name: ix_professional_zones_zone; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_zones_zone ON public.professional_zones USING btree (zone);


--
-- Name: ix_saved_professionals_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_saved_professionals_professional_profile_id ON public.saved_professionals USING btree (professional_profile_id);


--
-- Name: ix_saved_professionals_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_saved_professionals_user_id ON public.saved_professionals USING btree (user_id);


--
-- Name: ix_search_history_searched_at; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_search_history_searched_at ON public.search_history USING btree (searched_at);


--
-- Name: ix_search_history_specialty_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_search_history_specialty_id ON public.search_history USING btree (specialty_id);


--
-- Name: ix_search_history_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_search_history_user_id ON public.search_history USING btree (user_id);


--
-- Name: ix_service_applications_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_applications_professional_profile_id ON public.service_applications USING btree (professional_profile_id);


--
-- Name: ix_service_applications_service_request_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_applications_service_request_id ON public.service_applications USING btree (service_request_id);


--
-- Name: ix_service_applications_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_applications_status ON public.service_applications USING btree (status);


--
-- Name: ix_service_contacts_client_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_contacts_client_user_id ON public.service_contacts USING btree (client_user_id);


--
-- Name: ix_service_contacts_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_contacts_professional_profile_id ON public.service_contacts USING btree (professional_profile_id);


--
-- Name: ix_service_contacts_service_request_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_contacts_service_request_id ON public.service_contacts USING btree (service_request_id);


--
-- Name: ix_service_ratings_client_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_ratings_client_user_id ON public.service_ratings USING btree (client_user_id);


--
-- Name: ix_service_ratings_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_ratings_professional_profile_id ON public.service_ratings USING btree (professional_profile_id);


--
-- Name: ix_service_ratings_score; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_ratings_score ON public.service_ratings USING btree (score);


--
-- Name: ix_service_requests_assigned_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_requests_assigned_professional_profile_id ON public.service_requests USING btree (assigned_professional_profile_id);


--
-- Name: ix_service_requests_client_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_requests_client_user_id ON public.service_requests USING btree (client_user_id);


--
-- Name: ix_service_requests_created_at; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_requests_created_at ON public.service_requests USING btree (created_at);


--
-- Name: ix_service_requests_specialty_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_requests_specialty_id ON public.service_requests USING btree (specialty_id);


--
-- Name: ix_service_requests_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_requests_status ON public.service_requests USING btree (status);


--
-- Name: ix_service_requests_zone; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_service_requests_zone ON public.service_requests USING btree (zone);


--
-- Name: ix_user_addresses_user_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_user_addresses_user_id ON public.user_addresses USING btree (user_id);


--
-- Name: ix_user_addresses_zone; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_user_addresses_zone ON public.user_addresses USING btree (zone);


--
-- Name: ix_users_created_at; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_users_created_at ON public.users USING btree (created_at);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: ruper
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_role; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_users_role ON public.users USING btree (role);


--
-- Name: ix_users_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_users_status ON public.users USING btree (status);


--
-- Name: uq_user_addresses_primary_per_user; Type: INDEX; Schema: public; Owner: ruper
--

CREATE UNIQUE INDEX uq_user_addresses_primary_per_user ON public.user_addresses USING btree (user_id) WHERE (is_primary = true);


--
-- Name: certifications trg_certifications_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_certifications_updated_at BEFORE UPDATE ON public.certifications FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: professional_profiles trg_professional_profiles_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_professional_profiles_updated_at BEFORE UPDATE ON public.professional_profiles FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: professional_validation_queue trg_professional_validation_queue_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_professional_validation_queue_updated_at BEFORE UPDATE ON public.professional_validation_queue FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: service_ratings trg_service_ratings_recalculate_professional_rating; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_service_ratings_recalculate_professional_rating AFTER INSERT OR DELETE OR UPDATE ON public.service_ratings FOR EACH ROW EXECUTE FUNCTION public.trg_recalculate_professional_rating();


--
-- Name: service_ratings trg_service_ratings_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_service_ratings_updated_at BEFORE UPDATE ON public.service_ratings FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: service_requests trg_service_requests_recalculate_completed_services; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_service_requests_recalculate_completed_services AFTER INSERT OR DELETE OR UPDATE ON public.service_requests FOR EACH ROW EXECUTE FUNCTION public.trg_recalculate_completed_services();


--
-- Name: service_requests trg_service_requests_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_service_requests_updated_at BEFORE UPDATE ON public.service_requests FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user_addresses trg_user_addresses_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_user_addresses_updated_at BEFORE UPDATE ON public.user_addresses FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user_two_factor trg_user_two_factor_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_user_two_factor_updated_at BEFORE UPDATE ON public.user_two_factor FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users trg_users_updated_at; Type: TRIGGER; Schema: public; Owner: ruper
--

CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: administrative_notes fk_administrative_notes_author_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.administrative_notes
    ADD CONSTRAINT fk_administrative_notes_author_user_id FOREIGN KEY (author_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: administrative_reports fk_administrative_reports_generated_by; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.administrative_reports
    ADD CONSTRAINT fk_administrative_reports_generated_by FOREIGN KEY (generated_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: audit_logs fk_audit_logs_actor_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT fk_audit_logs_actor_user_id FOREIGN KEY (actor_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: certifications fk_certifications_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.certifications
    ADD CONSTRAINT fk_certifications_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: certifications fk_certifications_verified_by_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.certifications
    ADD CONSTRAINT fk_certifications_verified_by_user_id FOREIGN KEY (verified_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: professional_validation_queue fk_prof_validation_queue_assigned_support; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_validation_queue
    ADD CONSTRAINT fk_prof_validation_queue_assigned_support FOREIGN KEY (assigned_support_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: professional_validation_queue fk_prof_validation_queue_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_validation_queue
    ADD CONSTRAINT fk_prof_validation_queue_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: professional_validation_queue fk_prof_validation_queue_requested_by; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_validation_queue
    ADD CONSTRAINT fk_prof_validation_queue_requested_by FOREIGN KEY (requested_by_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: professional_availabilities fk_professional_availabilities_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_availabilities
    ADD CONSTRAINT fk_professional_availabilities_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: professional_profiles fk_professional_profiles_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_profiles
    ADD CONSTRAINT fk_professional_profiles_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: professional_profiles fk_professional_profiles_verified_by_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_profiles
    ADD CONSTRAINT fk_professional_profiles_verified_by_user_id_users FOREIGN KEY (verified_by_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: professional_specialties fk_professional_specialties_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT fk_professional_specialties_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: professional_specialties fk_professional_specialties_specialty_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT fk_professional_specialties_specialty_id FOREIGN KEY (specialty_id) REFERENCES public.specialties(id) ON DELETE RESTRICT;


--
-- Name: professional_zones fk_professional_zones_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_zones
    ADD CONSTRAINT fk_professional_zones_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: saved_professionals fk_saved_professionals_professional_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.saved_professionals
    ADD CONSTRAINT fk_saved_professionals_professional_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: saved_professionals fk_saved_professionals_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.saved_professionals
    ADD CONSTRAINT fk_saved_professionals_user_id FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: search_history fk_search_history_specialty_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.search_history
    ADD CONSTRAINT fk_search_history_specialty_id FOREIGN KEY (specialty_id) REFERENCES public.specialties(id) ON DELETE SET NULL;


--
-- Name: search_history fk_search_history_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.search_history
    ADD CONSTRAINT fk_search_history_user_id FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: service_applications fk_service_applications_professional_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_applications
    ADD CONSTRAINT fk_service_applications_professional_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: service_applications fk_service_applications_service_request_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_applications
    ADD CONSTRAINT fk_service_applications_service_request_id FOREIGN KEY (service_request_id) REFERENCES public.service_requests(id) ON DELETE CASCADE;


--
-- Name: service_contacts fk_service_contacts_client_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_contacts
    ADD CONSTRAINT fk_service_contacts_client_user_id FOREIGN KEY (client_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: service_contacts fk_service_contacts_professional_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_contacts
    ADD CONSTRAINT fk_service_contacts_professional_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE CASCADE;


--
-- Name: service_contacts fk_service_contacts_service_request_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_contacts
    ADD CONSTRAINT fk_service_contacts_service_request_id FOREIGN KEY (service_request_id) REFERENCES public.service_requests(id) ON DELETE SET NULL;


--
-- Name: service_ratings fk_service_ratings_client_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_ratings
    ADD CONSTRAINT fk_service_ratings_client_user_id FOREIGN KEY (client_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: service_ratings fk_service_ratings_professional_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_ratings
    ADD CONSTRAINT fk_service_ratings_professional_profile_id FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE RESTRICT;


--
-- Name: service_ratings fk_service_ratings_service_request_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_ratings
    ADD CONSTRAINT fk_service_ratings_service_request_id FOREIGN KEY (service_request_id) REFERENCES public.service_requests(id) ON DELETE CASCADE;


--
-- Name: service_requests fk_service_requests_assigned_professional_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_requests
    ADD CONSTRAINT fk_service_requests_assigned_professional_profile_id FOREIGN KEY (assigned_professional_profile_id) REFERENCES public.professional_profiles(id) ON DELETE SET NULL;


--
-- Name: service_requests fk_service_requests_client_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_requests
    ADD CONSTRAINT fk_service_requests_client_user_id FOREIGN KEY (client_user_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: service_requests fk_service_requests_specialty_id; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.service_requests
    ADD CONSTRAINT fk_service_requests_specialty_id FOREIGN KEY (specialty_id) REFERENCES public.specialties(id) ON DELETE RESTRICT;


--
-- Name: user_addresses fk_user_addresses_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_addresses
    ADD CONSTRAINT fk_user_addresses_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_two_factor user_two_factor_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_two_factor
    ADD CONSTRAINT user_two_factor_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict O3CQbRmiYm4ajDVRXkbPlsxjy9UTVXIZzu5h9mwUP7PeKsflnx5pnsJP4HsEQCV

