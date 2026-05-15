from fastapi import HTTPException

from app.models.user_address import UserAddress
from app.repositories.user_address_repository import UserAddressRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_address import UserAddressCreateRequest, UserAddressUpdateRequest


class UserAddressService:
    def __init__(self, db):
        self.repo = UserAddressRepository(db)
        self.user_repo = UserRepository(db)

    def _serialize(self, item):
        return {
            "id": item.id,
            "user_id": item.user_id,
            "department": item.department,
            "city": item.city,
            "zone": item.zone,
            "address": item.address,
            "reference": item.reference,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "is_primary": item.is_primary,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    def list_items(self):
        return [self._serialize(i) for i in self.repo.list_items()]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="User address not found")
        return self._serialize(item)

    def create_item(self, payload: UserAddressCreateRequest):
        if not self.user_repo.get_by_id(payload.user_id):
            raise HTTPException(status_code=404, detail="User not found")

        if payload.is_primary:
            current_primary = self.repo.get_primary_by_user_id(payload.user_id)
            if current_primary:
                current_primary.is_primary = False
                self.repo.save(current_primary)

        item = UserAddress(**payload.model_dump())
        return self._serialize(self.repo.create(item))

    def update_item(self, item_id, payload: UserAddressUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="User address not found")

        data = payload.model_dump(exclude_unset=True)

        if "is_primary" in data and data["is_primary"] is True:
            current_primary = self.repo.get_primary_by_user_id(item.user_id)
            if current_primary and str(current_primary.id) != str(item.id):
                current_primary.is_primary = False
                self.repo.save(current_primary)

        for key, value in data.items():
            setattr(item, key, value)

        return self._serialize(self.repo.save(item))

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="User address not found")
        self.repo.delete(item)
        return {"message": "User address deleted successfully"}