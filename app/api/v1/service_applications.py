from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service_application import (
    ServiceApplicationCreateRequest,
    ServiceApplicationResponse,
    ServiceApplicationUpdateRequest,
)
from app.services.service_application_service import ServiceApplicationService

router = APIRouter(prefix="/service-applications", tags=["Service Applications"])


@router.get("", response_model=list[ServiceApplicationResponse])
def list_items(db: Session = Depends(get_db)):
    return ServiceApplicationService(db).list_items()


@router.get("/{item_id}", response_model=ServiceApplicationResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return ServiceApplicationService(db).get_item(item_id)


@router.post("", response_model=ServiceApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ServiceApplicationCreateRequest, db: Session = Depends(get_db)):
    return ServiceApplicationService(db).create_item(payload)


@router.patch("/{item_id}", response_model=ServiceApplicationResponse)
def update_item(item_id: str, payload: ServiceApplicationUpdateRequest, db: Session = Depends(get_db)):
    return ServiceApplicationService(db).update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return ServiceApplicationService(db).delete_item(item_id)