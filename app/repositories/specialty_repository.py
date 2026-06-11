from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.specialty import Specialty


class SpecialtyRepository:
    @staticmethod
    def list_active(db: Session) -> List[Specialty]:
        stmt = (
            select(Specialty)
            .where(
                Specialty.is_active.is_(True),
                Specialty.deleted_at.is_(None),
            )
            .order_by(Specialty.name.asc())
        )
        return list(db.scalars(stmt).all())