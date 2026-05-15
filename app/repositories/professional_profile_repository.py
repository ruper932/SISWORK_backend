# app/repositories/professional_profile_repository.py
from sqlalchemy.orm import Session

from app.models.professional_profile import ProfessionalProfile


class ProfessionalProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_profiles(self):
        return self.db.query(ProfessionalProfile).order_by(ProfessionalProfile.created_at.desc()).all()

    def get_by_id(self, profile_id):
        return self.db.query(ProfessionalProfile).filter(ProfessionalProfile.id == profile_id).first()

    def get_by_user_id(self, user_id):
        return self.db.query(ProfessionalProfile).filter(ProfessionalProfile.user_id == user_id).first()

    def create(self, profile: ProfessionalProfile):
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def save(self, profile: ProfessionalProfile):
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete(self, profile: ProfessionalProfile):
        self.db.delete(profile)
        self.db.commit()