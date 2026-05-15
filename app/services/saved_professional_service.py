from fastapi import HTTPException

from app.models.saved_professional import SavedProfessional
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.saved_professional_repository import SavedProfessionalRepository
from app.repositories.user_repository import UserRepository
from app.schemas.saved_professional import SavedProfessionalCreateRequest


class SavedProfessionalService:
    def __init__(self, db):
        self.repo = SavedProfessionalRepository(db)
        self.user_repo = UserRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "user_id": item.user_id,
            "professional_profile_id": item.professional_profile_id,
            "created_at": item.created_at,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Saved professional not found")
        return self._serialize(item)

    def create_item(self, payload: SavedProfessionalCreateRequest):
        if not self.user_repo.get_by_id(payload.user_id):
            raise HTTPException(status_code=404, detail="User not found")
        if not self.profile_repo.get_by_id(payload.professional_profile_id):
            raise HTTPException(status_code=404, detail="Professional profile not found")
        if self.repo.get_by_unique_fields(payload.user_id, payload.professional_profile_id):
            raise HTTPException(status_code=409, detail="This professional is already saved by the user")

        item = SavedProfessional(
            user_id=payload.user_id,
            professional_profile_id=payload.professional_profile_id,
        )
        return self._serialize(self.repo.create(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Saved professional not found")
        self.repo.delete(item)
        return {"message": "Saved professional deleted successfully"}