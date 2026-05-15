# app/repositories/service_request_repository.py
from sqlalchemy.orm import Session

from app.models.service_request import ServiceRequest


class ServiceRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_items(self):
        return (
            self.db.query(ServiceRequest)
            .order_by(ServiceRequest.created_at.desc())
            .all()
        )

    def list_by_client_user_id(self, client_user_id):
        return (
            self.db.query(ServiceRequest)
            .filter(ServiceRequest.client_user_id == client_user_id)
            .order_by(ServiceRequest.created_at.desc())
            .all()
        )

    def get_by_id(self, item_id):
        return self.db.query(ServiceRequest).filter(ServiceRequest.id == item_id).first()

    def create(self, item: ServiceRequest):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item: ServiceRequest):
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ServiceRequest):
        self.db.delete(item)
        self.db.commit()