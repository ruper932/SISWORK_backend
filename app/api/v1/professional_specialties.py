# app/api/v1/professional_specialties.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.professional_specialty import (
    ProfessionalSpecialtyCreateRequest,
    ProfessionalSpecialtyCreateResponse,
    ProfessionalSpecialtyDetailResponse,
    ProfessionalSpecialtyListItemResponse,
    ProfessionalSpecialtyUpdateRequest,
)
from app.services.professional_specialty_service import ProfessionalSpecialtyService


router = APIRouter(prefix="/professional-specialties", tags=["Professional Specialties"])


@router.get("", response_model=list[ProfessionalSpecialtyListItemResponse])
def list_items(db: Session = Depends(get_db)):
    service = ProfessionalSpecialtyService(db)
    return service.list_items()


@router.get("/profile/{profile_id}", response_model=list[ProfessionalSpecialtyListItemResponse])
def list_by_profile_id(profile_id: str, db: Session = Depends(get_db)):
    service = ProfessionalSpecialtyService(db)
    return service.list_by_profile_id(profile_id)


@router.get("/{item_id}", response_model=ProfessionalSpecialtyDetailResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    service = ProfessionalSpecialtyService(db)
    return service.get_item(item_id)


@router.post("", response_model=ProfessionalSpecialtyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ProfessionalSpecialtyCreateRequest, db: Session = Depends(get_db)):
    service = ProfessionalSpecialtyService(db)
    return service.create_item(payload)


@router.patch("/{item_id}", response_model=ProfessionalSpecialtyDetailResponse)
def update_item(item_id: str, payload: ProfessionalSpecialtyUpdateRequest, db: Session = Depends(get_db)):
    service = ProfessionalSpecialtyService(db)
    return service.update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    service = ProfessionalSpecialtyService(db)
    return service.delete_item(item_id)