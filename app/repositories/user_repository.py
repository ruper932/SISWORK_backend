from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


class UserRepository:
    @staticmethod
    def get_by_ci(
        db: Session,
        ci: str,
        include_deleted: bool = False,
    ):
        stmt = (
            select(User)
            .options(
                joinedload(User.user_roles).joinedload(UserRole.role)
            )
            .where(User.ci == ci)
        )

        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))

        return db.scalar(stmt)

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
        include_deleted: bool = False,
    ):
        stmt = (
            select(User)
            .options(
                joinedload(User.user_roles).joinedload(UserRole.role)
            )
            .where(User.email == email)
        )

        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))

        return db.scalar(stmt)

    @staticmethod
    def get_by_phone(
        db: Session,
        phone: str,
        include_deleted: bool = False,
    ):
        stmt = (
            select(User)
            .options(
                joinedload(User.user_roles).joinedload(UserRole.role)
            )
            .where(User.phone == phone)
        )

        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))

        return db.scalar(stmt)

    @staticmethod
    def get_by_ci_or_email(
        db: Session,
        identifier: str,
    ):
        stmt = (
            select(User)
            .options(
                joinedload(User.user_roles).joinedload(UserRole.role)
            )
            .where(
                or_(
                    User.ci == identifier,
                    User.email == identifier,
                ),
                User.deleted_at.is_(None),
            )
        )

        return db.scalar(stmt)

    @staticmethod
    def list_users(
        db: Session,
        q: str | None = None,
        role: str | None = None,
        city: str | None = None,
        zone: str | None = None,
        is_active: bool | None = None,
        is_verified: bool | None = None,
        include_deleted: bool = False,
        skip: int = 0,
        limit: int = 50,
    ):
        stmt = (
            select(User)
            .options(
                joinedload(User.user_roles).joinedload(UserRole.role)
            )
        )

        count_stmt = select(func.count(func.distinct(User.ci)))
        needs_role_join = bool(role)

        if needs_role_join:
            stmt = stmt.join(User.user_roles).join(UserRole.role)
            count_stmt = (
                count_stmt.select_from(User)
                .join(User.user_roles)
                .join(UserRole.role)
            )
        else:
            count_stmt = count_stmt.select_from(User)

        filters = []

        if not include_deleted:
            filters.append(User.deleted_at.is_(None))

        if q:
            like_value = f"%{q.strip()}%"
            filters.append(
                or_(
                    User.ci.ilike(like_value),
                    User.first_name.ilike(like_value),
                    User.last_name.ilike(like_value),
                    User.mother_last_name.ilike(like_value),
                    User.email.ilike(like_value),
                    User.phone.ilike(like_value),
                )
            )

        if role:
            filters.append(Role.name == role.strip().upper())

        if city:
            filters.append(User.city.ilike(f"%{city.strip()}%"))

        if zone:
            filters.append(User.zone.ilike(f"%{zone.strip()}%"))

        if is_active is not None:
            filters.append(User.is_active == is_active)

        if is_verified is not None:
            filters.append(User.is_verified == is_verified)

        if filters:
            stmt = stmt.where(*filters)
            count_stmt = count_stmt.where(*filters)

        stmt = (
            stmt.order_by(User.created_at.desc(), User.ci.asc())
            .offset(skip)
            .limit(limit)
        )

        items = list(db.scalars(stmt).unique().all())
        total = db.scalar(count_stmt) or 0

        return items, total

    @staticmethod
    def create(
        db: Session,
        user: User,
    ):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update(
        db: Session,
        user: User,
    ):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def soft_delete(
        db: Session,
        user: User,
    ):
        user.is_active = False
        user.deleted_at = func.now()
        db.add(user)
        db.commit()

    @staticmethod
    def restore(
        db: Session,
        user: User,
    ):
        user.deleted_at = None
        user.is_active = True
        db.add(user)
        db.commit()
        db.refresh(user)
        return user