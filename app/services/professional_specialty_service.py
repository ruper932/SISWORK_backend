# app/services/professional_specialty_service.py
from fastapi import HTTPException, status

from app.models.enums import SpecialtyLevel
from app.models.professional_specialty import ProfessionalSpecialty
from app.repositories.professional_profile_repository import ProfessionalProfileRepository
from app.repositories.professional_specialty_repository import ProfessionalSpecialtyRepository
from app.repositories.specialty_repository import SpecialtyRepository
from app.schemas.professional_specialty import (
    ProfessionalSpecialtyCreateRequest,
    ProfessionalSpecialtyUpdateRequest,
)


class ProfessionalSpecialtyService:
    def __init__(self, db):
        self.repo = ProfessionalSpecialtyRepository(db)
        self.profile_repo = ProfessionalProfileRepository(db)
        self.specialty_repo = SpecialtyRepository(db)

    def list_items(self):
        items = self.repo.list_items()

        return [
            {
                "id": item.id,
                "professional_profile_id": item.professional_profile_id,
                "specialty_id": item.specialty_id,
                "level": item.level.value,
                "years_experience": item.years_experience,
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
                "specialty_id": item.specialty_id,
                "level": item.level.value,
                "years_experience": item.years_experience,
                "created_at": item.created_at,
            }
            for item in items
        ]

    def get_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional specialty not found",
            )

        return {
            "id": item.id,
            "professional_profile_id": item.professional_profile_id,
            "specialty_id": item.specialty_id,
            "level": item.level.value,
            "years_experience": item.years_experience,
            "created_at": item.created_at,
        }

    def create_item(self, payload: ProfessionalSpecialtyCreateRequest):
        profile = self.profile_repo.get_by_id(payload.professional_profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        specialty = self.specialty_repo.get_by_id(payload.specialty_id)
        if not specialty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specialty not found",
            )

        existing = self.repo.get_by_profile_and_specialty(
            payload.professional_profile_id,
            payload.specialty_id,
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This specialty is already assigned to the professional profile",
            )

        if payload.years_experience < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="years_experience must be greater than or equal to 0",
            )

        item = ProfessionalSpecialty(
            professional_profile_id=payload.professional_profile_id,
            specialty_id=payload.specialty_id,
            level=SpecialtyLevel(payload.level),
            years_experience=payload.years_experience,
        )

        created = self.repo.create(item)

        return {
            "id": created.id,
            "professional_profile_id": created.professional_profile_id,
            "specialty_id": created.specialty_id,
            "level": created.level.value,
            "years_experience": created.years_experience,
            "created_at": created.created_at,
        }

    def update_item(self, item_id, payload: ProfessionalSpecialtyUpdateRequest):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional specialty not found",
            )

        data = payload.model_dump(exclude_unset=True)

        if "years_experience" in data and data["years_experience"] < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="years_experience must be greater than or equal to 0",
            )

        if "level" in data:
            item.level = SpecialtyLevel(data["level"])
        if "years_experience" in data:
            item.years_experience = data["years_experience"]

        updated = self.repo.save(item)

        return {
            "id": updated.id,
            "professional_profile_id": updated.professional_profile_id,
            "specialty_id": updated.specialty_id,
            "level": updated.level.value,
            "years_experience": updated.years_experience,
            "created_at": updated.created_at,
        }

    def delete_item(self, item_id):
        item = self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional specialty not found",
            )

        self.repo.delete(item)
        return {"message": "Professional specialty deleted successfully"}