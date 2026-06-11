from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user_role import UserRole


class RoleRepository:
    @staticmethod
    def get_user_roles(
        db: Session,
        user_ci: str,
    ):
        stmt = (
            select(Role.name)
            .join(
                UserRole,
                UserRole.role_id == Role.id,
            )
            .where(
                UserRole.user_ci == user_ci,
            )
        )

        result = db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    def get_by_name(
        db: Session,
        role_name: str,
    ):
        stmt = select(Role).where(
            Role.name == role_name,
        )

        return db.scalar(stmt)