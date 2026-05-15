from fastapi import HTTPException

from app.models.service_rating import ServiceRating
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.service_rating_repository import ServiceRatingRepository
from app.repositories.service_request_repository import ServiceRequestRepository
from app.repositories.user_repository import UserRepository
from app.schemas.service_rating import ServiceRatingCreateRequest, ServiceRatingUpdateRequest


class ServiceRatingService:
    def __init__(self, db):
        self.repo = ServiceRatingRepository(db)
        self.service_request_repo = ServiceRequestRepository(db)
        self.user_repo = UserRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "service_request_id": item.service_request_id,
            "client_user_id": item.client_user_id,
            "professional_profile_id": item.professional_profile_id,
            "score": item.score,
            "comment": item.comment,
            "is_verified": item.is_verified,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service rating not found")
        return self._serialize(item)

    def create_item(self, payload: ServiceRatingCreateRequest):
        if payload.score < 1 or payload.score > 5:
            raise HTTPException(status_code=400, detail="score must be between 1 and 5")
        if not self.service_request_repo.get_by_id(payload.service_request_id):
            raise HTTPException(status_code=404, detail="Service request not found")
        if not self.user_repo.get_by_id(payload.client_user_id):
            raise HTTPException(status_code=404, detail="Client user not found")
        if not self.profile_repo.get_by_id(payload.professional_profile_id):
            raise HTTPException(status_code=404, detail="Professional profile not found")
        if self.repo.get_by_service_request_id(payload.service_request_id):
            raise HTTPException(status_code=409, detail="A rating already exists for this service request")

        item = ServiceRating(
            service_request_id=payload.service_request_id,
            client_user_id=payload.client_user_id,
            professional_profile_id=payload.professional_profile_id,
            score=payload.score,
            comment=payload.comment,
            is_verified=payload.is_verified,
        )
        return self._serialize(self.repo.create(item))

    def update_item(self, item_id, payload: ServiceRatingUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service rating not found")

        data = payload.model_dump(exclude_unset=True)
        if "score" in data and (data["score"] < 1 or data["score"] > 5):
            raise HTTPException(status_code=400, detail="score must be between 1 and 5")

        if "score" in data:
            item.score = data["score"]
        if "comment" in data:
            item.comment = data["comment"]
        if "is_verified" in data:
            item.is_verified = data["is_verified"]

        return self._serialize(self.repo.save(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Service rating not found")
        self.repo.delete(item)
        return {"message": "Service rating deleted successfully"}