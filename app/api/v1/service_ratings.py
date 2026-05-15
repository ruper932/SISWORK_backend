from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.service_rating import ServiceRatingCreateRequest, ServiceRatingResponse, ServiceRatingUpdateRequest
from app.services.service_rating_service import ServiceRatingService

router = APIRouter(prefix="/service-ratings", tags=["Service Ratings"])


@router.get("", response_model=list[ServiceRatingResponse])
def list_items(db: Session = Depends(get_db)):
    return ServiceRatingService(db).list_items()


@router.get("/{item_id}", response_model=ServiceRatingResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return ServiceRatingService(db).get_item(item_id)


@router.post("", response_model=ServiceRatingResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ServiceRatingCreateRequest, db: Session = Depends(get_db)):
    return ServiceRatingService(db).create_item(payload)


@router.patch("/{item_id}", response_model=ServiceRatingResponse)
def update_item(item_id: str, payload: ServiceRatingUpdateRequest, db: Session = Depends(get_db)):
    return ServiceRatingService(db).update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return ServiceRatingService(db).delete_item(item_id)