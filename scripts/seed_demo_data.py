from __future__ import annotations

import random
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from app.core.security import hash_password
from app.db.enums import (
    ApplicationStatusEnum,
    RequestStatusEnum,
    RoleEnum,
    UrgencyLevelEnum,
    VerificationStatusEnum,
)
from app.db.database import SessionLocal
from app.models.application import Application
from app.models.professional_availability import ProfessionalAvailability
from app.models.professional_profile import ProfessionalProfile
from app.models.professional_specialty import ProfessionalSpecialty
from app.models.request import Request
from app.models.review import Review
from app.models.role import Role
from app.models.specialty import Specialty
from app.models.user import User
from app.models.user_role import UserRole


RANDOM_SEED = 42
DEFAULT_PASSWORD = "demons312es"

SPECIALTIES = [
    ("Electricista", "Instalaciones eléctricas, tomacorrientes, tableros y mantenimiento."),
    ("Plomería", "Reparación de fugas, grifería, tuberías y sanitarios."),
    ("Albañilería", "Obra fina, refacciones, revoque y ampliaciones."),
    ("Pintura", "Pintado interior y exterior, resanes y acabados."),
    ("Carpintería", "Muebles, puertas, closets y estructuras de madera."),
    ("Cerrajería", "Apertura, cambio de chapas, cerraduras y refuerzos."),
    ("Jardinería", "Mantenimiento de jardines, poda y diseño básico."),
    ("Limpieza", "Limpieza profunda, postobra y mantenimiento doméstico."),
    ("Gasfitería", "Instalaciones de gas, revisiones y mantenimiento."),
    ("Técnico de electrodomésticos", "Reparación de lavadoras, refrigeradores y cocinas."),
    ("Soldadura", "Rejas, estructuras metálicas y reparaciones."),
    ("Yesero", "Cielos falsos, yeso y terminaciones interiores."),
]

CLIENTS = [
    {
        "ci": "CLI1001",
        "first_name": "María",
        "last_name": "Lopez",
        "mother_last_name": "Quispe",
        "birth_date": date(1992, 3, 15),
        "email": "maria.lopez@siswork.demo",
        "phone": "71000001",
        "city": "La Paz",
        "zone": "Sopocachi",
        "latitude": -16.5111,
        "longitude": -68.1246,
    },
    {
        "ci": "CLI1002",
        "first_name": "Carlos",
        "last_name": "Fernandez",
        "mother_last_name": "Rojas",
        "birth_date": date(1988, 7, 11),
        "email": "carlos.fernandez@siswork.demo",
        "phone": "71000002",
        "city": "La Paz",
        "zone": "Miraflores",
        "latitude": -16.4998,
        "longitude": -68.1193,
    },
    {
        "ci": "CLI1003",
        "first_name": "Lucía",
        "last_name": "Mamani",
        "mother_last_name": "Flores",
        "birth_date": date(1995, 1, 22),
        "email": "lucia.mamani@siswork.demo",
        "phone": "71000003",
        "city": "La Paz",
        "zone": "Calacoto",
        "latitude": -16.5348,
        "longitude": -68.0875,
    },
    {
        "ci": "CLI1004",
        "first_name": "Andrés",
        "last_name": "Vargas",
        "mother_last_name": "Mendoza",
        "birth_date": date(1990, 9, 2),
        "email": "andres.vargas@siswork.demo",
        "phone": "71000004",
        "city": "La Paz",
        "zone": "San Miguel",
        "latitude": -16.5400,
        "longitude": -68.0770,
    },
    {
        "ci": "CLI1005",
        "first_name": "Daniela",
        "last_name": "Choque",
        "mother_last_name": "Nina",
        "birth_date": date(1994, 6, 18),
        "email": "daniela.choque@siswork.demo",
        "phone": "71000005",
        "city": "La Paz",
        "zone": "Achumani",
        "latitude": -16.5533,
        "longitude": -68.0642,
    },
    {
        "ci": "CLI1006",
        "first_name": "José",
        "last_name": "Rivera",
        "mother_last_name": "Aliaga",
        "birth_date": date(1987, 11, 5),
        "email": "jose.rivera@siswork.demo",
        "phone": "71000006",
        "city": "El Alto",
        "zone": "Ciudad Satélite",
        "latitude": -16.5130,
        "longitude": -68.1637,
    },
    {
        "ci": "CLI1007",
        "first_name": "Paola",
        "last_name": "Torrez",
        "mother_last_name": "Gutiérrez",
        "birth_date": date(1991, 12, 8),
        "email": "paola.torrez@siswork.demo",
        "phone": "71000007",
        "city": "La Paz",
        "zone": "Obrajes",
        "latitude": -16.5231,
        "longitude": -68.1022,
    },
    {
        "ci": "CLI1008",
        "first_name": "Miguel",
        "last_name": "Soria",
        "mother_last_name": "Lima",
        "birth_date": date(1989, 4, 9),
        "email": "miguel.soria@siswork.demo",
        "phone": "71000008",
        "city": "La Paz",
        "zone": "Villa Fátima",
        "latitude": -16.4795,
        "longitude": -68.1132,
    },
    {
        "ci": "CLI1009",
        "first_name": "Valeria",
        "last_name": "Calle",
        "mother_last_name": "Paredes",
        "birth_date": date(1996, 2, 12),
        "email": "valeria.calle@siswork.demo",
        "phone": "71000009",
        "city": "La Paz",
        "zone": "Centro",
        "latitude": -16.4959,
        "longitude": -68.1336,
    },
    {
        "ci": "CLI1010",
        "first_name": "Raúl",
        "last_name": "Condori",
        "mother_last_name": "Apaza",
        "birth_date": date(1986, 8, 29),
        "email": "raul.condori@siswork.demo",
        "phone": "71000010",
        "city": "El Alto",
        "zone": "16 de Julio",
        "latitude": -16.4951,
        "longitude": -68.1942,
    },
]

