from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services.review_service import ReviewService


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post(
    "",
    response_model=ReviewResponse,
    status_code=201,
)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReviewService.create_review(db, current_user, review_data)


@router.get(
    "/me",
    response_model=List[ReviewResponse],
)
def list_reviews_for_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReviewService.list_reviews_for_me(db, current_user)


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
def get_review_detail(
    review_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReviewService.get_review_by_id(db, review_id)