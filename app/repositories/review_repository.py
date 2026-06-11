from __future__ import annotations

import uuid
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.review import Review


class ReviewRepository:
    @staticmethod
    def create(db: Session, review: Review) -> Review:
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def get_by_id(db: Session, review_id: uuid.UUID) -> Optional[Review]:
        stmt = (
            select(Review)
            .options(
                selectinload(Review.application),
                selectinload(Review.reviewer),
                selectinload(Review.reviewed_user),
            )
            .where(Review.id == review_id)
        )
        return db.scalar(stmt)

    @staticmethod
    def get_by_application_and_reviewer(
        db: Session,
        application_id: uuid.UUID,
        reviewer_ci: str,
    ) -> Optional[Review]:
        stmt = select(Review).where(
            Review.application_id == application_id,
            Review.reviewer_ci == reviewer_ci,
        )
        return db.scalar(stmt)

    @staticmethod
    def list_by_reviewed_user(
        db: Session,
        reviewed_user_ci: str,
    ) -> List[Review]:
        stmt = (
            select(Review)
            .options(
                selectinload(Review.application),
                selectinload(Review.reviewer),
                selectinload(Review.reviewed_user),
            )
            .where(Review.reviewed_user_ci == reviewed_user_ci)
            .order_by(Review.created_at.desc())
        )
        return list(db.scalars(stmt).all())