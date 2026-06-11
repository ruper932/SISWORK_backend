from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    @staticmethod
    def _serialize_user(user: User):
        roles = [user_role.role.name for user_role in user.user_roles]

        return {
            "ci": user.ci,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "mother_last_name": user.mother_last_name,
            "birth_date": user.birth_date,
            "email": user.email,
            "phone": user.phone,
            "city": user.city,
            "zone": user.zone,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "roles": roles,
        }

    @staticmethod
    def list_users(
        db,
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
        items, total = UserRepository.list_users(
            db=db,
            q=q,
            role=role,
            city=city,
            zone=zone,
            is_active=is_active,
            is_verified=is_verified,
            include_deleted=include_deleted,
            skip=skip,
            limit=limit,
        )

        return {
            "items": [UserService._serialize_user(item) for item in items],
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    @staticmethod
    def get_user_by_ci(db, ci: str):
        user = UserRepository.get_by_ci(db, ci, include_deleted=True)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserService._serialize_user(user)

    @staticmethod
    def create_user_admin(db, user_data: UserCreate):
        existing_ci = UserRepository.get_by_ci(db, user_data.ci, include_deleted=True)
        if existing_ci:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this CI already exists",
            )

        existing_email = UserRepository.get_by_email(db, user_data.email, include_deleted=True)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists",
            )

        existing_phone = UserRepository.get_by_phone(db, user_data.phone, include_deleted=True)
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this phone already exists",
            )

        user = User(
            ci=user_data.ci,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            mother_last_name=user_data.mother_last_name,
            birth_date=user_data.birth_date,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hash_password(user_data.password),
            city=user_data.city,
            zone=user_data.zone,
            is_active=True,
            is_verified=False,
        )

        created_user = UserRepository.create(db, user)
        created_user = UserRepository.get_by_ci(db, created_user.ci, include_deleted=True)

        return UserService._serialize_user(created_user)

    @staticmethod
    def update_user(db, ci: str, user_data: UserUpdate):
        user = UserRepository.get_by_ci(db, ci, include_deleted=True)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        update_data = user_data.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing_email = UserRepository.get_by_email(
                db,
                update_data["email"],
                include_deleted=True,
            )
            if existing_email and existing_email.ci != ci:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email already exists",
                )

        if "phone" in update_data:
            existing_phone = UserRepository.get_by_phone(
                db,
                update_data["phone"],
                include_deleted=True,
            )
            if existing_phone and existing_phone.ci != ci:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this phone already exists",
                )

        if "password" in update_data:
            user.password_hash = hash_password(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        updated_user = UserRepository.update(db, user)
        updated_user = UserRepository.get_by_ci(db, updated_user.ci, include_deleted=True)

        return UserService._serialize_user(updated_user)

    @staticmethod
    def delete_user(db, ci: str):
        user = UserRepository.get_by_ci(db, ci, include_deleted=False)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        UserRepository.soft_delete(db, user)

    @staticmethod
    def restore_user(db, ci: str):
        user = UserRepository.get_by_ci(db, ci, include_deleted=True)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return UserService._serialize_user(UserRepository.restore(db, user))