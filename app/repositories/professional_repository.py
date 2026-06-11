from __future__ import annotations

import uuid
from typing import Optional, List

from sqlalchemy import select, or_
from sqlalchemy.orm import Session, selectinload, joinedload

from app.db.enums import VerificationStatusEnum
from app.models.professional_profile import ProfessionalProfile
from app.models.professional_specialty import ProfessionalSpecialty
from app.models.specialty import Specialty
from app.models.user import User


class ProfessionalRepository:
    @staticmethod
    def get_by_user_ci(db: Session, user_ci: str) -> Optional[ProfessionalProfile]:
        stmt = (
            select(ProfessionalProfile)
            .options(
                joinedload(ProfessionalProfile.user),
                selectinload(ProfessionalProfile.specialties).joinedload(ProfessionalSpecialty.specialty),
                selectinload(ProfessionalProfile.availabilities),
            )
            .where(ProfessionalProfile.user_ci == user_ci)
        )
        return db.scalar(stmt)

    @staticmethod
    def search_public_professionals(
        db: Session,
        q: Optional[str] = None,
        specialty_id: Optional[uuid.UUID] = None,
        city: Optional[str] = None,
        zone: Optional[str] = None,
        min_rating: Optional[float] = None,
        is_available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ProfessionalProfile]:
        stmt = (
            select(ProfessionalProfile)
            .options(
                joinedload(ProfessionalProfile.user),
                selectinload(ProfessionalProfile.specialties).joinedload(ProfessionalSpecialty.specialty),
                selectinload(ProfessionalProfile.availabilities),
            )
            .where(ProfessionalProfile.verification_status == VerificationStatusEnum.APPROVED)
        )

        if q:
            like_value = f"%{q.strip()}%"
            stmt = stmt.join(ProfessionalProfile.user).where(
                or_(
                    User.firstname.ilike(like_value),
                    User.lastname.ilike(like_value),
                    User.mother_lastname.ilike(like_value),
                    ProfessionalProfile.bio.ilike(like_value),
                )
            )

        if specialty_id:
            stmt = stmt.join(ProfessionalProfile.specialties).where(
                ProfessionalSpecialty.specialty_id == specialty_id
            )

        if city:
            stmt = stmt.join(ProfessionalProfile.user).where(User.city.ilike(f"%{city.strip()}%"))

        if zone:
            stmt = stmt.join(ProfessionalProfile.user).where(User.zone.ilike(f"%{zone.strip()}%"))

        if min_rating is not None:
            stmt = stmt.where(ProfessionalProfile.rating_average >= min_rating)

        if is_available is not None:
            stmt = stmt.where(ProfessionalProfile.is_available == is_available)

        stmt = stmt.order_by(
            ProfessionalProfile.rating_average.desc(),
            ProfessionalProfile.rating_count.desc(),
            ProfessionalProfile.created_at.desc(),
        ).offset(skip).limit(limit)

        return list(db.scalars(stmt).unique().all())