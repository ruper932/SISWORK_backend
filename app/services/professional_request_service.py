from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.enums import (
    ProfessionalRequestStatusEnum,
    RoleEnum,
    VerificationStatusEnum,
)
from app.models.professional_profile import ProfessionalProfile
from app.models.professional_request import ProfessionalRequest
from app.models.user import User
from app.repositories.professional_request_repository import ProfessionalRequestRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.professional_request import ProfessionalRequestCreate


class ProfessionalRequestService:
    @staticmethod
    def create_request(
        db: Session,
        current_user: User,
        payload: ProfessionalRequestCreate,
    ):
        user_roles = RoleRepository.get_user_roles(
            db,
            current_user.ci,
        )

        if RoleEnum.PROFESSIONAL.value in user_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a professional",
            )

        if RoleEnum.CLIENT.value not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only clients can request to become professionals",
            )

        existing_pending = ProfessionalRequestRepository.get_pending_by_user_ci(
            db,
            current_user.ci,
        )
        if existing_pending:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a pending professional request",
            )

        entity = ProfessionalRequest(
            user_ci=current_user.ci,
            bio=payload.bio,
            experience_years=payload.experience_years,
            motivation=payload.motivation,
            status=ProfessionalRequestStatusEnum.PENDING,
        )

        return ProfessionalRequestRepository.create(db, entity)

    @staticmethod
    def list_my_requests(
        db: Session,
        current_user: User,
        skip: int = 0,
        limit: int = 50,
    ):
        items = ProfessionalRequestRepository.list_by_user_ci(
            db,
            current_user.ci,
            skip,
            limit,
        )
        total = ProfessionalRequestRepository.count_by_user_ci(
            db,
            current_user.ci,
        )
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    @staticmethod
    def list_pending(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ):
        items = ProfessionalRequestRepository.list_pending(
            db,
            skip,
            limit,
        )
        total = ProfessionalRequestRepository.count_pending(db)
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    @staticmethod
    def approve_request(
        db: Session,
        professional_request_id: UUID,
        reviewer_ci: str,
    ):
        entity = ProfessionalRequestRepository.get_by_id(
            db,
            professional_request_id,
        )

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional request not found",
            )

        if entity.status != ProfessionalRequestStatusEnum.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending requests can be approved",
            )

        profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.user_ci == entity.user_ci
            )
        )

        if not profile:
            profile = ProfessionalProfile(
                user_ci=entity.user_ci,
                bio=entity.bio,
                experience_years=entity.experience_years,
                verification_status=VerificationStatusEnum.PENDING,
                is_available=True,
            )
            db.add(profile)
            db.flush()
        else:
            if entity.bio is not None:
                profile.bio = entity.bio
            profile.experience_years = entity.experience_years

        RoleRepository.replace_user_role(
            db,
            entity.user_ci,
            RoleEnum.CLIENT.value,
            RoleEnum.PROFESSIONAL.value,
        )

        entity.status = ProfessionalRequestStatusEnum.APPROVED
        entity.reviewed_by_ci = reviewer_ci
        entity.rejection_reason = None

        db.commit()
        db.refresh(entity)
        return entity

    @staticmethod
    def reject_request(
        db: Session,
        professional_request_id: UUID,
        reviewer_ci: str,
        rejection_reason: str,
    ):
        entity = ProfessionalRequestRepository.get_by_id(
            db,
            professional_request_id,
        )

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professional request not found",
            )

        if entity.status != ProfessionalRequestStatusEnum.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending requests can be rejected",
            )

        entity.status = ProfessionalRequestStatusEnum.REJECTED
        entity.reviewed_by_ci = reviewer_ci
        entity.rejection_reason = rejection_reason

        db.commit()
        db.refresh(entity)
        return entity