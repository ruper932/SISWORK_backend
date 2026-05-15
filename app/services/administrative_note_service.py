from fastapi import HTTPException

from app.models.administrative_note import AdministrativeNote
from app.repositories.administrative_note_repository import AdministrativeNoteRepository
from app.repositories.user_repository import UserRepository
from app.schemas.administrative_note import AdministrativeNoteCreateRequest, AdministrativeNoteUpdateRequest


class AdministrativeNoteService:
    def __init__(self, db):
        self.repo = AdministrativeNoteRepository(db)
        self.user_repo = UserRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "author_user_id": item.author_user_id,
            "related_entity": item.related_entity,
            "related_entity_id": item.related_entity_id,
            "note": item.note,
            "is_private": item.is_private,
            "created_at": item.created_at,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Administrative note not found")
        return self._serialize(item)

    def create_item(self, payload: AdministrativeNoteCreateRequest):
        if not self.user_repo.get_by_id(payload.author_user_id):
            raise HTTPException(status_code=404, detail="Author user not found")

        item = AdministrativeNote(**payload.model_dump())
        return self._serialize(self.repo.create(item))

    def update_item(self, item_id, payload: AdministrativeNoteUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Administrative note not found")

        data = payload.model_dump(exclude_unset=True)
        if "note" in data:
            item.note = data["note"]
        if "is_private" in data:
            item.is_private = data["is_private"]

        return self._serialize(self.repo.save(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Administrative note not found")
        self.repo.delete(item)
        return {"message": "Administrative note deleted successfully"}