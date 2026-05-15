# app/services/professional_availability_service.py
from fastapi import HTTPException, status

from app.models.enums import Weekday
from app.models.professional_availability import ProfessionalAvailability
from app.repositories.professional_availability_repository import ProfessionalAvailabilityRepository
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.schemas.professional_availability import (
    ProfessionalAvailabilityCreateRequest,
    ProfessionalAvailabilityUpdateRequest,
)


class ProfessionalAvailabilityService:
    def __init__(self, db):
        self.repo = ProfessionalAvailabilityRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)

    def list_items(self):
        items = self.repo.list_items()

        return [
            {
                "id": item.id,
                "professional_profile_id": item.professional_profile_id,
                "weekday": item.weekday.value,
                "start_time": item.start_time,
                "end_time": item.end_time,
                "is_available": item.is_available,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]

    def list_by_profile_id(self, profile_id):
        items = self.repo.list_by_profile_id(profile_id)

        return [
            {
                "id": item.id,
                "professional_profile_id": item.professional_profile_id,
                "weekday": item.weekday.value,
                "start_time": item.start_time,
                "end_time": item.end_time,
                "is_available": item.is_available,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional availability not found",
            )

        return {
            "id": item.id,
            "professional_profile_id": item.professional_profile_id,
            "weekday": item.weekday.value,
            "start_time": item.start_time,
            "end_time": item.end_time,
            "is_available": item.is_available,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    def create_item(self, payload: ProfessionalAvailabilityCreateRequest):
        profile = self.profile_repo.get_by_id(payload.professional_profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        if payload.start_time >= payload.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_time must be less than end_time",
            )

        weekday = Weekday(payload.weekday)

        existing = self.repo.get_by_unique_fields(
            payload.professional_profile_id,
            weekday,
            payload.start_time,
            payload.end_time,
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This availability already exists for the professional profile",
            )

        item = ProfessionalAvailability(
            professional_profile_id=payload.professional_profile_id,
            weekday=weekday,
            start_time=payload.start_time,
            end_time=payload.end_time,
            is_available=payload.is_available,
        )

        created = self.repo.create(item)

        return {
            "id": created.id,
            "professional_profile_id": created.professional_profile_id,
            "weekday": created.weekday.value,
            "start_time": created.start_time,
            "end_time": created.end_time,
            "is_available": created.is_available,
            "created_at": created.created_at,
            "updated_at": created.updated_at,
        }

    def update_item(self, item_id, payload: ProfessionalAvailabilityUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional availability not found",
            )

        data = payload.model_dump(exclude_unset=True)

        next_weekday = Weekday(data["weekday"]) if "weekday" in data else item.weekday
        next_start_time = data.get("start_time", item.start_time)
        next_end_time = data.get("end_time", item.end_time)

        if next_start_time >= next_end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_time must be less than end_time",
            )

        existing = self.repo.get_by_unique_fields(
            item.professional_profile_id,
            next_weekday,
            next_start_time,
            next_end_time,
        )
        if existing and str(existing.id) != str(item.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This availability already exists for the professional profile",
            )

        if "weekday" in data:
            item.weekday = Weekday(data["weekday"])
        if "start_time" in data:
            item.start_time = data["start_time"]
        if "end_time" in data:
            item.end_time = data["end_time"]
        if "is_available" in data:
            item.is_available = data["is_available"]

        updated = self.repo.save(item)

        return {
            "id": updated.id,
            "professional_profile_id": updated.professional_profile_id,
            "weekday": updated.weekday.value,
            "start_time": updated.start_time,
            "end_time": updated.end_time,
            "is_available": updated.is_available,
            "created_at": updated.created_at,
            "updated_at": updated.updated_at,
        }

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional availability not found",
            )

        self.repo.delete(item)
        return {"message": "Professional availability deleted successfully"}