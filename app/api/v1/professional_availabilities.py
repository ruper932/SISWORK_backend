# app/api/v1/professional_availabilities.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.professional_availability import (
    ProfessionalAvailabilityCreateRequest,
    ProfessionalAvailabilityCreateResponse,
    ProfessionalAvailabilityDetailResponse,
    ProfessionalAvailabilityListItemResponse,
    ProfessionalAvailabilityUpdateRequest,
)
from app.services.professional_availability_service import ProfessionalAvailabilityService


router = APIRouter(prefix="/professional-availabilities", tags=["Professional Availabilities"])


@router.get("", response_model=list[ProfessionalAvailabilityListItemResponse])
def list_items(db: Session = Depends(get_db)):
    service = ProfessionalAvailabilityService(db)
    return service.list_items()


@router.get("/profile/{profile_id}", response_model=list[ProfessionalAvailabilityListItemResponse])
def list_by_profile_id(profile_id: str, db: Session = Depends(get_db)):
    service = ProfessionalAvailabilityService(db)
    return service.list_by_profile_id(profile_id)


@router.get("/{item_id}", response_model=ProfessionalAvailabilityDetailResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    service = ProfessionalAvailabilityService(db)
    return service.get_item(item_id)


@router.post("", response_model=ProfessionalAvailabilityCreateResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ProfessionalAvailabilityCreateRequest, db: Session = Depends(get_db)):
    service = ProfessionalAvailabilityService(db)
    return service.create_item(payload)


@router.patch("/{item_id}", response_model=ProfessionalAvailabilityDetailResponse)
def update_item(item_id: str, payload: ProfessionalAvailabilityUpdateRequest, db: Session = Depends(get_db)):
    service = ProfessionalAvailabilityService(db)
    return service.update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    service = ProfessionalAvailabilityService(db)
    return service.delete_item(item_id)