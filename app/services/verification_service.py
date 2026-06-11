from sqlalchemy import select

from app.models.role import Role

from app.models.user_role import UserRole

from app.models.professional_profile import (
    ProfessionalProfile,
)

from app.models.verification_request import (
    VerificationRequest,
)

from app.db.enums import VerificationStatusEnum


class VerificationService:

    @staticmethod
    def approve_verification(
        db,
        verification_request_id,
        reviewer_ci,
    ):

        verification_request = db.scalar(
            select(VerificationRequest).where(
                VerificationRequest.id
                == verification_request_id
            )
        )

        if not verification_request:
            raise Exception(
                "Verification request not found"
            )

        verification_request.status = (
            VerificationStatusEnum.APPROVED
        )

        verification_request.reviewed_by_ci = (
            reviewer_ci
        )

        profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id
                == verification_request.professional_profile_id
            )
        )

        profile.verification_status = (
            VerificationStatusEnum.APPROVED
        )

        role = db.scalar(
            select(Role).where(
                Role.name == "PROFESSIONAL"
            )
        )

        existing_role = db.scalar(
            select(UserRole).where(
                UserRole.user_ci == profile.user_ci,
                UserRole.role_id == role.id,
            )
        )

        if not existing_role:

            user_role = UserRole(
                user_ci=profile.user_ci,
                role_id=role.id,
            )

            db.add(user_role)

        db.commit()

        return verification_request

    @staticmethod
    def reject_verification(
        db,
        verification_request_id,
        reviewer_ci,
        rejection_reason,
    ):

        verification_request = db.scalar(
            select(VerificationRequest).where(
                VerificationRequest.id
                == verification_request_id
            )
        )

        if not verification_request:
            raise Exception(
                "Verification request not found"
            )

        verification_request.status = (
            VerificationStatusEnum.REJECTED
        )

        verification_request.reviewed_by_ci = (
            reviewer_ci
        )

        verification_request.rejection_reason = (
            rejection_reason
        )

        profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id
                == verification_request.professional_profile_id
            )
        )

        profile.verification_status = (
            VerificationStatusEnum.REJECTED
        )

        db.commit()

        return verification_request