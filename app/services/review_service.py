from __future__ import annotations

from typing import List
import uuid

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.professional_profile import ProfessionalProfile
from app.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate
from app.db.enums import ApplicationStatusEnum, RequestStatusEnum


class ReviewService:
    @staticmethod
    def create_review(
        db: Session,
        current_user,
        review_data: ReviewCreate,
    ) -> Review:
        application = db.scalar(
            select(Application).where(Application.id == review_data.application_id)
        )
        if not application:
            raise Exception("Application not found")

        request = application.request
        if not request:
            raise Exception("Request not found")

        if request.status != RequestStatusEnum.COMPLETED:
            raise Exception("Reviews are only allowed for completed requests")

        if not request.is_review_enabled:
            raise Exception("Reviews are not enabled for this request")

        if application.status != ApplicationStatusEnum.COMPLETED:
            raise Exception("Only completed applications can be reviewed")

        existing_review = ReviewRepository.get_by_application_and_reviewer(
            db,
            review_data.application_id,
            current_user.ci,
        )
        if existing_review:
            raise Exception("You have already reviewed this application")

        assigned_profile = application.professional_profile
        if not assigned_profile:
            raise Exception("Professional profile not found")

        is_client = request.client_ci == current_user.ci
        is_professional = assigned_profile.user_ci == current_user.ci

        if not is_client and not is_professional:
            raise Exception("You do not have permission to review this application")

        reviewed_user_ci = assigned_profile.user_ci if is_client else request.client_ci

        if reviewed_user_ci == current_user.ci:
            raise Exception("You cannot review yourself")

        review = Review(
            application_id=review_data.application_id,
            reviewer_ci=current_user.ci,
            reviewed_user_ci=reviewed_user_ci,
            rating=review_data.rating,
            comment=review_data.comment,
        )
        created_review = ReviewRepository.create(db, review)

        if reviewed_user_ci == assigned_profile.user_ci:
            ReviewService._recalculate_professional_rating(db, assigned_profile.id)

        return created_review

    @staticmethod
    def get_review_by_id(db: Session, review_id: uuid.UUID) -> Review:
        review = ReviewRepository.get_by_id(db, review_id)
        if not review:
            raise Exception("Review not found")
        return review

    @staticmethod
    def list_reviews_for_me(db: Session, current_user) -> List[Review]:
        return ReviewRepository.list_by_reviewed_user(db, current_user.ci)

    @staticmethod
    def _recalculate_professional_rating(db: Session, professional_profile_id: uuid.UUID) -> None:
        profile = db.scalar(
            select(ProfessionalProfile).where(ProfessionalProfile.id == professional_profile_id)
        )
        if not profile:
            return

        stmt = (
            select(func.avg(Review.rating), func.count(Review.id))
            .join(Application, Application.id == Review.application_id)
            .where(Application.professional_profile_id == professional_profile_id)
        )
        avg_rating, rating_count = db.execute(stmt).one()

        profile.rating_average = float(avg_rating or 0.0)
        profile.rating_count = int(rating_count or 0)

        db.commit()