from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .options(joinedload(User.two_factor))
            .filter(User.email == email, User.deleted_at.is_(None))
            .first()
        )

    def get_by_id(self, user_id: UUID | str) -> User | None:
        return (
            self.db.query(User)
            .options(joinedload(User.two_factor))
            .filter(User.id == user_id, User.deleted_at.is_(None))
            .first()
        )

    def list_users(self) -> list[User]:
        return (
            self.db.query(User)
            .filter(User.deleted_at.is_(None))
            .order_by(User.created_at.desc())
            .all()
        )

    def email_exists(self, email: str, exclude_user_id: UUID | str | None = None) -> bool:
        query = self.db.query(User).filter(
            User.email == email,
            User.deleted_at.is_(None),
        )

        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)

        return query.first() is not None

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def soft_delete(self, user: User) -> User:
        user.deleted_at = datetime.now(timezone.utc)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user