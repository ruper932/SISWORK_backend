--
-- PostgreSQL database dump
--

\restrict tCZFNBDUXWfzFCg2xvJDq2lPyHPLppE9AVZq1ZBIgyfcPMbktxL1EMnD5Ruopia

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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
-- Name: application_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.application_status_enum AS ENUM (
    'PENDING',
    'ACCEPTED',
    'REJECTED',
    'WITHDRAWN',
    'COMPLETED'
);


ALTER TYPE public.application_status_enum OWNER TO ruper;

--
-- Name: request_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.request_status_enum AS ENUM (
    'OPEN',
    'IN_PROGRESS',
    'COMPLETED',
    'CANCELLED',
    'EXPIRED'
);


ALTER TYPE public.request_status_enum OWNER TO ruper;

--
-- Name: urgency_level_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.urgency_level_enum AS ENUM (
    'LOW',
    'MEDIUM',
    'HIGH'
);


ALTER TYPE public.urgency_level_enum OWNER TO ruper;

--
-- Name: verification_document_type_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.verification_document_type_enum AS ENUM (
    'ID_CARD_FRONT',
    'ID_CARD_BACK',
    'SELFIE',
    'CERTIFICATE',
    'PDF_CERTIFICATION'
);


ALTER TYPE public.verification_document_type_enum OWNER TO ruper;

--
-- Name: verification_request_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.verification_request_status_enum AS ENUM (
    'PENDING',
    'UNDER_REVIEW',
    'APPROVED',
    'REJECTED'
);


ALTER TYPE public.verification_request_status_enum OWNER TO ruper;

--
-- Name: verification_status_enum; Type: TYPE; Schema: public; Owner: ruper
--

CREATE TYPE public.verification_status_enum AS ENUM (
    'PENDING',
    'UNDER_REVIEW',
    'APPROVED',
    'REJECTED'
);


ALTER TYPE public.verification_status_enum OWNER TO ruper;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ruper;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.applications (
    id uuid NOT NULL,
    request_id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    proposed_price numeric(10,2),
    status public.application_status_enum NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    proposal_message text NOT NULL,
    estimated_time_hours integer
);


ALTER TABLE public.applications OWNER TO ruper;

