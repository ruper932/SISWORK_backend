from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user, require_roles
from app.db.enums import UrgencyLevelEnum
from app.db.session import get_db
from app.models.user import User
from app.schemas.request import (
    RequestCancel,
    RequestCreate,
    RequestListResponse,
    RequestResponse,
    RequestUpdate,
)
from app.services.request_service import RequestService

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)


@router.post(
    "",
    response_model=RequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_request(
    request_data: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["CLIENT"])),
):
    return RequestService.create_request(db, current_user, request_data)


@router.get(
    "",
    response_model=RequestListResponse,
)
def list_requests(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None),
    specialty_id: uuid.UUID | None = Query(default=None),
    city: str | None = Query(default=None),
    zone: str | None = Query(default=None),
    urgency: UrgencyLevelEnum | None = Query(default=None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    has_filters = any([q, specialty_id, city, zone, urgency])
    if has_filters:
        return RequestService.search_public_requests(
            db=db,
            q=q,
            specialty_id=specialty_id,
            city=city,
            zone=zone,
            urgency=urgency,
            skip=skip,
            limit=limit,
        )
    return RequestService.list_public_requests(db, skip=skip, limit=limit)


@router.get(
    "/me",
    response_model=RequestListResponse,
)
def list_my_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    return RequestService.list_my_requests(db, current_user, skip=skip, limit=limit)


@router.post(
    "/{request_id}/cancel",
    response_model=RequestResponse,
)
def cancel_request(
    request_id: uuid.UUID,
    payload: RequestCancel | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["CLIENT"])),
):
    cancellation_reason = payload.cancellation_reason if payload else None
    return RequestService.cancel_request(db, current_user, request_id, cancellation_reason)


@router.post(
    "/{request_id}/start",
    response_model=RequestResponse,
)
def start_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RequestService.start_request(db, current_user, request_id)


@router.post(
    "/{request_id}/complete",
    response_model=RequestResponse,
)
def complete_request(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return RequestService.complete_request(db, current_user, request_id)


@router.get(
    "/{request_id}",
    response_model=RequestResponse,
)
def get_request_detail(
    request_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    request = RequestService.get_request_by_id(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.put(
    "/{request_id}",
    response_model=RequestResponse,
)
def update_request(
    request_id: uuid.UUID,
    request_data: RequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["CLIENT"])),
):
    return RequestService.update_request(db, current_user, request_id, request_data)