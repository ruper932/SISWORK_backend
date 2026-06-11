from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.api.deps.auth import require_roles

from app.db.session import get_db

from app.models.user import User

from app.services.verification_service import (
    VerificationService,
)


router = APIRouter(
    prefix="/support",
    tags=["Support"],
)


@router.post(
    "/approve/{verification_request_id}",
)
def approve_verification(
    verification_request_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "SUPPORT",
                "ADMIN",
                "SUPERADMIN",
            ]
        )
    ),
):

    try:

        result = (
            VerificationService.approve_verification(
                db,
                verification_request_id,
                current_user.ci,
            )
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/reject/{verification_request_id}",
)
def reject_verification(
    verification_request_id: UUID,
    rejection_reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            [
                "SUPPORT",
                "ADMIN",
                "SUPERADMIN",
            ]
        )
    ),
):

    try:

        result = (
            VerificationService.reject_verification(
                db,
                verification_request_id,
                current_user.ci,
                rejection_reason,
            )
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )