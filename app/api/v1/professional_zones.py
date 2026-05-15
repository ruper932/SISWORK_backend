# app/api/v1/professional_zones.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.professional_zone import (
    ProfessionalZoneCreateRequest,
    ProfessionalZoneCreateResponse,
    ProfessionalZoneDetailResponse,
    ProfessionalZoneListItemResponse,
    ProfessionalZoneUpdateRequest,
)
from app.services.professional_zone_service import ProfessionalZoneService


router = APIRouter(prefix="/professional-zones", tags=["Professional Zones"])


@router.get("", response_model=list[ProfessionalZoneListItemResponse])
def list_items(db: Session = Depends(get_db)):
    service = ProfessionalZoneService(db)
    return service.list_items()


@router.get("/profile/{profile_id}", response_model=list[ProfessionalZoneListItemResponse])
def list_by_profile_id(profile_id: str, db: Session = Depends(get_db)):
    service = ProfessionalZoneService(db)
    return service.list_by_profile_id(profile_id)


@router.get("/{item_id}", response_model=ProfessionalZoneDetailResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    service = ProfessionalZoneService(db)
    return service.get_item(item_id)


@router.post("", response_model=ProfessionalZoneCreateResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ProfessionalZoneCreateRequest, db: Session = Depends(get_db)):
    service = ProfessionalZoneService(db)
    return service.create_item(payload)


@router.patch("/{item_id}", response_model=ProfessionalZoneDetailResponse)
def update_item(item_id: str, payload: ProfessionalZoneUpdateRequest, db: Session = Depends(get_db)):
    service = ProfessionalZoneService(db)
    return service.update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    service = ProfessionalZoneService(db)
    return service.delete_item(item_id)