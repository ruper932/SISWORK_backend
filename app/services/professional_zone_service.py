# app/services/professional_zone_service.py
from fastapi import HTTPException, status

from app.models.professional_zone import ProfessionalZone
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.professional_zone_repository import ProfessionalZoneRepository
from app.schemas.professional_zone import (
    ProfessionalZoneCreateRequest,
    ProfessionalZoneUpdateRequest,
)


class ProfessionalZoneService:
    def __init__(self, db):
        self.repo = ProfessionalZoneRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)

    def list_items(self):
        items = self.repo.list_items()

        return [
            {
                "id": item.id,
                "professional_profile_id": item.professional_profile_id,
                "department": item.department,
                "city": item.city,
                "zone": item.zone,
                "created_at": item.created_at,
            }
            for item in items
        ]

    def list_by_profile_id(self, profile_id):
        items = self.repo.list_by_profile_id(profile_id)

        return [
            {
                "id": item.id,
                "professional_profile_id": item.professional_profile_id,
                "department": item.department,
                "city": item.city,
                "zone": item.zone,
                "created_at": item.created_at,
            }
            for item in items
        ]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional zone not found",
            )

        return {
            "id": item.id,
            "professional_profile_id": item.professional_profile_id,
            "department": item.department,
            "city": item.city,
            "zone": item.zone,
            "created_at": item.created_at,
        }

    def create_item(self, payload: ProfessionalZoneCreateRequest):
        profile = self.profile_repo.get_by_id(payload.professional_profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        existing = self.repo.get_by_unique_fields(
            payload.professional_profile_id,
            payload.department,
            payload.city,
            payload.zone,
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This zone is already assigned to the professional profile",
            )

        item = ProfessionalZone(
            professional_profile_id=payload.professional_profile_id,
            department=payload.department,
            city=payload.city,
            zone=payload.zone,
        )

        created = self.repo.create(item)

        return {
            "id": created.id,
            "professional_profile_id": created.professional_profile_id,
            "department": created.department,
            "city": created.city,
            "zone": created.zone,
            "created_at": created.created_at,
        }

    def update_item(self, item_id, payload: ProfessionalZoneUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional zone not found",
            )

        data = payload.model_dump(exclude_unset=True)

        next_department = data.get("department", item.department)
        next_city = data.get("city", item.city)
        next_zone = data.get("zone", item.zone)

        existing = self.repo.get_by_unique_fields(
            item.professional_profile_id,
            next_department,
            next_city,
            next_zone,
        )
        if existing and str(existing.id) != str(item.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This zone is already assigned to the professional profile",
            )

        if "department" in data:
            item.department = data["department"]
        if "city" in data:
            item.city = data["city"]
        if "zone" in data:
            item.zone = data["zone"]

        updated = self.repo.save(item)

        return {
            "id": updated.id,
            "professional_profile_id": updated.professional_profile_id,
            "department": updated.department,
            "city": updated.city,
            "zone": updated.zone,
            "created_at": updated.created_at,
        }

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional zone not found",
            )

        self.repo.delete(item)
        return {"message": "Professional zone deleted successfully"}