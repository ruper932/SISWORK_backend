from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    UserCreateRequest,
    UserCreateResponse,
    UserDetailResponse,
    UserListItemResponse,
    UserUpdateRequest,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserListItemResponse])
def list_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.list_users()


@router.get("/{user_id}", response_model=UserDetailResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user(user_id)


@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(payload)


@router.patch("/{user_id}", response_model=UserDetailResponse)
def update_user(user_id: str, payload: UserUpdateRequest, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update_user(user_id, payload)


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)