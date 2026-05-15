from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.administrative_note import (
    AdministrativeNoteCreateRequest,
    AdministrativeNoteResponse,
    AdministrativeNoteUpdateRequest,
)
from app.services.administrative_note_service import AdministrativeNoteService

router = APIRouter(prefix="/administrative-notes", tags=["Administrative Notes"])


@router.get("", response_model=list[AdministrativeNoteResponse])
def list_items(db: Session = Depends(get_db)):
    return AdministrativeNoteService(db).list_items()


@router.get("/{item_id}", response_model=AdministrativeNoteResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return AdministrativeNoteService(db).get_item(item_id)


@router.post("", response_model=AdministrativeNoteResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: AdministrativeNoteCreateRequest, db: Session = Depends(get_db)):
    return AdministrativeNoteService(db).create_item(payload)


@router.patch("/{item_id}", response_model=AdministrativeNoteResponse)
def update_item(item_id: str, payload: AdministrativeNoteUpdateRequest, db: Session = Depends(get_db)):
    return AdministrativeNoteService(db).update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return AdministrativeNoteService(db).delete_item(item_id)