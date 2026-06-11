from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.application import (
    ApplicationCreate,
    ApplicationListResponse,
    ApplicationResponse,
)
from app.services.application_service import ApplicationService


router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["PROFESSIONAL"])),
):
    try:
        return ApplicationService.create_application(db, current_user, application_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/me",
    response_model=ApplicationListResponse,
)
def list_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["PROFESSIONAL"])),
):
    try:
        items = ApplicationService.list_my_applications(db, current_user)
        return {
            "items": items,
            "total": len(items),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application_detail(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return ApplicationService.get_application_by_id(db, current_user, application_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/request/{request_id}",
    response_model=ApplicationListResponse,
)
def list_request_applications(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        items = ApplicationService.list_request_applications(db, current_user, request_id)
        return {
            "items": items,
            "total": len(items),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{application_id}/accept",
    response_model=ApplicationResponse,
)
def accept_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["CLIENT"])),
):
    try:
        return ApplicationService.accept_application(db, current_user, application_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{application_id}/reject",
    response_model=ApplicationResponse,
)
def reject_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["CLIENT"])),
):
    try:
        return ApplicationService.reject_application(db, current_user, application_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{application_id}/cancel",
    response_model=ApplicationResponse,
)
def cancel_my_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["PROFESSIONAL"])),
):
    try:
        return ApplicationService.cancel_my_application(db, current_user, application_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))