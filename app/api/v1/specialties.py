from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.specialty import SpecialtyResponse
from app.services.specialty_service import SpecialtyService


router = APIRouter(
    prefix="/specialties",
    tags=["Specialties"],
)


@router.get(
    "",
    response_model=List[SpecialtyResponse],
)
def list_specialties(
    db: Session = Depends(get_db),
):
    return SpecialtyService.list_active_specialties(db)