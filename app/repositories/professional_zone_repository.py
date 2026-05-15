# app/repositories/professional_zone_repository.py
from sqlalchemy.orm import Session

from app.models.professional_zone import ProfessionalZone


class ProfessionalZoneRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return (
            self.db.query(ProfessionalZone)
            .order_by(ProfessionalZone.created_at.desc())
            .all()
        )

    def list_by_profile_id(self, profile_id):
        return (
            self.db.query(ProfessionalZone)
            .filter(ProfessionalZone.professional_profile_id == profile_id)
            .order_by(ProfessionalZone.created_at.desc())
            .all()
        )

    def get_by_id(self, item_id):
        return self.db.query(ProfessionalZone).filter(ProfessionalZone.id == item_id).first()

    def get_by_unique_fields(self, profile_id, department, city, zone):
        return (
            self.db.query(ProfessionalZone)
            .filter(
                ProfessionalZone.professional_profile_id == profile_id,
                ProfessionalZone.department == department,
                ProfessionalZone.city == city,
                ProfessionalZone.zone == zone,
            )
            .first()
        )

    def create(self, item: ProfessionalZone):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item: ProfessionalZone):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ProfessionalZone):
        self.db.delete(item)
        self.db.commit()