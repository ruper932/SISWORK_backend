from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.specialty_repository import SpecialtyRepository


class SpecialtyService:
    @staticmethod
    def list_active_specialties(db: Session):
        return SpecialtyRepository.list_active(db)