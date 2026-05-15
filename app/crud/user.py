from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    return db.scalar(select(User).where(User.id == user_id))


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.scalar(select(User).where(User.email == email))


def get_users(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(User).offset(skip).limit(limit).order_by(User.createdat.desc())
    return db.scalars(stmt).all()


def create_user(db: Session, payload: UserCreate) -> User:
    user = User(
        firstname=payload.firstname,
        lastname=payload.lastname,
        email=payload.email,
        passwordhash=get_password_hash(payload.password),
        role=payload.role,
        status="ACTIVE",
        failedloginattempts=0,
        isactive=True,
        phone=payload.phone,
        whatsappnumber=payload.whatsappnumber,
        profilephotourl=payload.profilephotourl,
        birthdate=payload.birthdate,
        gender=payload.gender,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, db_obj: User, payload: UserUpdate) -> User:
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def soft_delete_user(db: Session, db_obj: User) -> User:
    db_obj.status = "DELETED"
    db_obj.isactive = False
    db_obj.deletedat = datetime.now(timezone.utc)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj