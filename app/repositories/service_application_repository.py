from sqlalchemy.orm import Session

from app.models.service_application import ServiceApplication


class ServiceApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(ServiceApplication).order_by(ServiceApplication.applied_at.desc()).all()

    def list_by_service_request_id(self, service_request_id):
        return self.db.query(ServiceApplication).filter(ServiceApplication.service_request_id == service_request_id).all()

    def list_by_professional_profile_id(self, professional_profile_id):
        return self.db.query(ServiceApplication).filter(ServiceApplication.professional_profile_id == professional_profile_id).all()

    def get_by_id(self, item_id):
        return self.db.query(ServiceApplication).filter(ServiceApplication.id == item_id).first()

    def get_by_unique_fields(self, service_request_id, professional_profile_id):
        return self.db.query(ServiceApplication).filter(
            ServiceApplication.service_request_id == service_request_id,
            ServiceApplication.professional_profile_id == professional_profile_id,
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