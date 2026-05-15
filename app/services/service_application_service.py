from datetime import datetime
from fastapi import HTTPException, status

from app.models.enums import ApplicationStatus
from app.models.service_application import ServiceApplication
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.service_application_repository import ServiceApplicationRepository
from app.repositories.service_request_repository import ServiceRequestRepository
from app.schemas.service_application import ServiceApplicationCreateRequest, ServiceApplicationUpdateRequest


class ServiceApplicationService:
    def __init__(self, db):
        self.repo = ServiceApplicationRepository(db)
        self.service_request_repo = ServiceRequestRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "service_request_id": item.service_request_id,
            "professional_profile_id": item.professional_profile_id,
            "proposal_message": item.proposal_message,
            "estimated_price": item.estimated_price,
            "status": item.status.value,
            "applied_at": item.applied_at,
            "responded_at": item.responded_at,
            "cancelled_at": item.cancelled_at,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service application not found")
        return self._serialize(item)

    def create_item(self, payload: ServiceApplicationCreateRequest):
        if payload.estimated_price is not None and payload.estimated_price < 0:
            raise HTTPException(status_code=400, detail="estimated_price must be greater than or equal to 0")

        if not self.service_request_repo.get_by_id(payload.service_request_id):
            raise HTTPException(status_code=404, detail="Service request not found")

        if not self.profile_repo.get_by_id(payload.professional_profile_id):
            raise HTTPException(status_code=404, detail="Professional profile not found")

        existing = self.repo.get_by_unique_fields(payload.service_request_id, payload.professional_profile_id)
        if existing:
            raise HTTPException(status_code=409, detail="This application already exists")

        item = ServiceApplication(
            service_request_id=payload.service_request_id,
            professional_profile_id=payload.professional_profile_id,
            proposal_message=payload.proposal_message,
            estimated_price=payload.estimated_price,
            status=ApplicationStatus.PENDING,
        )
        return self._serialize(self.repo.create(item))

    def update_item(self, item_id, payload: ServiceApplicationUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service application not found")

        data = payload.model_dump(exclude_unset=True)

        if "estimated_price" in data and data["estimated_price"] is not None and data["estimated_price"] < 0:
            raise HTTPException(status_code=400, detail="estimated_price must be greater than or equal to 0")

        if "proposal_message" in data:
            item.proposal_message = data["proposal_message"]
        if "estimated_price" in data:
            item.estimated_price = data["estimated_price"]
        if "status" in data:
            item.status = ApplicationStatus(data["status"])
            if data["status"] in {ApplicationStatus.ACCEPTED.value, ApplicationStatus.REJECTED.value} and item.responded_at is None:
                item.responded_at = datetime.utcnow()
        if "responded_at" in data:
            item.responded_at = data["responded_at"]
        if "cancelled_at" in data:
            item.cancelled_at = data["cancelled_at"]

        return self._serialize(self.repo.save(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service application not found")
        self.repo.delete(item)
        return {"message": "Service application deleted successfully"}