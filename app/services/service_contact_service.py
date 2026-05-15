from fastapi import HTTPException

from app.models.enums import ContactChannel
from app.models.service_contact import ServiceContact
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.service_contact_repository import ServiceContactRepository
from app.repositories.service_request_repository import ServiceRequestRepository
from app.repositories.user_repository import UserRepository
from app.schemas.service_contact import ServiceContactCreateRequest, ServiceContactUpdateRequest


class ServiceContactService:
    def __init__(self, db):
        self.repo = ServiceContactRepository(db)
        self.user_repo = UserRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)
        self.service_request_repo = ServiceRequestRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "service_request_id": item.service_request_id,
            "client_user_id": item.client_user_id,
            "professional_profile_id": item.professional_profile_id,
            "channel": item.channel.value,
            "contacted_at": item.contacted_at,
            "note": item.note,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service contact not found")
        return self._serialize(item)

    def create_item(self, payload: ServiceContactCreateRequest):
        if payload.service_request_id and not self.service_request_repo.get_by_id(payload.service_request_id):
            raise HTTPException(status_code=404, detail="Service request not found")
        if not self.user_repo.get_by_id(payload.client_user_id):
            raise HTTPException(status_code=404, detail="Client user not found")
        if not self.profile_repo.get_by_id(payload.professional_profile_id):
            raise HTTPException(status_code=404, detail="Professional profile not found")

        item = ServiceContact(
            service_request_id=payload.service_request_id,
            client_user_id=payload.client_user_id,
            professional_profile_id=payload.professional_profile_id,
            channel=ContactChannel(payload.channel),
            note=payload.note,
        )
        return self._serialize(self.repo.create(item))

    def update_item(self, item_id, payload: ServiceContactUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service contact not found")

        data = payload.model_dump(exclude_unset=True)
        if "channel" in data:
            item.channel = ContactChannel(data["channel"])
        if "note" in data:
            item.note = data["note"]

        return self._serialize(self.repo.save(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service contact not found")
        self.repo.delete(item)
        return {"message": "Service contact deleted successfully"}