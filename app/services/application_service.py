from __future__ import annotations

from typing import List
import uuid

from fastapi import HTTPException, status
from sqlalchemy import or_, select
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
    def create_application(
        db: Session,
        current_user: User,
        application_data: ApplicationCreate,
    ) -> Application:
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
        return ApplicationRepository.create(db, application)

    @staticmethod
    def get_application_by_id(db: Session, current_user: User, application_id: uuid.UUID) -> Application:
        professional_profile_id = current_user.professional_profile.id if current_user.professional_profile else None
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
        return application

    @staticmethod
    def list_my_applications(db: Session, current_user: User) -> List[Application]:
        professional_profile = ApplicationService._get_professional_profile(db, current_user)
        return ApplicationRepository.list_by_professional(db, professional_profile.id)

    @staticmethod
    def list_request_applications(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
    ) -> List[Application]:
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

        return ApplicationRepository.list_by_request(db, request_id)

    @staticmethod
    def accept_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Application:
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
        db.refresh(application)
        return application

    @staticmethod
    def reject_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Application:
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
        return ApplicationRepository.update(db, application)

    @staticmethod
    def cancel_my_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Application:
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
        return ApplicationRepository.update(db, application)