PROFESSIONALS = [
    {
        "ci": "PRO2001",
        "first_name": "Jorge",
        "last_name": "Mendoza",
        "mother_last_name": "Quisbert",
        "birth_date": date(1985, 5, 10),
        "email": "jorge.mendoza@siswork.demo",
        "phone": "72000001",
        "city": "La Paz",
        "zone": "Sopocachi",
        "latitude": -16.5120,
        "longitude": -68.1280,
        "bio": "Electricista con experiencia en instalaciones domiciliarias, tableros y mantenimiento preventivo.",
        "experience_years": 12,
        "is_available": True,
        "specialties": ["Electricista"],
    },
    {
        "ci": "PRO2002",
        "first_name": "Patricia",
        "last_name": "Luna",
        "mother_last_name": "Mamani",
        "birth_date": date(1990, 1, 20),
        "email": "patricia.luna@siswork.demo",
        "phone": "72000002",
        "city": "La Paz",
        "zone": "Miraflores",
        "latitude": -16.5005,
        "longitude": -68.1189,
        "bio": "Especialista en plomería, cambio de grifería, fugas y mantenimiento de baños y cocinas.",
        "experience_years": 8,
        "is_available": True,
        "specialties": ["Plomería", "Gasfitería"],
    },
    {
        "ci": "PRO2003",
        "first_name": "Wilson",
        "last_name": "Choque",
        "mother_last_name": "Ticona",
        "birth_date": date(1983, 6, 14),
        "email": "wilson.choque@siswork.demo",
        "phone": "72000003",
        "city": "El Alto",
        "zone": "Ciudad Satélite",
        "latitude": -16.5121,
        "longitude": -68.1645,
        "bio": "Maestro albañil para refacciones, ampliaciones, obra fina y mantenimiento general.",
        "experience_years": 15,
        "is_available": True,
        "specialties": ["Albañilería", "Yesero"],
    },
    {
        "ci": "PRO2004",
        "first_name": "Carla",
        "last_name": "Rojas",
        "mother_last_name": "Flores",
        "birth_date": date(1992, 3, 7),
        "email": "carla.rojas@siswork.demo",
        "phone": "72000004",
        "city": "La Paz",
        "zone": "Calacoto",
        "latitude": -16.5340,
        "longitude": -68.0881,
        "bio": "Pintora de interiores y exteriores, con enfoque en acabados limpios y resane de muros.",
        "experience_years": 7,
        "is_available": True,
        "specialties": ["Pintura"],
    },
    {
        "ci": "PRO2005",
        "first_name": "Eduardo",
        "last_name": "Paredes",
        "mother_last_name": "Cruz",
        "birth_date": date(1987, 9, 1),
        "email": "eduardo.paredes@siswork.demo",
        "phone": "72000005",
        "city": "La Paz",
        "zone": "San Miguel",
        "latitude": -16.5392,
        "longitude": -68.0765,
        "bio": "Carpintero para muebles a medida, puertas, closets y reparaciones de madera.",
        "experience_years": 10,
        "is_available": True,
        "specialties": ["Carpintería"],
    },
    {
        "ci": "PRO2006",
        "first_name": "Roxana",
        "last_name": "Arce",
        "mother_last_name": "Salazar",
        "birth_date": date(1991, 8, 30),
        "email": "roxana.arce@siswork.demo",
        "phone": "72000006",
        "city": "La Paz",
        "zone": "Obrajes",
        "latitude": -16.5227,
        "longitude": -68.1030,
        "bio": "Servicio de limpieza profunda, postobra y mantenimiento de departamentos y oficinas.",
        "experience_years": 6,
        "is_available": True,
        "specialties": ["Limpieza"],
    },
    {
        "ci": "PRO2007",
        "first_name": "Luis",
        "last_name": "Acuña",
        "mother_last_name": "Vargas",
        "birth_date": date(1984, 12, 17),
        "email": "luis.acuna@siswork.demo",
        "phone": "72000007",
        "city": "El Alto",
        "zone": "16 de Julio",
        "latitude": -16.4962,
        "longitude": -68.1935,
        "bio": "Cerrajero con atención rápida para apertura, cambio de chapas y refuerzo de puertas.",
        "experience_years": 11,
        "is_available": True,
        "specialties": ["Cerrajería"],
    },
    {
        "ci": "PRO2008",
        "first_name": "Mónica",
        "last_name": "Quiroga",
        "mother_last_name": "Navia",
        "birth_date": date(1989, 10, 26),
        "email": "monica.quiroga@siswork.demo",
        "phone": "72000008",
        "city": "La Paz",
        "zone": "Achumani",
        "latitude": -16.5525,
        "longitude": -68.0635,
        "bio": "Jardinera para poda, mantenimiento y mejora estética de jardines y patios.",
        "experience_years": 9,
        "is_available": True,
        "specialties": ["Jardinería"],
    },
    {
        "ci": "PRO2009",
        "first_name": "Sergio",
        "last_name": "Velasco",
        "mother_last_name": "Peñaranda",
        "birth_date": date(1986, 2, 3),
        "email": "sergio.velasco@siswork.demo",
        "phone": "72000009",
        "city": "La Paz",
        "zone": "Villa Fátima",
        "latitude": -16.4803,
        "longitude": -68.1127,
        "bio": "Técnico en electrodomésticos con experiencia en línea blanca y mantenimiento correctivo.",
        "experience_years": 13,
        "is_available": True,
        "specialties": ["Técnico de electrodomésticos"],
    },
    {
        "ci": "PRO2010",
        "first_name": "Ana",
        "last_name": "Condori",
        "mother_last_name": "López",
        "birth_date": date(1993, 11, 19),
        "email": "ana.condori@siswork.demo",
        "phone": "72000010",
        "city": "La Paz",
        "zone": "Centro",
        "latitude": -16.4950,
        "longitude": -68.1341,
        "bio": "Soldadora y técnica en estructuras metálicas, rejas, barandas y reparaciones.",
        "experience_years": 7,
        "is_available": True,
        "specialties": ["Soldadura"],
    },
]

