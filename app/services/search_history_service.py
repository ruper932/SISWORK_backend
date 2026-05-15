from fastapi import HTTPException

from app.models.search_history import SearchHistory
from app.repositories.search_history_repository import SearchHistoryRepository
from app.repositories.specialty_repository import SpecialtyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.search_history import SearchHistoryCreateRequest


class SearchHistoryService:
    def __init__(self, db):
        self.repo = SearchHistoryRepository(db)
        self.user_repo = UserRepository(db)
        self.specialty_repo = SpecialtyRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "user_id": item.user_id,
            "search_term": item.search_term,
            "specialty_id": item.specialty_id,
            "zone": item.zone,
            "minimum_rating": item.minimum_rating,
            "available_now": item.available_now,
            "results_count": item.results_count,
            "searched_at": item.searched_at,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Search history not found")
        return self._serialize(item)

    def create_item(self, payload: SearchHistoryCreateRequest):
        if payload.user_id is not None and not self.user_repo.get_by_id(payload.user_id):
            raise HTTPException(status_code=404, detail="User not found")
        if payload.specialty_id is not None and not self.specialty_repo.get_by_id(payload.specialty_id):
            raise HTTPException(status_code=404, detail="Specialty not found")
        if payload.minimum_rating is not None and (payload.minimum_rating < 0 or payload.minimum_rating > 5):
            raise HTTPException(status_code=400, detail="minimum_rating must be between 0 and 5")

        item = SearchHistory(**payload.model_dump())
        return self._serialize(self.repo.create(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Search history not found")
        self.repo.delete(item)
        return {"message": "Search history deleted successfully"}