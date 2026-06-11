from __future__ import annotations

import uuid
from typing import Optional, List

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.application import Application


class ApplicationRepository:
    @staticmethod
    def create(db: Session, application: Application) -> Application:
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def update(db: Session, application: Application) -> Application:
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def get_by_id(db: Session, application_id: uuid.UUID) -> Optional[Application]:
        stmt = (
            select(Application)
            .options(
                selectinload(Application.request),
                selectinload(Application.professional_profile),
            )
            .where(Application.id == application_id)
        )
        return db.scalar(stmt)

    @staticmethod
    def get_by_id_for_professional(
        db: Session,
        application_id: uuid.UUID,
        professional_profile_id: uuid.UUID,
    ) -> Optional[Application]:
        stmt = (
            select(Application)
            .options(
                selectinload(Application.request),
                selectinload(Application.professional_profile),
            )
            .where(
                Application.id == application_id,
                Application.professional_profile_id == professional_profile_id,
            )
        )
        return db.scalar(stmt)

    @staticmethod
    def get_by_id_for_request_owner(
        db: Session,
        application_id: uuid.UUID,
        client_ci: str,
    ) -> Optional[Application]:
        stmt = (
            select(Application)
            .options(
                selectinload(Application.request),
                selectinload(Application.professional_profile),
            )
            .join(Application.request)
            .where(
                Application.id == application_id,
                Application.request.has(client_ci=client_ci),
            )
        )
        return db.scalar(stmt)

    @staticmethod
    def get_visible_by_id(
        db: Session,
        application_id: uuid.UUID,
        current_user_ci: str,
        professional_profile_id: uuid.UUID | None = None,
    ) -> Optional[Application]:
        stmt = (
            select(Application)
            .options(
                selectinload(Application.request),
                selectinload(Application.professional_profile),
            )
            .join(Application.request)
            .where(Application.id == application_id)
        )

        conditions = [Application.request.has(client_ci=current_user_ci)]
        if professional_profile_id is not None:
            conditions.append(Application.professional_profile_id == professional_profile_id)

        stmt = stmt.where(*conditions) if len(conditions) == 1 else stmt.where(conditions[0] | conditions[1])
        return db.scalar(stmt)

    @staticmethod
    def get_by_request_and_professional(
        db: Session,
        request_id: uuid.UUID,
        professional_profile_id: uuid.UUID,
    ) -> Optional[Application]:
        stmt = select(Application).where(
            Application.request_id == request_id,
            Application.professional_profile_id == professional_profile_id,
        )
        return db.scalar(stmt)

    @staticmethod
    def list_by_request(
        db: Session,
        request_id: uuid.UUID,
    ) -> List[Application]:
        stmt = (
            select(Application)
            .options(
                selectinload(Application.professional_profile),
                selectinload(Application.request),
            )
            .where(Application.request_id == request_id)
            .order_by(Application.created_at.desc())
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def count_by_request(
        db: Session,
        request_id: uuid.UUID,
    ) -> int:
        stmt = select(func.count(Application.id)).where(Application.request_id == request_id)
        return db.scalar(stmt) or 0

    @staticmethod
    def list_by_professional(
        db: Session,
        professional_profile_id: uuid.UUID,
    ) -> List[Application]:
        stmt = (
            select(Application)
            .options(
                selectinload(Application.professional_profile),
                selectinload(Application.request),
            )
            .where(Application.professional_profile_id == professional_profile_id)
            .order_by(Application.created_at.desc())
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def count_by_professional(
        db: Session,
        professional_profile_id: uuid.UUID,
    ) -> int:
        stmt = select(func.count(Application.id)).where(
            Application.professional_profile_id == professional_profile_id
        )
        return db.scalar(stmt) or 0