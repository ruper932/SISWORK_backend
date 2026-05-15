# app/repositories/specialty_repository.py
from sqlalchemy.orm import Session

from app.models.specialty import Specialty


class SpecialtyRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_specialties(self):
        return self.db.query(Specialty).order_by(Specialty.name.asc()).all()

    def get_by_id(self, specialty_id):
        return self.db.query(Specialty).filter(Specialty.id == specialty_id).first()

    def get_by_code(self, code: str):
        return self.db.query(Specialty).filter(Specialty.code == code).first()

    def get_by_name(self, name: str):
        return self.db.query(Specialty).filter(Specialty.name == name).first()

    def create(self, specialty: Specialty):
        self.db.add(specialty)
        self.db.commit()
        self.db.refresh(specialty)
        return specialty

    def save(self, specialty: Specialty):
        self.db.commit()
        self.db.refresh(specialty)
        return specialty

    def delete(self, specialty: Specialty):
        self.db.delete(specialty)
        self.db.commit()