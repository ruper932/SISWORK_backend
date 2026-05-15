# app/api/v1/specialties.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.specialty import (
    SpecialtyCreateRequest,
    SpecialtyCreateResponse,
    SpecialtyDetailResponse,
    SpecialtyListItemResponse,
    SpecialtyUpdateRequest,
)
from app.services.specialty_service import SpecialtyService


router = APIRouter(prefix="/specialties", tags=["Specialties"])


@router.get("", response_model=list[SpecialtyListItemResponse])
def list_specialties(db: Session = Depends(get_db)):
    service = SpecialtyService(db)
    return service.list_specialties()


@router.get("/{specialty_id}", response_model=SpecialtyDetailResponse)
def get_specialty(specialty_id: str, db: Session = Depends(get_db)):
    service = SpecialtyService(db)
    return service.get_specialty(specialty_id)


@router.post("", response_model=SpecialtyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_specialty(payload: SpecialtyCreateRequest, db: Session = Depends(get_db)):
    service = SpecialtyService(db)
    return service.create_specialty(payload)


@router.patch("/{specialty_id}", response_model=SpecialtyDetailResponse)
def update_specialty(
    specialty_id: str,
    payload: SpecialtyUpdateRequest,
    db: Session = Depends(get_db),
):
    service = SpecialtyService(db)
    return service.update_specialty(specialty_id, payload)


@router.delete("/{specialty_id}")
def delete_specialty(specialty_id: str, db: Session = Depends(get_db)):
    service = SpecialtyService(db)
    return service.delete_specialty(specialty_id)