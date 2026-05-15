from sqlalchemy.orm import Session

from app.models.service_contact import ServiceContact


class ServiceContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return self.db.query(ServiceContact).order_by(ServiceContact.contacted_at.desc()).all()

    def list_by_client_user_id(self, client_user_id):
        return self.db.query(ServiceContact).filter(ServiceContact.client_user_id == client_user_id).all()

    def list_by_professional_profile_id(self, professional_profile_id):
        return self.db.query(ServiceContact).filter(ServiceContact.professional_profile_id == professional_profile_id).all()

    def list_by_service_request_id(self, service_request_id):
        return self.db.query(ServiceContact).filter(ServiceContact.service_request_id == service_request_id).all()

    def get_by_id(self, item_id):
        return self.db.query(ServiceContact).filter(ServiceContact.id == item_id).first()

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