REQUEST_TEMPLATES = [
    ("Cambio de instalación eléctrica en cocina", "Necesito revisar cableado, cambiar tomas y asegurar que el tablero soporte nuevos equipos."),
    ("Reparación de fuga en baño principal", "Hay una fuga constante debajo del lavamanos y también se debe revisar la presión del agua."),
    ("Pintado completo de departamento", "Busco pintar sala, comedor y dos habitaciones con resane previo de grietas pequeñas."),
    ("Armado de muebles de cocina", "Necesito apoyo para instalar módulos nuevos y ajustar puertas de melamina."),
    ("Cambio de chapa principal", "La cerradura principal falla y necesito una solución segura el mismo día."),
    ("Mantenimiento de jardín delantero", "Poda, limpieza, retiro de maleza y recomendación para mejorar el diseño del espacio."),
    ("Refacción de pared con humedad", "Una pared presenta humedad y desprendimiento de yeso. Se requiere evaluación y reparación."),
    ("Limpieza profunda post obra", "Necesito limpieza profunda después de una remodelación, incluyendo polvo fino y residuos."),
    ("Revisión de cocina a gas", "Se requiere inspección de conexiones y cambio de una válvula con fuga."),
    ("Reparación de refrigerador", "El refrigerador dejó de enfriar correctamente y hace ruido al encender."),
    ("Instalación de reja metálica", "Necesito fabricar e instalar una reja para ventana con medidas específicas."),
    ("Cambio de puertas de closet", "Quiero reemplazar puertas antiguas y nivelar rieles en un closet empotrado."),
    ("Nivelación y acabado de muro", "Se debe emparejar un muro interior y dejarlo listo para pintar."),
    ("Instalación de lámparas y apliques", "Colocar tres lámparas, dos apliques y revisar una llave térmica."),
    ("Mantenimiento integral de baño", "Cambio de grifería, ajuste de sanitario y revisión de filtraciones menores."),
]

