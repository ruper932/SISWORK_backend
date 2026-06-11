from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.enums import (
    RequestStatusEnum,
    RoleEnum,
    ApplicationStatusEnum,
    UrgencyLevelEnum,
)
from app.models.application import Application
from app.models.request import Request
from app.models.specialty import Specialty
from app.models.user import User
from app.repositories.request_repository import RequestRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.request import RequestCreate, RequestUpdate


class RequestService:
    @staticmethod
    def create_request(db: Session, current_user: User, request_data: RequestCreate) -> Request:
        user_roles = RoleRepository.get_user_roles(db, current_user.ci)
        if RoleEnum.CLIENT.value not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only clients can create requests",
            )

        specialty = db.get(Specialty, request_data.specialty_id)
        if not specialty or not specialty.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Specialty not found or inactive",
            )

        request = Request(
            client_ci=current_user.ci,
            specialty_id=request_data.specialty_id,
            title=request_data.title,
            description=request_data.description,
            budget=request_data.budget,
            proposed_final_price=request_data.proposed_final_price,
            scheduled_date=request_data.scheduled_date,
            city=request_data.city,
            zone=request_data.zone,
            latitude=request_data.latitude,
            longitude=request_data.longitude,
            urgency=request_data.urgency,
            status=RequestStatusEnum.OPEN,
            is_review_enabled=False,
        )
        return RequestRepository.create(db, request)

    @staticmethod
    def get_request_by_id(db: Session, request_id: uuid.UUID) -> Request | None:
        return RequestRepository.get_by_id(db, request_id)

    @staticmethod
    def list_public_requests(db: Session, skip: int = 0, limit: int = 50):
        items = RequestRepository.list_public_open_requests(db, skip=skip, limit=limit)
        total = RequestRepository.count_public_open_requests(db)
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    @staticmethod
    def search_public_requests(
        db: Session,
        q: str | None = None,
        specialty_id: uuid.UUID | None = None,
        city: str | None = None,
        zone: str | None = None,
        urgency: UrgencyLevelEnum | None = None,
        skip: int = 0,
        limit: int = 50,
    ):
        items = RequestRepository.search_public_requests(
            db=db,
            q=q,
            specialty_id=specialty_id,
            city=city,
            zone=zone,
            urgency=urgency,
            skip=skip,
            limit=limit,
        )
        total = RequestRepository.count_search_public_requests(
            db=db,
            q=q,
            specialty_id=specialty_id,
            city=city,
            zone=zone,
            urgency=urgency,
        )
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    @staticmethod
    def list_my_requests(db: Session, current_user: User, skip: int = 0, limit: int = 50):
        items = RequestRepository.list_by_client(db, current_user.ci, skip=skip, limit=limit)
        total = RequestRepository.count_by_client(db, current_user.ci)
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    @staticmethod
    def update_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
        request_data: RequestUpdate,
    ) -> Request:
        request = RequestRepository.get_by_id_for_owner(db, request_id, current_user.ci)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if request.status != RequestStatusEnum.OPEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only open requests can be updated",
            )

        if request_data.specialty_id is not None:
            specialty = db.get(Specialty, request_data.specialty_id)
            if not specialty or not specialty.is_active:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Specialty not found or inactive",
                )
            request.specialty_id = request_data.specialty_id

        if request_data.title is not None:
            request.title = request_data.title

        if request_data.description is not None:
            request.description = request_data.description

        if request_data.budget is not None:
            request.budget = request_data.budget

        if request_data.proposed_final_price is not None:
            request.proposed_final_price = request_data.proposed_final_price

        if request_data.scheduled_date is not None:
            request.scheduled_date = request_data.scheduled_date

        if request_data.city is not None:
            request.city = request_data.city

        if request_data.zone is not None:
            request.zone = request_data.zone

        if request_data.latitude is not None:
            request.latitude = request_data.latitude

        if request_data.longitude is not None:
            request.longitude = request_data.longitude

        if request_data.urgency is not None:
            request.urgency = request_data.urgency

        return RequestRepository.update(db, request)

    @staticmethod
    def cancel_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
        cancellation_reason: str | None = None,
    ) -> Request:
        request = RequestRepository.get_by_id_for_owner(db, request_id, current_user.ci)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if request.status in [RequestStatusEnum.COMPLETED, RequestStatusEnum.CANCELLED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request cannot be cancelled",
            )

        request.status = RequestStatusEnum.CANCELLED
        request.cancellation_reason = cancellation_reason or "Cancelled by client"

        pending_or_accepted_applications = db.scalars(
            select(Application).where(
                Application.request_id == request.id,
                Application.status.in_([
                    ApplicationStatusEnum.PENDING,
                    ApplicationStatusEnum.ACCEPTED,
                ]),
            )
        ).all()

        for application in pending_or_accepted_applications:
            application.status = ApplicationStatusEnum.CANCELLED

        return RequestRepository.update(db, request)

    @staticmethod
    def start_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
    ) -> Request:
        request = RequestRepository.get_by_id(db, request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        is_client = request.client_ci == current_user.ci
        is_assigned_professional = (
            request.assigned_professional is not None
            and request.assigned_professional.user_ci == current_user.ci
        )

        if not is_client and not is_assigned_professional:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to start this request",
            )

        if request.status != RequestStatusEnum.OPEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only open requests can be started",
            )

        accepted_application = db.scalar(
            select(Application).where(
                Application.request_id == request.id,
                Application.status == ApplicationStatusEnum.ACCEPTED,
            )
        )
        if not accepted_application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Accepted application not found for this request",
            )

        request.status = RequestStatusEnum.IN_PROGRESS
        return RequestRepository.update(db, request)

    @staticmethod
    def complete_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
    ) -> Request:
        request = RequestRepository.get_by_id(db, request_id)
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        is_client = request.client_ci == current_user.ci
        is_assigned_professional = (
            request.assigned_professional is not None
            and request.assigned_professional.user_ci == current_user.ci
        )

        if not is_client and not is_assigned_professional:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to complete this request",
            )

        if request.status != RequestStatusEnum.IN_PROGRESS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only requests in progress can be completed",
            )

        accepted_application = db.scalar(
            select(Application).where(
                Application.request_id == request.id,
                Application.status == ApplicationStatusEnum.ACCEPTED,
            )
        )
        if not accepted_application:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Accepted application not found for this request",
            )

        request.status = RequestStatusEnum.COMPLETED
        request.is_review_enabled = True
        accepted_application.status = ApplicationStatusEnum.COMPLETED

        return RequestRepository.update(db, request)