--
-- Name: files; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.files (
    id uuid NOT NULL,
    uploaded_by_ci character varying(20) NOT NULL,
    original_filename character varying(255) NOT NULL,
    stored_filename character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    mime_type character varying(100) NOT NULL,
    file_size bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.files OWNER TO ruper;

--
-- Name: professional_availabilities; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_availabilities (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    day_of_week integer NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.professional_availabilities OWNER TO ruper;

--
-- Name: professional_profiles; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_profiles (
    id uuid NOT NULL,
    user_ci character varying(20) NOT NULL,
    bio character varying(1000),
    experience_years integer NOT NULL,
    verification_status public.verification_status_enum NOT NULL,
    rating_average double precision NOT NULL,
    rating_count integer NOT NULL,
    is_available boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.professional_profiles OWNER TO ruper;

--
-- Name: professional_specialties; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.professional_specialties (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    specialty_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.professional_specialties OWNER TO ruper;

--
-- Name: requests; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.requests (
    id uuid NOT NULL,
    client_ci character varying(20) NOT NULL,
    specialty_id uuid NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    city character varying(100) NOT NULL,
    zone character varying(100),
    latitude double precision,
    longitude double precision,
    status public.request_status_enum NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    assigned_professional_profile_id uuid,
    budget numeric(10,2),
    proposed_final_price numeric(10,2),
    scheduled_date timestamp with time zone,
    urgency public.urgency_level_enum NOT NULL,
    is_review_enabled boolean NOT NULL,
    cancellation_reason text
);


ALTER TABLE public.requests OWNER TO ruper;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.reviews (
    id uuid NOT NULL,
    application_id uuid NOT NULL,
    reviewer_ci character varying(20) NOT NULL,
    rating integer NOT NULL,
    comment text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    reviewed_user_ci character varying NOT NULL,
    CONSTRAINT ck_reviews_check_review_rating CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.reviews OWNER TO ruper;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(255)
);


ALTER TABLE public.roles OWNER TO ruper;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: ruper
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO ruper;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ruper
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: specialties; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.specialties (
    id uuid NOT NULL,
    name character varying(150) NOT NULL,
    description character varying(500),
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.specialties OWNER TO ruper;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_ci character varying(20) NOT NULL,
    role_id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.user_roles OWNER TO ruper;

--
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: ruper
--

CREATE SEQUENCE public.user_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_roles_id_seq OWNER TO ruper;

--
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ruper
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.users (
    ci character varying(20) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    mother_last_name character varying(100),
    birth_date date NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(30) NOT NULL,
    whatsapp_enabled boolean NOT NULL,
    password_hash character varying(255) NOT NULL,
    profile_photo_path character varying(500),
    city character varying(100),
    zone character varying(100),
    latitude double precision,
    longitude double precision,
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    last_login timestamp with time zone,
    failed_login_attempts integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO ruper;

--
-- Name: verification_documents; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.verification_documents (
    id uuid NOT NULL,
    verification_request_id uuid NOT NULL,
    file_id uuid NOT NULL,
    document_type public.verification_document_type_enum NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.verification_documents OWNER TO ruper;

--
-- Name: verification_requests; Type: TABLE; Schema: public; Owner: ruper
--

CREATE TABLE public.verification_requests (
    id uuid NOT NULL,
    professional_profile_id uuid NOT NULL,
    status public.verification_request_status_enum NOT NULL,
    rejection_reason character varying(1000),
    reviewed_by_ci character varying(20),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.verification_requests OWNER TO ruper;

--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.alembic_version (version_num) FROM stdin;
71720a3c289c
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.applications (id, request_id, professional_profile_id, proposed_price, status, created_at, updated_at, proposal_message, estimated_time_hours) FROM stdin;
\.


--
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.files (id, uploaded_by_ci, original_filename, stored_filename, file_path, mime_type, file_size, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: professional_availabilities; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_availabilities (id, professional_profile_id, day_of_week, start_time, end_time, is_active, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: professional_profiles; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_profiles (id, user_ci, bio, experience_years, verification_status, rating_average, rating_count, is_available, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: professional_specialties; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.professional_specialties (id, professional_profile_id, specialty_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.requests (id, client_ci, specialty_id, title, description, city, zone, latitude, longitude, status, created_at, updated_at, assigned_professional_profile_id, budget, proposed_final_price, scheduled_date, urgency, is_review_enabled, cancellation_reason) FROM stdin;
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.reviews (id, application_id, reviewer_ci, rating, comment, created_at, updated_at, reviewed_user_ci) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.roles (id, name, description) FROM stdin;
1	CLIENT	\N
2	PROFESSIONAL	\N
3	ADMIN	\N
4	SUPPORT	\N
5	SUPERADMIN	\N
\.


--
-- Data for Name: specialties; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.specialties (id, name, description, is_active, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.user_roles (id, user_ci, role_id, created_at, updated_at) FROM stdin;
1	SUPERADMIN	5	2026-05-22 15:10:20.476758-04	2026-05-22 15:10:20.47676-04
2	CLIENT001	1	2026-05-22 15:10:20.523673-04	2026-05-22 15:10:20.523675-04
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.users (ci, first_name, last_name, mother_last_name, birth_date, email, phone, whatsapp_enabled, password_hash, profile_photo_path, city, zone, latitude, longitude, is_active, is_verified, last_login, failed_login_attempts, created_at, updated_at, deleted_at) FROM stdin;
SUPERADMIN	Super	Admin	System	1990-01-01	superadmin@siswork.com	70000000	t	$argon2id$v=19$m=65536,t=3,p=4$UOWCSH3Zh/dCApCJwoH46Q$LfQUopL82f48ITUpORthTFtGSB8VgoWIROybET8zQyY	\N	La Paz	Central	\N	\N	t	t	\N	0	2026-05-22 15:10:20.471056-04	2026-05-22 15:10:20.47106-04	\N
CLIENT001	Test	Client	User	1998-05-10	client@siswork.com	71111111	t	$argon2id$v=19$m=65536,t=3,p=4$DfwllgK/JOgnfgukL9WTOA$qnpuY4Yj9efx9WoPArpfq5gPYDwOo3YUN+QLuYk2so4	\N	La Paz	Sopocachi	\N	\N	t	f	\N	0	2026-05-22 15:10:20.519186-04	2026-05-22 15:10:20.51919-04	\N
\.


--
-- Data for Name: verification_documents; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.verification_documents (id, verification_request_id, file_id, document_type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: verification_requests; Type: TABLE DATA; Schema: public; Owner: ruper
--

COPY public.verification_requests (id, professional_profile_id, status, rejection_reason, reviewed_by_ci, created_at, updated_at, deleted_at) FROM stdin;
\.


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ruper
--

SELECT pg_catalog.setval('public.roles_id_seq', 5, true);


--
-- Name: user_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ruper
--

SELECT pg_catalog.setval('public.user_roles_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: applications pk_applications; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT pk_applications PRIMARY KEY (id);


--
-- Name: files pk_files; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT pk_files PRIMARY KEY (id);


--
-- Name: professional_availabilities pk_professional_availabilities; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_availabilities
    ADD CONSTRAINT pk_professional_availabilities PRIMARY KEY (id);


--
-- Name: professional_profiles pk_professional_profiles; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_profiles
    ADD CONSTRAINT pk_professional_profiles PRIMARY KEY (id);


--
-- Name: professional_specialties pk_professional_specialties; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT pk_professional_specialties PRIMARY KEY (id);


--
-- Name: requests pk_requests; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT pk_requests PRIMARY KEY (id);


--
-- Name: reviews pk_reviews; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT pk_reviews PRIMARY KEY (id);


--
-- Name: roles pk_roles; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT pk_roles PRIMARY KEY (id);


--
-- Name: specialties pk_specialties; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT pk_specialties PRIMARY KEY (id);


--
-- Name: user_roles pk_user_roles; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT pk_user_roles PRIMARY KEY (id);


--
-- Name: users pk_users; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (ci);


--
-- Name: verification_documents pk_verification_documents; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.verification_documents
    ADD CONSTRAINT pk_verification_documents PRIMARY KEY (id);


--
-- Name: verification_requests pk_verification_requests; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.verification_requests
    ADD CONSTRAINT pk_verification_requests PRIMARY KEY (id);


--
-- Name: applications uq_application_request_professional; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT uq_application_request_professional UNIQUE (request_id, professional_profile_id);


--
-- Name: files uq_files_stored_filename; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT uq_files_stored_filename UNIQUE (stored_filename);


--
-- Name: professional_availabilities uq_professional_day; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_availabilities
    ADD CONSTRAINT uq_professional_day UNIQUE (professional_profile_id, day_of_week);


--
-- Name: professional_specialties uq_professional_specialty; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT uq_professional_specialty UNIQUE (professional_profile_id, specialty_id);


--
-- Name: user_roles uq_user_role; Type: CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT uq_user_role UNIQUE (user_ci, role_id);


--
-- Name: idx_request_location; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX idx_request_location ON public.requests USING btree (city, zone);


--
-- Name: ix_applications_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_applications_professional_profile_id ON public.applications USING btree (professional_profile_id);


--
-- Name: ix_applications_request_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_applications_request_id ON public.applications USING btree (request_id);


--
-- Name: ix_files_uploaded_by_ci; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_files_uploaded_by_ci ON public.files USING btree (uploaded_by_ci);


--
-- Name: ix_professional_availabilities_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_availabilities_professional_profile_id ON public.professional_availabilities USING btree (professional_profile_id);


--
-- Name: ix_professional_profiles_user_ci; Type: INDEX; Schema: public; Owner: ruper
--

CREATE UNIQUE INDEX ix_professional_profiles_user_ci ON public.professional_profiles USING btree (user_ci);


--
-- Name: ix_professional_profiles_verification_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_profiles_verification_status ON public.professional_profiles USING btree (verification_status);


--
-- Name: ix_professional_specialties_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_specialties_professional_profile_id ON public.professional_specialties USING btree (professional_profile_id);


--
-- Name: ix_professional_specialties_specialty_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_professional_specialties_specialty_id ON public.professional_specialties USING btree (specialty_id);


--
-- Name: ix_requests_client_ci; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_requests_client_ci ON public.requests USING btree (client_ci);


--
-- Name: ix_requests_specialty_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_requests_specialty_id ON public.requests USING btree (specialty_id);


--
-- Name: ix_requests_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_requests_status ON public.requests USING btree (status);


--
-- Name: ix_reviews_application_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_reviews_application_id ON public.reviews USING btree (application_id);


--
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: ruper
--

CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- Name: ix_specialties_name; Type: INDEX; Schema: public; Owner: ruper
--

CREATE UNIQUE INDEX ix_specialties_name ON public.specialties USING btree (name);


--
-- Name: ix_user_roles_role_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_user_roles_role_id ON public.user_roles USING btree (role_id);


--
-- Name: ix_user_roles_user_ci; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_user_roles_user_ci ON public.user_roles USING btree (user_ci);


--
-- Name: ix_users_ci; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_users_ci ON public.users USING btree (ci);


--
-- Name: ix_users_city; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_users_city ON public.users USING btree (city);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: ruper
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_phone; Type: INDEX; Schema: public; Owner: ruper
--

CREATE UNIQUE INDEX ix_users_phone ON public.users USING btree (phone);


--
-- Name: ix_users_zone; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_users_zone ON public.users USING btree (zone);


--
-- Name: ix_verification_documents_file_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_verification_documents_file_id ON public.verification_documents USING btree (file_id);


--
-- Name: ix_verification_documents_verification_request_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_verification_documents_verification_request_id ON public.verification_documents USING btree (verification_request_id);


--
-- Name: ix_verification_requests_professional_profile_id; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_verification_requests_professional_profile_id ON public.verification_requests USING btree (professional_profile_id);


--
-- Name: ix_verification_requests_status; Type: INDEX; Schema: public; Owner: ruper
--

CREATE INDEX ix_verification_requests_status ON public.verification_requests USING btree (status);


--
-- Name: applications fk_applications_professional_profile_id_applications; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT fk_applications_professional_profile_id_applications FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id);


--
-- Name: applications fk_applications_request_id_applications; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT fk_applications_request_id_applications FOREIGN KEY (request_id) REFERENCES public.requests(id);


--
-- Name: files fk_files_uploaded_by_ci_files; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT fk_files_uploaded_by_ci_files FOREIGN KEY (uploaded_by_ci) REFERENCES public.users(ci);


--
-- Name: professional_availabilities fk_professional_availabilities_professional_profile_id__2616; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_availabilities
    ADD CONSTRAINT fk_professional_availabilities_professional_profile_id__2616 FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id);


--
-- Name: professional_profiles fk_professional_profiles_user_ci_professional_profiles; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_profiles
    ADD CONSTRAINT fk_professional_profiles_user_ci_professional_profiles FOREIGN KEY (user_ci) REFERENCES public.users(ci);


--
-- Name: professional_specialties fk_professional_specialties_professional_profile_id_pro_075a; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT fk_professional_specialties_professional_profile_id_pro_075a FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id);


--
-- Name: professional_specialties fk_professional_specialties_specialty_id_professional_s_0033; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.professional_specialties
    ADD CONSTRAINT fk_professional_specialties_specialty_id_professional_s_0033 FOREIGN KEY (specialty_id) REFERENCES public.specialties(id);


--
-- Name: requests fk_requests_assigned_professional_profile; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_assigned_professional_profile FOREIGN KEY (assigned_professional_profile_id) REFERENCES public.professional_profiles(id);


--
-- Name: requests fk_requests_client_ci_requests; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_client_ci_requests FOREIGN KEY (client_ci) REFERENCES public.users(ci);


--
-- Name: requests fk_requests_specialty_id_requests; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT fk_requests_specialty_id_requests FOREIGN KEY (specialty_id) REFERENCES public.specialties(id);


--
-- Name: reviews fk_reviews_application_id_reviews; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_application_id_reviews FOREIGN KEY (application_id) REFERENCES public.applications(id);


--
-- Name: reviews fk_reviews_reviewed_user_ci_users; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_reviewed_user_ci_users FOREIGN KEY (reviewed_user_ci) REFERENCES public.users(ci);


--
-- Name: reviews fk_reviews_reviewer_ci_reviews; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_reviewer_ci_reviews FOREIGN KEY (reviewer_ci) REFERENCES public.users(ci);


--
-- Name: user_roles fk_user_roles_role_id_user_roles; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT fk_user_roles_role_id_user_roles FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- Name: user_roles fk_user_roles_user_ci_user_roles; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT fk_user_roles_user_ci_user_roles FOREIGN KEY (user_ci) REFERENCES public.users(ci);


--
-- Name: verification_documents fk_verification_documents_file_id_verification_documents; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.verification_documents
    ADD CONSTRAINT fk_verification_documents_file_id_verification_documents FOREIGN KEY (file_id) REFERENCES public.files(id);


--
-- Name: verification_documents fk_verification_documents_verification_request_id_verif_2f87; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.verification_documents
    ADD CONSTRAINT fk_verification_documents_verification_request_id_verif_2f87 FOREIGN KEY (verification_request_id) REFERENCES public.verification_requests(id);


--
-- Name: verification_requests fk_verification_requests_professional_profile_id_verifi_de30; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.verification_requests
    ADD CONSTRAINT fk_verification_requests_professional_profile_id_verifi_de30 FOREIGN KEY (professional_profile_id) REFERENCES public.professional_profiles(id);


--
-- Name: verification_requests fk_verification_requests_reviewed_by_ci_verification_requests; Type: FK CONSTRAINT; Schema: public; Owner: ruper
--

ALTER TABLE ONLY public.verification_requests
    ADD CONSTRAINT fk_verification_requests_reviewed_by_ci_verification_requests FOREIGN KEY (reviewed_by_ci) REFERENCES public.users(ci);


--
-- PostgreSQL database dump complete
--

\unrestrict tCZFNBDUXWfzFCg2xvJDq2lPyHPLppE9AVZq1ZBIgyfcPMbktxL1EMnD5Ruopia

