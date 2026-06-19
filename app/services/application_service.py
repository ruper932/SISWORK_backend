from __future__ import annotations

from typing import List, Dict, Any
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.enums import (
    ApplicationStatusEnum,
    RequestStatusEnum,
    RoleEnum,
    VerificationStatusEnum,
)
from app.models.application import Application
from app.models.professional_profile import ProfessionalProfile
from app.models.request import Request
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.application import ApplicationCreate


class ApplicationService:
    @staticmethod
    def _get_professional_profile(db: Session, current_user: User) -> ProfessionalProfile:
        stmt = select(ProfessionalProfile).where(ProfessionalProfile.user_ci == current_user.ci)
        profile = db.scalar(stmt)

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional profile not found",
            )

        if profile.verification_status != VerificationStatusEnum.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only verified professionals can apply to requests",
            )

        if not profile.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Professional is not available",
            )

        return profile

    @staticmethod
    def _serialize_application(application: Application) -> Dict[str, Any]:
        profile = application.professional_profile
        user = profile.user if profile else None

        return {
            "id": application.id,
            "request_id": application.request_id,
            "professional_profile_id": application.professional_profile_id,
            "proposal_message": application.proposal_message,
            "proposed_price": application.proposed_price,
            "estimated_time_hours": application.estimated_time_hours,
            "status": application.status,
            "created_at": application.created_at,
            "updated_at": application.updated_at,
            "professional_profile": {
                "id": profile.id,
                "user_ci": profile.user_ci,
                "full_name": " ".join(
                    part
                    for part in [
                        getattr(user, "first_name", None),
                        getattr(user, "last_name", None),
                        getattr(user, "mother_last_name", None),
                    ]
                    if part
                ),
                "bio": profile.bio,
                "experience_years": profile.experience_years,
                "verification_status": profile.verification_status,
                "rating_average": profile.rating_average,
                "rating_count": profile.rating_count,
                "is_available": profile.is_available,
                "city": getattr(user, "city", None) if user else None,
                "zone": getattr(user, "zone", None) if user else None,
                "specialties": [
                    {
                        "id": item.specialty.id,
                        "name": item.specialty.name,
                        "description": item.specialty.description,
                    }
                    for item in profile.specialties
                    if getattr(item, "specialty", None) is not None
                ],
                "availabilities": [
                    {
                        "id": availability.id,
                        "day_of_week": availability.day_of_week,
                        "start_time": availability.start_time,
                        "end_time": availability.end_time,
                        "is_active": availability.is_active,
                    }
                    for availability in profile.availabilities
                ],
            } if profile else None,
        }

    @staticmethod
    def create_application(
        db: Session,
        current_user: User,
        application_data: ApplicationCreate,
    ) -> Dict[str, Any]:
        user_roles = RoleRepository.get_user_roles(db, current_user.ci)
        if RoleEnum.PROFESSIONAL.value not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only professionals can create applications",
            )

        professional_profile = ApplicationService._get_professional_profile(db, current_user)

        request = db.get(Request, application_data.request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if request.status != RequestStatusEnum.OPEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request is not available for applications",
            )

        if request.client_ci == current_user.ci:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot apply to your own request",
            )

        existing_application = ApplicationRepository.get_by_request_and_professional(
            db,
            application_data.request_id,
            professional_profile.id,
        )
        if existing_application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied to this request",
            )

        application = Application(
            request_id=application_data.request_id,
            professional_profile_id=professional_profile.id,
            proposal_message=application_data.proposal_message,
            proposed_price=application_data.proposed_price,
            estimated_time_hours=application_data.estimated_time_hours,
            status=ApplicationStatusEnum.PENDING,
        )
        new_app = ApplicationRepository.create(db, application)
        return ApplicationService._serialize_application(new_app)

    @staticmethod
    def get_application_by_id(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Dict[str, Any]:
        professional_profile_id = (
            current_user.professional_profile.id
            if current_user.professional_profile
            else None
        )
        application = ApplicationRepository.get_visible_by_id(
            db,
            application_id,
            current_user.ci,
            professional_profile_id,
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )
        return ApplicationService._serialize_application(application)

    @staticmethod
    def list_my_applications(db: Session, current_user: User) -> List[Dict[str, Any]]:
        professional_profile = ApplicationService._get_professional_profile(db, current_user)
        applications = ApplicationRepository.list_by_professional(db, professional_profile.id)
        return [ApplicationService._serialize_application(app) for app in applications]

    @staticmethod
    def list_request_applications(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
    ) -> List[Dict[str, Any]]:
        request = db.get(Request, request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if request.client_ci != current_user.ci:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view these applications",
            )

        applications = ApplicationRepository.list_by_request(db, request_id)
        return [ApplicationService._serialize_application(app) for app in applications]

    @staticmethod
    def accept_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Dict[str, Any]:
        application = ApplicationRepository.get_by_id_for_request_owner(
            db,
            application_id,
            current_user.ci,
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        request = application.request
        if request.status != RequestStatusEnum.OPEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request is no longer available for assignment",
            )

        request_applications = ApplicationRepository.list_by_request(db, request.id)

        for item in request_applications:
            if item.id == application.id:
                item.status = ApplicationStatusEnum.ACCEPTED
            elif item.status == ApplicationStatusEnum.PENDING:
                item.status = ApplicationStatusEnum.REJECTED

        request.assigned_professional_profile_id = application.professional_profile_id
        request.proposed_final_price = application.proposed_price

        db.commit()
        updated_app = ApplicationRepository.get_by_id(db, application.id)
        return ApplicationService._serialize_application(updated_app)

    @staticmethod
    def reject_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Dict[str, Any]:
        application = ApplicationRepository.get_by_id_for_request_owner(
            db,
            application_id,
            current_user.ci,
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if application.status != ApplicationStatusEnum.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending applications can be rejected",
            )

        application.status = ApplicationStatusEnum.REJECTED
        updated_app = ApplicationRepository.update(db, application)
        return ApplicationService._serialize_application(updated_app)

    @staticmethod
    def cancel_my_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Dict[str, Any]:
        professional_profile = ApplicationService._get_professional_profile(db, current_user)

        application = ApplicationRepository.get_by_id_for_professional(
            db,
            application_id,
            professional_profile.id,
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if application.status != ApplicationStatusEnum.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending applications can be cancelled",
            )

        application.status = ApplicationStatusEnum.CANCELLED
        updated_app = ApplicationRepository.update(db, application)
        return ApplicationService._serialize_application(updated_app)