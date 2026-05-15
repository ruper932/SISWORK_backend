from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service_contact import ServiceContactCreateRequest, ServiceContactResponse, ServiceContactUpdateRequest
from app.services.service_contact_service import ServiceContactService

router = APIRouter(prefix="/service-contacts", tags=["Service Contacts"])


@router.get("", response_model=list[ServiceContactResponse])
def list_items(db: Session = Depends(get_db)):
    return ServiceContactService(db).list_items()


@router.get("/{item_id}", response_model=ServiceContactResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return ServiceContactService(db).get_item(item_id)


@router.post("", response_model=ServiceContactResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ServiceContactCreateRequest, db: Session = Depends(get_db)):
    return ServiceContactService(db).create_item(payload)


@router.patch("/{item_id}", response_model=ServiceContactResponse)
def update_item(item_id: str, payload: ServiceContactUpdateRequest, db: Session = Depends(get_db)):
    return ServiceContactService(db).update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return ServiceContactService(db).delete_item(item_id)