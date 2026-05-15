# app/repositories/professional_specialty_repository.py
from sqlalchemy.orm import Session

from app.models.professional_specialty import ProfessionalSpecialty


class ProfessionalSpecialtyRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return (
            self.db.query(ProfessionalSpecialty)
            .order_by(ProfessionalSpecialty.created_at.desc())
            .all()
        )

    def list_by_profile_id(self, profile_id):
        return (
            self.db.query(ProfessionalSpecialty)
            .filter(ProfessionalSpecialty.professional_profile_id == profile_id)
            .order_by(ProfessionalSpecialty.created_at.desc())
            .all()
        )

    def get_by_id(self, item_id):
        return self.db.query(ProfessionalSpecialty).filter(ProfessionalSpecialty.id == item_id).first()

    def get_by_profile_and_specialty(self, profile_id, specialty_id):
        return (
            self.db.query(ProfessionalSpecialty)
            .filter(
                ProfessionalSpecialty.professional_profile_id == profile_id,
                ProfessionalSpecialty.specialty_id == specialty_id,
            )
            .first()
        )

    def create(self, item: ProfessionalSpecialty):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item: ProfessionalSpecialty):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ProfessionalSpecialty):
        self.db.delete(item)
        self.db.commit()