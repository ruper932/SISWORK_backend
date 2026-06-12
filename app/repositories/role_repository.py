from sqlalchemy import delete, select
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

    @staticmethod
    def assign_role_to_user(
        db: Session,
        user_ci: str,
        role_name: str,
    ):
        role = RoleRepository.get_by_name(
            db,
            role_name,
        )

        if not role:
            raise ValueError(f"Role {role_name} not found")

        existing = db.scalar(
            select(UserRole).where(
                UserRole.user_ci == user_ci,
                UserRole.role_id == role.id,
            )
        )

        if existing:
            return existing

        user_role = UserRole(
            user_ci=user_ci,
            role_id=role.id,
        )

        db.add(user_role)
        db.flush()

        return user_role

    @staticmethod
    def replace_user_role(
        db: Session,
        user_ci: str,
        old_role_name: str,
        new_role_name: str,
    ):
        old_role = RoleRepository.get_by_name(
            db,
            old_role_name,
        )
        new_role = RoleRepository.get_by_name(
            db,
            new_role_name,
        )

        if not old_role:
            raise ValueError(f"Role {old_role_name} not found")

        if not new_role:
            raise ValueError(f"Role {new_role_name} not found")

        db.execute(
            delete(UserRole).where(
                UserRole.user_ci == user_ci,
                UserRole.role_id == old_role.id,
            )
        )

        existing_new_role = db.scalar(
            select(UserRole).where(
                UserRole.user_ci == user_ci,
                UserRole.role_id == new_role.id,
            )
        )

        if existing_new_role:
            return existing_new_role

        user_role = UserRole(
            user_ci=user_ci,
            role_id=new_role.id,
        )

        db.add(user_role)
        db.flush()

        return user_role