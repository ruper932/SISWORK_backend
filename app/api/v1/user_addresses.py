from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_address import UserAddressCreateRequest, UserAddressResponse, UserAddressUpdateRequest
from app.services.user_address_service import UserAddressService

router = APIRouter(prefix="/user-addresses", tags=["User Addresses"])


@router.get("", response_model=list[UserAddressResponse])
def list_items(db: Session = Depends(get_db)):
    return UserAddressService(db).list_items()


@router.get("/{item_id}", response_model=UserAddressResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return UserAddressService(db).get_item(item_id)


@router.post("", response_model=UserAddressResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: UserAddressCreateRequest, db: Session = Depends(get_db)):
    return UserAddressService(db).create_item(payload)


@router.patch("/{item_id}", response_model=UserAddressResponse)
def update_item(item_id: str, payload: UserAddressUpdateRequest, db: Session = Depends(get_db)):
    return UserAddressService(db).update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return UserAddressService(db).delete_item(item_id)