REVIEW_COMMENTS = [
    "Excelente trabajo, llegó puntual y dejó todo funcionando correctamente.",
    "Muy buena atención y explicación clara del problema y la solución.",
    "Cumplió con el tiempo acordado y el acabado fue mejor de lo esperado.",
    "Trabajo responsable, ordenado y con buena comunicación en todo momento.",
    "Recomendado, resolvió el problema sin complicaciones y con buen trato.",
    "Muy profesional, cuidó los detalles y dejó el área limpia.",
    "Buena experiencia, volvería a contratar este servicio sin problema.",
    "Atención rápida y resultado sólido, quedó conforme toda la familia.",
    "Mostró experiencia y dio alternativas útiles para evitar futuros problemas.",
    "Servicio correcto, transparente con el precio y puntual con la visita.",
]


def random_decimal(min_value: int, max_value: int) -> Decimal:
    return Decimal(str(random.randint(min_value, max_value)))


def ensure_role(db, name: str, description: str | None = None) -> Role:
    role = db.scalar(select(Role).where(Role.name == name))
    if role:
        if role.description != description:
            role.description = description
            db.commit()
            db.refresh(role)
        return role

    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def ensure_user(
    db,
    *,
    ci: str,
    first_name: str,
    last_name: str,
    mother_last_name: str | None,
    birth_date: date,
    email: str,
    phone: str,
    city: str | None,
    zone: str | None,
    latitude: float | None = None,
    longitude: float | None = None,
    is_verified: bool = True,
) -> User:
    user = db.scalar(select(User).where(User.ci == ci))
    if user:
        changed = False
        updates = {
            "first_name": first_name,
            "last_name": last_name,
            "mother_last_name": mother_last_name,
            "birth_date": birth_date,
            "email": email,
            "phone": phone,
            "city": city,
            "zone": zone,
            "latitude": latitude,
            "longitude": longitude,
            "is_verified": is_verified,
            "is_active": True,
        }
        for field, value in updates.items():
            if getattr(user, field) != value:
                setattr(user, field, value)
                changed = True
        if changed:
            db.commit()
            db.refresh(user)
        return user

    user = User(
        ci=ci,
        first_name=first_name,
        last_name=last_name,
        mother_last_name=mother_last_name,
        birth_date=birth_date,
        email=email,
        phone=phone,
        password_hash=hash_password(DEFAULT_PASSWORD),
        city=city,
        zone=zone,
        latitude=latitude,
        longitude=longitude,
        is_active=True,
        is_verified=is_verified,
        failed_login_attempts=0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def ensure_user_role(db, user_ci: str, role_name: str) -> UserRole:
    role = db.scalar(select(Role).where(Role.name == role_name))
    existing = db.scalar(
        select(UserRole).where(
            UserRole.user_ci == user_ci,
            UserRole.role_id == role.id,
        )
    )
    if existing:
        return existing

    user_role = UserRole(user_ci=user_ci, role_id=role.id)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


def ensure_specialty(db, name: str, description: str) -> Specialty:
    specialty = db.scalar(select(Specialty).where(Specialty.name == name))
    if specialty:
        changed = False
        if specialty.description != description:
            specialty.description = description
            changed = True
        if specialty.is_active is not True:
            specialty.is_active = True
            changed = True
        if changed:
            db.commit()
            db.refresh(specialty)
        return specialty

    specialty = Specialty(
        name=name,
        description=description,
        is_active=True,
    )
    db.add(specialty)
    db.commit()
    db.refresh(specialty)
    return specialty


def ensure_professional_profile(
    db,
    *,
    user_ci: str,
    bio: str,
    experience_years: int,
    is_available: bool,
    verification_status: VerificationStatusEnum = VerificationStatusEnum.APPROVED,
) -> ProfessionalProfile:
    profile = db.scalar(
        select(ProfessionalProfile).where(ProfessionalProfile.user_ci == user_ci)
    )
    if profile:
        profile.bio = bio
        profile.experience_years = experience_years
        profile.is_available = is_available
        profile.verification_status = verification_status
        db.commit()
        db.refresh(profile)
        return profile

    profile = ProfessionalProfile(
        user_ci=user_ci,
        bio=bio,
        experience_years=experience_years,
        verification_status=verification_status,
        rating_average=0.0,
        rating_count=0,
        is_available=is_available,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def ensure_professional_specialty(
    db,
    professional_profile_id,
    specialty_id,
) -> ProfessionalSpecialty:
    link = db.scalar(
        select(ProfessionalSpecialty).where(
            ProfessionalSpecialty.professional_profile_id == professional_profile_id,
            ProfessionalSpecialty.specialty_id == specialty_id,
        )
    )
    if link:
        return link

    link = ProfessionalSpecialty(
        professional_profile_id=professional_profile_id,
        specialty_id=specialty_id,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def ensure_availability(
    db,
    professional_profile_id,
    day_of_week: int,
    start_time: time,
    end_time: time,
    is_active: bool = True,
) -> ProfessionalAvailability:
    availability = db.scalar(
        select(ProfessionalAvailability).where(
            ProfessionalAvailability.professional_profile_id == professional_profile_id,
            ProfessionalAvailability.day_of_week == day_of_week,
        )
    )
    if availability:
        availability.start_time = start_time
        availability.end_time = end_time
        availability.is_active = is_active
        db.commit()
        db.refresh(availability)
        return availability

    availability = ProfessionalAvailability(
        professional_profile_id=professional_profile_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        is_active=is_active,
    )
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


def ensure_request(
    db,
    *,
    client_ci: str,
    specialty_id,
    title: str,
    description: str,
    city: str,
    zone: str | None,
    latitude: float | None,
    longitude: float | None,
    budget: Decimal | None,
    urgency: UrgencyLevelEnum,
    scheduled_date: datetime | None,
) -> Request:
    request = db.scalar(
        select(Request).where(
            Request.client_ci == client_ci,
            Request.title == title,
        )
    )
    if request:
        request.specialty_id = specialty_id
        request.description = description
        request.city = city
        request.zone = zone
        request.latitude = latitude
        request.longitude = longitude
        request.budget = budget
        request.urgency = urgency
        request.scheduled_date = scheduled_date
        request.status = RequestStatusEnum.PENDING
        request.assigned_professional_profile_id = None
        request.proposed_final_price = None
        request.is_review_enabled = False
        request.cancellation_reason = None
        db.commit()
        db.refresh(request)
        return request

    request = Request(
        client_ci=client_ci,
        specialty_id=specialty_id,
        title=title,
        description=description,
        budget=budget,
        proposed_final_price=None,
        scheduled_date=scheduled_date,
        city=city,
        zone=zone,
        latitude=latitude,
        longitude=longitude,
        urgency=urgency,
        status=RequestStatusEnum.PENDING,
        is_review_enabled=False,
        cancellation_reason=None,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def ensure_application(
    db,
    *,
    request_id,
    professional_profile_id,
    proposal_message: str,
    proposed_price: Decimal | None,
    estimated_time_hours: int | None,
) -> Application:
    application = db.scalar(
        select(Application).where(
            Application.request_id == request_id,
            Application.professional_profile_id == professional_profile_id,
        )
    )
    if application:
        application.proposal_message = proposal_message
        application.proposed_price = proposed_price
        application.estimated_time_hours = estimated_time_hours
        db.commit()
        db.refresh(application)
        return application

    application = Application(
        request_id=request_id,
        professional_profile_id=professional_profile_id,
        proposal_message=proposal_message,
        proposed_price=proposed_price,
        estimated_time_hours=estimated_time_hours,
        status=ApplicationStatusEnum.PENDING,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def ensure_review(
    db,
    *,
    application_id,
    reviewer_ci: str,
    reviewed_user_ci: str,
    rating: int,
    comment: str,
) -> Review:
    review = db.scalar(
        select(Review).where(
            Review.application_id == application_id,
            Review.reviewer_ci == reviewer_ci,
        )
    )
    if review:
        review.reviewed_user_ci = reviewed_user_ci
        review.rating = rating
        review.comment = comment
        db.commit()
        db.refresh(review)
        return review

    review = Review(
        application_id=application_id,
        reviewer_ci=reviewer_ci,
        reviewed_user_ci=reviewed_user_ci,
        rating=rating,
        comment=comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def recalculate_professional_ratings(db) -> None:
    profiles = db.scalars(select(ProfessionalProfile)).all()
    for profile in profiles:
        avg_rating, rating_count = db.execute(
            select(
                func.avg(Review.rating),
                func.count(Review.id),
            )
            .join(Application, Application.id == Review.application_id)
            .where(Application.professional_profile_id == profile.id)
        ).one()
        profile.rating_average = float(avg_rating or 0.0)
        profile.rating_count = int(rating_count or 0)
    db.commit()


def seed_roles(db) -> None:
    ensure_role(db, RoleEnum.CLIENT.value, "Cliente del marketplace")
    ensure_role(db, RoleEnum.PROFESSIONAL.value, "Profesional del marketplace")
    ensure_role(db, RoleEnum.ADMIN.value, "Administrador")
    ensure_role(db, RoleEnum.SUPPORT.value, "Soporte")
    ensure_role(db, RoleEnum.SUPERADMIN.value, "Super administrador")


def seed_specialties(db) -> dict[str, Specialty]:
    result: dict[str, Specialty] = {}
    for name, description in SPECIALTIES:
        result[name] = ensure_specialty(db, name, description)
    return result


def seed_clients(db) -> list[User]:
    users: list[User] = []
    for item in CLIENTS:
        user = ensure_user(db, **item, is_verified=True)
        ensure_user_role(db, user.ci, RoleEnum.CLIENT.value)
        users.append(user)
    return users


def seed_professionals(db, specialties_by_name: dict[str, Specialty]) -> list[ProfessionalProfile]:
    profiles: list[ProfessionalProfile] = []

    for item in PROFESSIONALS:
        user_data = {
            "ci": item["ci"],
            "first_name": item["first_name"],
            "last_name": item["last_name"],
            "mother_last_name": item["mother_last_name"],
            "birth_date": item["birth_date"],
            "email": item["email"],
            "phone": item["phone"],
            "city": item["city"],
            "zone": item["zone"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
        }

        user = ensure_user(db, **user_data, is_verified=True)
        ensure_user_role(db, user.ci, RoleEnum.PROFESSIONAL.value)

        profile = ensure_professional_profile(
            db,
            user_ci=user.ci,
            bio=item["bio"],
            experience_years=item["experience_years"],
            is_available=item["is_available"],
            verification_status=VerificationStatusEnum.APPROVED,
        )

        for specialty_name in item["specialties"]:
            ensure_professional_specialty(db, profile.id, specialties_by_name[specialty_name].id)

        ensure_availability(db, profile.id, 1, time(8, 0), time(12, 0))
        ensure_availability(db, profile.id, 3, time(14, 0), time(18, 0))
        ensure_availability(db, profile.id, 5, time(9, 0), time(13, 0))

        profiles.append(profile)

    return profiles


def seed_requests(
    db,
    clients: list[User],
    specialties_by_name: dict[str, Specialty],
) -> list[Request]:
    requests: list[Request] = []
    now = datetime.now(UTC)

    request_plan = [
        ("Electricista", 0),
        ("Plomería", 1),
        ("Pintura", 2),
        ("Carpintería", 3),
        ("Cerrajería", 4),
        ("Jardinería", 5),
        ("Albañilería", 6),
        ("Limpieza", 7),
        ("Gasfitería", 8),
        ("Técnico de electrodomésticos", 9),
        ("Soldadura", 0),
        ("Yesero", 1),
        ("Electricista", 2),
        ("Plomería", 3),
        ("Carpintería", 4),
    ]

    for idx, (specialty_name, client_idx) in enumerate(request_plan):
        title, description = REQUEST_TEMPLATES[idx]
        client = clients[client_idx]
        specialty = specialties_by_name[specialty_name]

        request = ensure_request(
            db,
            client_ci=client.ci,
            specialty_id=specialty.id,
            title=title,
            description=description,
            city=client.city,
            zone=client.zone,
            latitude=client.latitude,
            longitude=client.longitude,
            budget=random_decimal(120, 1500),
            urgency=random.choice(
                [UrgencyLevelEnum.LOW, UrgencyLevelEnum.MEDIUM, UrgencyLevelEnum.HIGH]
            ),
            scheduled_date=now + timedelta(days=idx + 1),
        )
        requests.append(request)

    return requests


def seed_applications_and_state_flow(
    db,
    requests: list[Request],
    profiles: list[ProfessionalProfile],
) -> tuple[list[Application], list[Request]]:
    applications: list[Application] = []

    target_states = {
        6: RequestStatusEnum.ASSIGNED,
        7: RequestStatusEnum.ASSIGNED,
        8: RequestStatusEnum.ASSIGNED,
        9: RequestStatusEnum.IN_PROGRESS,
        10: RequestStatusEnum.IN_PROGRESS,
        11: RequestStatusEnum.IN_PROGRESS,
        12: RequestStatusEnum.COMPLETED,
        13: RequestStatusEnum.COMPLETED,
        14: RequestStatusEnum.COMPLETED,
    }

    for idx, request in enumerate(requests):
        fresh_request = db.scalar(select(Request).where(Request.id == request.id))

        matching_profiles = db.scalars(
            select(ProfessionalProfile)
            .join(
                ProfessionalSpecialty,
                ProfessionalSpecialty.professional_profile_id == ProfessionalProfile.id,
            )
            .where(ProfessionalSpecialty.specialty_id == fresh_request.specialty_id)
        ).all()

        if not matching_profiles:
            matching_profiles = profiles[:]

        random.shuffle(matching_profiles)
        candidates = matching_profiles[: min(3, len(matching_profiles))]

        for profile in candidates:
            if profile.user_ci == fresh_request.client_ci:
                continue

            app = ensure_application(
                db,
                request_id=fresh_request.id,
                professional_profile_id=profile.id,
                proposal_message=(
                    f"Puedo ayudarte con '{fresh_request.title.lower()}'. "
                    "Tengo experiencia en trabajos similares y disponibilidad esta semana."
                ),
                proposed_price=random_decimal(100, 1600),
                estimated_time_hours=random.randint(2, 12),
            )
            applications.append(app)

        target_status = target_states.get(idx)
        if target_status is None:
            continue

        request_apps = db.scalars(
            select(Application).where(Application.request_id == fresh_request.id)
        ).all()

        if not request_apps:
            continue

        accepted = request_apps[0]
        for item in request_apps:
            item.status = (
                ApplicationStatusEnum.ACCEPTED
                if item.id == accepted.id
                else ApplicationStatusEnum.REJECTED
            )

        fresh_request.assigned_professional_profile_id = accepted.professional_profile_id
        fresh_request.proposed_final_price = accepted.proposed_price

        if target_status == RequestStatusEnum.ASSIGNED:
            fresh_request.status = RequestStatusEnum.ASSIGNED
            fresh_request.is_review_enabled = False
        elif target_status == RequestStatusEnum.IN_PROGRESS:
            fresh_request.status = RequestStatusEnum.IN_PROGRESS
            fresh_request.is_review_enabled = False
        elif target_status == RequestStatusEnum.COMPLETED:
            fresh_request.status = RequestStatusEnum.COMPLETED
            fresh_request.is_review_enabled = True
            accepted.status = ApplicationStatusEnum.COMPLETED

        db.commit()
        db.refresh(fresh_request)

    return applications, requests


def seed_reviews(db) -> list[Review]:
    reviews: list[Review] = []
    comment_idx = 0

    completed_requests = db.scalars(
        select(Request).where(Request.status == RequestStatusEnum.COMPLETED)
    ).all()

    for request in completed_requests:
        accepted_application = db.scalar(
            select(Application).where(
                Application.request_id == request.id,
                Application.status == ApplicationStatusEnum.COMPLETED,
            )
        )
        if not accepted_application:
            continue

        assigned_profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id == accepted_application.professional_profile_id
            )
        )
        if not assigned_profile:
            continue

        review = ensure_review(
            db,
            application_id=accepted_application.id,
            reviewer_ci=request.client_ci,
            reviewed_user_ci=assigned_profile.user_ci,
            rating=random.randint(4, 5),
            comment=REVIEW_COMMENTS[comment_idx % len(REVIEW_COMMENTS)],
        )
        comment_idx += 1
        reviews.append(review)

    recalculate_professional_ratings(db)
    return reviews


def print_summary(db) -> None:
    counts = {
        "roles": db.scalar(select(func.count(Role.id))),
        "users": db.scalar(select(func.count(User.ci))),
        "specialties": db.scalar(select(func.count(Specialty.id))),
        "professional_profiles": db.scalar(select(func.count(ProfessionalProfile.id))),
        "professional_specialties": db.scalar(select(func.count(ProfessionalSpecialty.id))),
        "availabilities": db.scalar(select(func.count(ProfessionalAvailability.id))),
        "requests": db.scalar(select(func.count(Request.id))),
        "applications": db.scalar(select(func.count(Application.id))),
        "reviews": db.scalar(select(func.count(Review.id))),
    }

    print("\nSeed demo completado:")
    for key, value in counts.items():
        print(f"- {key}: {value}")


def run_seed_demo() -> None:
    random.seed(RANDOM_SEED)
    db = SessionLocal()

    try:
        print("Iniciando seed demo...")
        seed_roles(db)
        specialties_by_name = seed_specialties(db)
        clients = seed_clients(db)
        profiles = seed_professionals(db, specialties_by_name)
        requests = seed_requests(db, clients, specialties_by_name)
        seed_applications_and_state_flow(db, requests, profiles)
        seed_reviews(db)
        print_summary(db)
        print(f"\nContraseña por defecto para usuarios demo: {DEFAULT_PASSWORD}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed_demo()