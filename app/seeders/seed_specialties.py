from sqlalchemy.orm import Session

from app.models.specialty import Specialty


SPECIALTIES = [
    {"codigo": "plomeria", "nombre": "Plomería", "descripcion": "Servicios de plomería y gasfitería"},
    {"codigo": "electricidad", "nombre": "Electricidad", "descripcion": "Instalaciones y reparaciones eléctricas"},
    {"codigo": "carpinteria", "nombre": "Carpintería", "descripcion": "Trabajos en madera"},
]


def seed_specialties(db: Session) -> None:
    for item in SPECIALTIES:
        exists = db.query(Specialty).filter(Specialty.codigo == item["codigo"]).first()
        if exists:
            continue

        db.add(Specialty(**item))

    db.commit()