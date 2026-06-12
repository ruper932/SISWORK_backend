from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.enums import ApplicationStatusEnum, RequestStatusEnum, RoleEnum
from app.models.application import Application
from app.models.review import Review
from app.models.user import User
from app.repositories.review_repository import ReviewRepository
from app.repositories.role_repository import RoleRepository


class ReviewService:
    @staticmethod
    def create_review(db: Session, current_user: User, review_data) -> Review:
        user_roles = RoleRepository.get_user_roles(db, current_user.ci)

        if RoleEnum.CLIENT.value not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only clients can create reviews",
            )

        application = db.get(Application, review_data.application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        request = application.request
        if not request:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request not associated with application",
            )

        if request.client_ci != current_user.ci:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only review professionals for your own requests",
            )

        if request.status != RequestStatusEnum.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review is only allowed when the request is completed",
            )

        if not request.is_review_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review is not enabled for this request",
            )

        if application.professional_profile is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Application does not have a professional profile",
            )

        if request.assigned_professional_profile_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request does not have an assigned professional",
            )

        if application.professional_profile_id != request.assigned_professional_profile_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can only review the assigned professional",
            )

        if application.status not in [
            ApplicationStatusEnum.ACCEPTED,
            ApplicationStatusEnum.COMPLETED,
        ]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only accepted or completed applications can be reviewed",
            )

        existing_review = ReviewRepository.get_by_application_and_reviewer(
            db,
            review_data.application_id,
            current_user.ci,
        )
        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already reviewed this application",
            )

        reviewed_user_ci = application.professional_profile.user_ci

        review = Review(
            application_id=review_data.application_id,
            reviewer_ci=current_user.ci,
            reviewed_user_ci=reviewed_user_ci,
            rating=review_data.rating,
            comment=review_data.comment,
        )

        try:
            db.add(review)

            professional_profile = application.professional_profile
            current_count = professional_profile.rating_count or 0
            current_average = professional_profile.rating_average or 0

            new_count = current_count + 1
            new_average = ((current_average * current_count) + review_data.rating) / new_count

            professional_profile.rating_count = new_count
            professional_profile.rating_average = round(new_average, 2)

            request.is_review_enabled = False

            db.add(professional_profile)
            db.add(request)

            db.commit()
            db.refresh(review)

            return review

        except IntegrityError as e:
            db.rollback()

            if "uq_review_application_reviewer" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="You have already reviewed this application",
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create review due to a database integrity error",
            )

    @staticmethod
    def list_reviews_for_me(db: Session, current_user: User):
        user_roles = RoleRepository.get_user_roles(db, current_user.ci)

        if RoleEnum.PROFESSIONAL.value in user_roles:
            return ReviewRepository.list_by_reviewed_user(db, current_user.ci)

        if RoleEnum.CLIENT.value in user_roles:
            return ReviewRepository.list_by_reviewer(db, current_user.ci)

        return []

    @staticmethod
    def get_review_by_id(db: Session, review_id: uuid.UUID):
        review = ReviewRepository.get_by_id(db, review_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )
        return review