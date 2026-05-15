# app/api/v1/certifications.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.certification import (
    CertificationCreateRequest,
    CertificationCreateResponse,
    CertificationDetailResponse,
    CertificationListItemResponse,
    CertificationUpdateRequest,
)
from app.services.certification_service import CertificationService


router = APIRouter(prefix="/certifications", tags=["Certifications"])


@router.get("", response_model=list[CertificationListItemResponse])
def list_items(db: Session = Depends(get_db)):
    service = CertificationService(db)
    return service.list_items()


@router.get("/profile/{profile_id}", response_model=list[CertificationListItemResponse])
def list_by_profile_id(profile_id: str, db: Session = Depends(get_db)):
    service = CertificationService(db)
    return service.list_by_profile_id(profile_id)


@router.get("/{item_id}", response_model=CertificationDetailResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    service = CertificationService(db)
    return service.get_item(item_id)


@router.post("", response_model=CertificationCreateResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: CertificationCreateRequest, db: Session = Depends(get_db)):
    service = CertificationService(db)
    return service.create_item(payload)


@router.patch("/{item_id}", response_model=CertificationDetailResponse)
def update_item(item_id: str, payload: CertificationUpdateRequest, db: Session = Depends(get_db)):
    service = CertificationService(db)
    return service.update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    service = CertificationService(db)
    return service.delete_item(item_id)