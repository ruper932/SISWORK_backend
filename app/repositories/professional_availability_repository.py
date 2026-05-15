# app/repositories/professional_availability_repository.py
from sqlalchemy.orm import Session

from app.models.professional_availability import ProfessionalAvailability


class ProfessionalAvailabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return (
            self.db.query(ProfessionalAvailability)
            .order_by(
                ProfessionalAvailability.weekday.asc(),
                ProfessionalAvailability.start_time.asc(),
            )
            .all()
        )

    def list_by_profile_id(self, profile_id):
        return (
            self.db.query(ProfessionalAvailability)
            .filter(ProfessionalAvailability.professional_profile_id == profile_id)
            .order_by(
                ProfessionalAvailability.weekday.asc(),
                ProfessionalAvailability.start_time.asc(),
            )
            .all()
        )

    def get_by_id(self, item_id):
        return self.db.query(ProfessionalAvailability).filter(ProfessionalAvailability.id == item_id).first()

    def get_by_unique_fields(self, profile_id, weekday, start_time, end_time):
        return (
            self.db.query(ProfessionalAvailability)
            .filter(
                ProfessionalAvailability.professional_profile_id == profile_id,
                ProfessionalAvailability.weekday == weekday,
                ProfessionalAvailability.start_time == start_time,
                ProfessionalAvailability.end_time == end_time,
            )
            .first()
        )

    def create(self, item: ProfessionalAvailability):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item: ProfessionalAvailability):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ProfessionalAvailability):
        self.db.delete(item)
        self.db.commit()