import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.enums import ProfessionalRequestStatusEnum
from app.models.professional_request import ProfessionalRequest


class ProfessionalRequestRepository:
    @staticmethod
    def create(db: Session, entity: ProfessionalRequest):
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    @staticmethod
    def get_by_id(db: Session, request_id: uuid.UUID):
        stmt = select(ProfessionalRequest).where(
            ProfessionalRequest.id == request_id
        )
        return db.scalar(stmt)

    @staticmethod
    def get_pending_by_user_ci(db: Session, user_ci: str):
        stmt = select(ProfessionalRequest).where(
            ProfessionalRequest.user_ci == user_ci,
            ProfessionalRequest.status == ProfessionalRequestStatusEnum.PENDING,
            ProfessionalRequest.deleted_at.is_(None),
        )
        return db.scalar(stmt)

    @staticmethod
    def list_by_user_ci(db: Session, user_ci: str, skip: int = 0, limit: int = 50):
        stmt = (
            select(ProfessionalRequest)
            .where(
                ProfessionalRequest.user_ci == user_ci,
                ProfessionalRequest.deleted_at.is_(None),
            )
            .order_by(ProfessionalRequest.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def count_by_user_ci(db: Session, user_ci: str):
        stmt = select(func.count(ProfessionalRequest.id)).where(
            ProfessionalRequest.user_ci == user_ci,
            ProfessionalRequest.deleted_at.is_(None),
        )
        return db.scalar(stmt) or 0

    @staticmethod
    def list_pending(db: Session, skip: int = 0, limit: int = 50):
        stmt = (
            select(ProfessionalRequest)
            .where(
                ProfessionalRequest.status == ProfessionalRequestStatusEnum.PENDING,
                ProfessionalRequest.deleted_at.is_(None),
            )
            .order_by(ProfessionalRequest.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    @staticmethod
    def count_pending(db: Session):
        stmt = select(func.count(ProfessionalRequest.id)).where(
            ProfessionalRequest.status == ProfessionalRequestStatusEnum.PENDING,
            ProfessionalRequest.deleted_at.is_(None),
        )
        return db.scalar(stmt) or 0