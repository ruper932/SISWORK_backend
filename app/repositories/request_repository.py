from __future__ import annotations

import uuid
from typing import Optional, List

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.request import Request
from app.db.enums import RequestStatusEnum, UrgencyLevelEnum


class RequestRepository:
    @staticmethod
    def create(db: Session, request: Request) -> Request:
        db.add(request)
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def update(db: Session, request: Request) -> Request:
        db.add(request)
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def get_by_id(db: Session, request_id: uuid.UUID) -> Optional[Request]:
        stmt = (
            select(Request)
            .options(
                selectinload(Request.client),
                selectinload(Request.specialty),
                selectinload(Request.assigned_professional),
                selectinload(Request.applications),
            )
            .where(Request.id == request_id)
        )
        return db.scalar(stmt)

    @staticmethod
    def get_by_id_for_owner(db: Session, request_id: uuid.UUID, client_ci: str) -> Optional[Request]:
        stmt = (
            select(Request)
            .options(
                selectinload(Request.client),
                selectinload(Request.specialty),
                selectinload(Request.assigned_professional),
                selectinload(Request.applications),
            )
            .where(
                Request.id == request_id,
                Request.client_ci == client_ci,
            )
        )
        return db.scalar(stmt)

    @staticmethod
    def list_public_open_requests(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Request]:
        stmt = (
            select(Request)
            .options(
                selectinload(Request.client),
                selectinload(Request.specialty),
                selectinload(Request.assigned_professional),
            )
            .where(Request.status == RequestStatusEnum.OPEN)
            .order_by(Request.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def count_public_open_requests(db: Session) -> int:
        stmt = select(func.count(Request.id)).where(Request.status == RequestStatusEnum.OPEN)
        return db.scalar(stmt) or 0

    @staticmethod
    def search_public_requests(
        db: Session,
        q: Optional[str] = None,
        specialty_id: Optional[uuid.UUID] = None,
        city: Optional[str] = None,
        zone: Optional[str] = None,
        urgency: Optional[UrgencyLevelEnum] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Request]:
        stmt = (
            select(Request)
            .options(
                selectinload(Request.client),
                selectinload(Request.specialty),
                selectinload(Request.assigned_professional),
            )
            .where(Request.status == RequestStatusEnum.OPEN)
        )

        if q:
            like_value = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    Request.title.ilike(like_value),
                    Request.description.ilike(like_value),
                )
            )

        if specialty_id:
            stmt = stmt.where(Request.specialty_id == specialty_id)

        if city:
            stmt = stmt.where(Request.city.ilike(f"%{city.strip()}%"))

        if zone:
            stmt = stmt.where(Request.zone.ilike(f"%{zone.strip()}%"))

        if urgency is not None:
            stmt = stmt.where(Request.urgency == urgency)

        stmt = stmt.order_by(Request.created_at.desc()).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    @staticmethod
    def count_search_public_requests(
        db: Session,
        q: Optional[str] = None,
        specialty_id: Optional[uuid.UUID] = None,
        city: Optional[str] = None,
        zone: Optional[str] = None,
        urgency: Optional[UrgencyLevelEnum] = None,
    ) -> int:
        stmt = select(func.count(Request.id)).where(Request.status == RequestStatusEnum.OPEN)

        if q:
            like_value = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    Request.title.ilike(like_value),
                    Request.description.ilike(like_value),
                )
            )

        if specialty_id:
            stmt = stmt.where(Request.specialty_id == specialty_id)

        if city:
            stmt = stmt.where(Request.city.ilike(f"%{city.strip()}%"))

        if zone:
            stmt = stmt.where(Request.zone.ilike(f"%{zone.strip()}%"))

        if urgency is not None:
            stmt = stmt.where(Request.urgency == urgency)

        return db.scalar(stmt) or 0

    @staticmethod
    def list_by_client(
        db: Session,
        client_ci: str,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Request]:
        stmt = (
            select(Request)
            .options(
                selectinload(Request.client),
                selectinload(Request.specialty),
                selectinload(Request.assigned_professional),
                selectinload(Request.applications),
            )
            .where(Request.client_ci == client_ci)
            .order_by(Request.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def count_by_client(
        db: Session,
        client_ci: str,
    ) -> int:
        stmt = select(func.count(Request.id)).where(Request.client_ci == client_ci)
        return db.scalar(stmt) or 0

    @staticmethod
    def exists_by_id(db: Session, request_id: uuid.UUID) -> bool:
        stmt = select(Request.id).where(Request.id == request_id)
        return db.scalar(stmt) is not None