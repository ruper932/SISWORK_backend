# app/api/v1/professional_profiles.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.professional_profile import (
    ProfessionalProfileCreateRequest,
    ProfessionalProfileCreateResponse,
    ProfessionalProfileDetailResponse,
    ProfessionalProfileListItemResponse,
    ProfessionalProfileUpdateRequest,
)
from app.services.professional_profile_service import ProfessionalProfileService


router = APIRouter(prefix="/professional-profiles", tags=["Professional Profiles"])


@router.get("", response_model=list[ProfessionalProfileListItemResponse])
def list_profiles(db: Session = Depends(get_db)):
    service = ProfessionalProfileService(db)
    return service.list_profiles()


@router.get("/{profile_id}", response_model=ProfessionalProfileDetailResponse)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    service = ProfessionalProfileService(db)
    return service.get_profile(profile_id)


@router.post("", response_model=ProfessionalProfileCreateResponse, status_code=status.HTTP_201_CREATED)
def create_profile(payload: ProfessionalProfileCreateRequest, db: Session = Depends(get_db)):
    service = ProfessionalProfileService(db)
    return service.create_profile(payload)


@router.patch("/{profile_id}", response_model=ProfessionalProfileDetailResponse)
def update_profile(profile_id: str, payload: ProfessionalProfileUpdateRequest, db: Session = Depends(get_db)):
    service = ProfessionalProfileService(db)
    return service.update_profile(profile_id, payload)


@router.delete("/{profile_id}")
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    service = ProfessionalProfileService(db)
    return service.delete_profile(profile_id)