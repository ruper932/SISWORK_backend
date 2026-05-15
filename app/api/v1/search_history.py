from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.search_history import SearchHistoryCreateRequest, SearchHistoryResponse
from app.services.search_history_service import SearchHistoryService

router = APIRouter(prefix="/search-history", tags=["Search History"])


@router.get("", response_model=list[SearchHistoryResponse])
def list_items(db: Session = Depends(get_db)):
    return SearchHistoryService(db).list_items()


@router.get("/{item_id}", response_model=SearchHistoryResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return SearchHistoryService(db).get_item(item_id)


@router.post("", response_model=SearchHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: SearchHistoryCreateRequest, db: Session = Depends(get_db)):
    return SearchHistoryService(db).create_item(payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return SearchHistoryService(db).delete_item(item_id)