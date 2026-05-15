# app/services/specialty_service.py
from fastapi import HTTPException, status

from app.models.specialty import Specialty
from app.repositories.specialty_repository import SpecialtyRepository
from app.schemas.specialty import SpecialtyCreateRequest, SpecialtyUpdateRequest


class SpecialtyService:
    def __init__(self, db):
        self.repo = SpecialtyRepository(db)

    def list_specialties(self):
        specialties = self.repo.list_specialties()
        return [
            {
                "id": specialty.id,
                "code": specialty.code,
                "name": specialty.name,
                "description": specialty.description,
                "is_active": specialty.is_active,
                "created_at": specialty.created_at,
            }
            for specialty in specialties
        ]

    def get_specialty(self, specialty_id):
        specialty = self.repo.get_by_id(specialty_id)
        if not specialty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specialty not found",
            )

        return {
            "id": specialty.id,
            "code": specialty.code,
            "name": specialty.name,
            "description": specialty.description,
            "is_active": specialty.is_active,
            "created_at": specialty.created_at,
        }

    def create_specialty(self, payload: SpecialtyCreateRequest):
        if self.repo.get_by_code(payload.code):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Specialty code already exists",
            )

        if self.repo.get_by_name(payload.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Specialty name already exists",
            )

        specialty = Specialty(
            code=payload.code,
            name=payload.name,
            description=payload.description,
            is_active=payload.is_active,
        )

        created = self.repo.create(specialty)

        return {
            "id": created.id,
            "code": created.code,
            "name": created.name,
            "description": created.description,
            "is_active": created.is_active,
            "created_at": created.created_at,
        }

    def update_specialty(self, specialty_id, payload: SpecialtyUpdateRequest):
        specialty = self.repo.get_by_id(specialty_id)
        if not specialty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specialty not found",
            )

        data = payload.model_dump(exclude_unset=True)

        if "code" in data and data["code"] != specialty.code:
            if self.repo.get_by_code(data["code"]):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Specialty code already exists",
                )

        if "name" in data and data["name"] != specialty.name:
            if self.repo.get_by_name(data["name"]):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Specialty name already exists",
                )

        if "code" in data:
            specialty.code = data["code"]
        if "name" in data:
            specialty.name = data["name"]
        if "description" in data:
            specialty.description = data["description"]
        if "is_active" in data:
            specialty.is_active = data["is_active"]

        updated = self.repo.save(specialty)

        return {
            "id": updated.id,
            "code": updated.code,
            "name": updated.name,
            "description": updated.description,
            "is_active": updated.is_active,
            "created_at": updated.created_at,
        }

    def delete_specialty(self, specialty_id):
        specialty = self.repo.get_by_id(specialty_id)
        if not specialty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specialty not found",
            )

        self.repo.delete(specialty)
        return {"message": "Specialty deleted successfully"}