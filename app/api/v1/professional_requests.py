from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.professional_request import (
    ProfessionalRequestCreate,
    ProfessionalRequestListResponse,
    ProfessionalRequestReject,
    ProfessionalRequestResponse,
)
from app.services.professional_request_service import ProfessionalRequestService


router = APIRouter(
    prefix="/professional-requests",
    tags=["Professional Requests"],
)


@router.post(
    "",
    response_model=ProfessionalRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_professional_request(
    payload: ProfessionalRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProfessionalRequestService.create_request(
        db,
        current_user,
        payload,
    )


@router.get(
    "/me",
    response_model=ProfessionalRequestListResponse,
)
def list_my_professional_requests(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ProfessionalRequestService.list_my_requests(
        db,
        current_user,
        skip,
        limit,
    )


@router.get(
    "/pending",
    response_model=ProfessionalRequestListResponse,
)
def list_pending_professional_requests(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(["SUPPORT", "ADMIN", "SUPERADMIN"])),
):
    return ProfessionalRequestService.list_pending(
        db,
        skip,
        limit,
    )


@router.post(
    "/{professional_request_id}/approve",
    response_model=ProfessionalRequestResponse,
)
def approve_professional_request(
    professional_request_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["SUPPORT", "ADMIN", "SUPERADMIN"])),
):
    return ProfessionalRequestService.approve_request(
        db,
        professional_request_id,
        current_user.ci,
    )


@router.post(
    "/{professional_request_id}/reject",
    response_model=ProfessionalRequestResponse,
)
def reject_professional_request(
    professional_request_id: UUID,
    payload: ProfessionalRequestReject,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["SUPPORT", "ADMIN", "SUPERADMIN"])),
):
    return ProfessionalRequestService.reject_request(
        db,
        professional_request_id,
        current_user.ci,
        payload.rejection_reason,
    )