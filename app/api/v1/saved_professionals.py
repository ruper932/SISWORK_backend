from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.saved_professional import SavedProfessionalCreateRequest, SavedProfessionalResponse
from app.services.saved_professional_service import SavedProfessionalService

router = APIRouter(prefix="/saved-professionals", tags=["Saved Professionals"])


@router.get("", response_model=list[SavedProfessionalResponse])
def list_items(db: Session = Depends(get_db)):
    return SavedProfessionalService(db).list_items()


@router.get("/{item_id}", response_model=SavedProfessionalResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return SavedProfessionalService(db).get_item(item_id)


@router.post("", response_model=SavedProfessionalResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: SavedProfessionalCreateRequest, db: Session = Depends(get_db)):
    return SavedProfessionalService(db).create_item(payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return SavedProfessionalService(db).delete_item(item_id)