# app/api/v1/service_requests.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service_request import (
    ServiceRequestCreateRequest,
    ServiceRequestCreateResponse,
    ServiceRequestDetailResponse,
    ServiceRequestListItemResponse,
    ServiceRequestUpdateRequest,
)
from app.services.service_request_service import ServiceRequestService


router = APIRouter(prefix="/service-requests", tags=["Service Requests"])


@router.get("", response_model=list[ServiceRequestListItemResponse])
def list_items(db: Session = Depends(get_db)):
    service = ServiceRequestService(db)
    return service.list_items()


@router.get("/client/{client_user_id}", response_model=list[ServiceRequestListItemResponse])
def list_by_client_user_id(client_user_id: str, db: Session = Depends(get_db)):
    service = ServiceRequestService(db)
    return service.list_by_client_user_id(client_user_id)


@router.get("/{item_id}", response_model=ServiceRequestDetailResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    service = ServiceRequestService(db)
    return service.get_item(item_id)


@router.post("", response_model=ServiceRequestCreateResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ServiceRequestCreateRequest, db: Session = Depends(get_db)):
    service = ServiceRequestService(db)
    return service.create_item(payload)


@router.patch("/{item_id}", response_model=ServiceRequestDetailResponse)
def update_item(item_id: str, payload: ServiceRequestUpdateRequest, db: Session = Depends(get_db)):
    service = ServiceRequestService(db)
    return service.update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    service = ServiceRequestService(db)
    return service.delete_item(item_id)