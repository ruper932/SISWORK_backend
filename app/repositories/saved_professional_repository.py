from sqlalchemy.orm import Session

from app.models.saved_professional import SavedProfessional


class SavedProfessionalRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(SavedProfessional).order_by(SavedProfessional.created_at.desc()).all()

    def list_by_user_id(self, user_id):
        return self.db.query(SavedProfessional).filter(SavedProfessional.user_id == user_id).all()

    def get_by_id(self, item_id):
        return self.db.query(SavedProfessional).filter(SavedProfessional.id == item_id).first()

    def get_by_unique_fields(self, user_id, professional_profile_id):
        return self.db.query(SavedProfessional).filter(
            SavedProfessional.user_id == user_id,
            SavedProfessional.professional_profile_id == professional_profile_id,
        ).first()

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item):
        self.db.delete(item)
        self.db.commit()