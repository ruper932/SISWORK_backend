from sqlalchemy.orm import Session

from app.models.professional_validation_queue import ProfessionalValidationQueue


class ProfessionalValidationQueueRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(ProfessionalValidationQueue).order_by(ProfessionalValidationQueue.submitted_at.desc()).all()

    def get_by_id(self, item_id):
        return self.db.query(ProfessionalValidationQueue).filter(ProfessionalValidationQueue.id == item_id).first()

    def get_by_profile_id(self, professional_profile_id):
        return self.db.query(ProfessionalValidationQueue).filter(
            ProfessionalValidationQueue.professional_profile_id == professional_profile_id
        ).first()

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item):
        self.db.delete(item)
        self.db.commit()