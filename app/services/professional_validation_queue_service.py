from fastapi import HTTPException

from app.models.enums import VerificationStatus
from app.models.professional_validation_queue import ProfessionalValidationQueue
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.professional_validation_queue_repository import ProfessionalValidationQueueRepository
from app.repositories.user_repository import UserRepository
from app.schemas.professional_validation_queue import (
    ProfessionalValidationQueueCreateRequest,
    ProfessionalValidationQueueUpdateRequest,
)


class ProfessionalValidationQueueService:
    def __init__(self, db):
        self.repo = ProfessionalValidationQueueRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)
        self.user_repo = UserRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "professional_profile_id": item.professional_profile_id,
            "requested_by_user_id": item.requested_by_user_id,
            "assigned_support_user_id": item.assigned_support_user_id,
            "status": item.status.value,
            "submitted_at": item.submitted_at,
            "review_started_at": item.review_started_at,
            "resolved_at": item.resolved_at,
            "rejection_reason": item.rejection_reason,
            "waiting_time_minutes": item.waiting_time_minutes,
            "review_time_minutes": item.review_time_minutes,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Professional validation queue item not found")
        return self._serialize(item)

    def create_item(self, payload: ProfessionalValidationQueueCreateRequest):
        if not self.profile_repo.get_by_id(payload.professional_profile_id):
            raise HTTPException(status_code=404, detail="Professional profile not found")
        if not self.user_repo.get_by_id(payload.requested_by_user_id):
            raise HTTPException(status_code=404, detail="Requested by user not found")
        if payload.assigned_support_user_id and not self.user_repo.get_by_id(payload.assigned_support_user_id):
            raise HTTPException(status_code=404, detail="Assigned support user not found")
        if self.repo.get_by_profile_id(payload.professional_profile_id):
            raise HTTPException(status_code=409, detail="This profile is already in validation queue")

        item = ProfessionalValidationQueue(
            professional_profile_id=payload.professional_profile_id,
            requested_by_user_id=payload.requested_by_user_id,
            assigned_support_user_id=payload.assigned_support_user_id,
            status=VerificationStatus.PENDING,
        )
        return self._serialize(self.repo.create(item))

    def update_item(self, item_id, payload: ProfessionalValidationQueueUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Professional validation queue item not found")

        data = payload.model_dump(exclude_unset=True)

        if "assigned_support_user_id" in data and data["assigned_support_user_id"] is not None:
            if not self.user_repo.get_by_id(data["assigned_support_user_id"]):
                raise HTTPException(status_code=404, detail="Assigned support user not found")

        for key in ["waiting_time_minutes", "review_time_minutes"]:
            if key in data and data[key] is not None and data[key] < 0:
                raise HTTPException(status_code=400, detail=f"{key} must be greater than or equal to 0")

        if "assigned_support_user_id" in data:
            item.assigned_support_user_id = data["assigned_support_user_id"]
        if "status" in data:
            item.status = VerificationStatus(data["status"])
        if "review_started_at" in data:
            item.review_started_at = data["review_started_at"]
        if "resolved_at" in data:
            item.resolved_at = data["resolved_at"]
        if "rejection_reason" in data:
            item.rejection_reason = data["rejection_reason"]
        if "waiting_time_minutes" in data:
            item.waiting_time_minutes = data["waiting_time_minutes"]
        if "review_time_minutes" in data:
            item.review_time_minutes = data["review_time_minutes"]

        return self._serialize(self.repo.save(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Professional validation queue item not found")
        self.repo.delete(item)
        return {"message": "Professional validation queue item deleted successfully"}