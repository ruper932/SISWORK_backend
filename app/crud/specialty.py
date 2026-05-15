# app/crud/specialty.py
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.specialty import Specialty
from app.schemas.specialty import SpecialtyCreate, SpecialtyUpdate


def get_specialty(db: Session, specialty_id: UUID) -> Optional[Specialty]:
    return db.scalar(select(Specialty).where(Specialty.id == specialty_id))


def get_specialty_by_code(db: Session, code: str) -> Optional[Specialty]:
    return db.scalar(select(Specialty).where(Specialty.code == code))


def get_specialty_by_name(db: Session, name: str) -> Optional[Specialty]:
    return db.scalar(select(Specialty).where(Specialty.name == name))


def get_specialties(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    only_active: bool = False,
):
    stmt = select(Specialty)

    if only_active:
        stmt = stmt.where(Specialty.isactive.is_(True))

    stmt = stmt.order_by(Specialty.name.asc()).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_specialty(db: Session, payload: SpecialtyCreate) -> Specialty:
    specialty = Specialty(**payload.model_dump())
    db.add(specialty)
    db.commit()
    db.refresh(specialty)
    return specialty


def update_specialty(db: Session, db_obj: Specialty, payload: SpecialtyUpdate) -> Specialty:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_specialty(db: Session, db_obj: Specialty) -> None:
    db.delete(db_obj)
    db.commit()