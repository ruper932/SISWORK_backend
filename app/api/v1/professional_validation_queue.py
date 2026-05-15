from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.professional_validation_queue import (
    ProfessionalValidationQueueCreateRequest,
    ProfessionalValidationQueueResponse,
    ProfessionalValidationQueueUpdateRequest,
)
from app.services.professional_validation_queue_service import ProfessionalValidationQueueService

router = APIRouter(prefix="/professional-validation-queue", tags=["Professional Validation Queue"])


@router.get("", response_model=list[ProfessionalValidationQueueResponse])
def list_items(db: Session = Depends(get_db)):
    return ProfessionalValidationQueueService(db).list_items()


@router.get("/{item_id}", response_model=ProfessionalValidationQueueResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return ProfessionalValidationQueueService(db).get_item(item_id)


@router.post("", response_model=ProfessionalValidationQueueResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ProfessionalValidationQueueCreateRequest, db: Session = Depends(get_db)):
    return ProfessionalValidationQueueService(db).create_item(payload)


@router.patch("/{item_id}", response_model=ProfessionalValidationQueueResponse)
def update_item(item_id: str, payload: ProfessionalValidationQueueUpdateRequest, db: Session = Depends(get_db)):
    return ProfessionalValidationQueueService(db).update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return ProfessionalValidationQueueService(db).delete_item(item_id)