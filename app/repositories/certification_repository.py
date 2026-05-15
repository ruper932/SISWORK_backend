# app/repositories/certification_repository.py
from sqlalchemy.orm import Session

from app.models.certification import Certification


class CertificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return (
            self.db.query(Certification)
            .order_by(Certification.created_at.desc())
            .all()
        )

    def list_by_profile_id(self, profile_id):
        return (
            self.db.query(Certification)
            .filter(Certification.professional_profile_id == profile_id)
            .order_by(Certification.created_at.desc())
            .all()
        )

    def get_by_id(self, item_id):
        return self.db.query(Certification).filter(Certification.id == item_id).first()

    def create(self, item: Certification):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item: Certification):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: Certification):
        self.db.delete(item)
        self.db.commit()