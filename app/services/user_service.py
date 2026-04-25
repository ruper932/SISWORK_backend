from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.models.enums import UserGender, UserRole, UserStatus
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    def list_users(self):
        users = self.repo.list_users()

        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role.value,
                "status": user.status.value,
                "is_active": user.is_active,
                "created_at": user.created_at,
            }
            for user in users
        ]

    def get_user(self, user_id: UUID | str):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "whatsapp_number": user.whatsapp_number,
            "profile_photo_url": user.profile_photo_url,
            "birth_date": user.birth_date,
            "gender": user.gender.value if user.gender else None,
            "role": user.role.value,
            "status": user.status.value,
            "is_active": user.is_active,
            "email_verified_at": user.email_verified_at,
            "last_login_at": user.last_login_at,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    def create_user(self, payload):
        if self.repo.email_exists(payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password_hash=get_password_hash(payload.password),
            phone=payload.phone,
            whatsapp_number=payload.whatsapp_number,
            profile_photo_url=payload.profile_photo_url,
            birth_date=payload.birth_date,
            gender=UserGender(payload.gender) if payload.gender else None,
            role=UserRole(payload.role),
            status=UserStatus(payload.status),
            is_active=payload.is_active,
            failed_login_attempts=0,
        )

        created = self.repo.create(user)

        return {
            "id": created.id,
            "first_name": created.first_name,
            "last_name": created.last_name,
            "email": created.email,
            "role": created.role.value,
            "status": created.status.value,
            "is_active": created.is_active,
            "created_at": created.created_at,
        }

    def update_user(self, user_id: UUID | str, payload):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        data = payload.model_dump(exclude_unset=True)

        if "email" in data and self.repo.email_exists(data["email"], exclude_user_id=user.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "email" in data:
            user.email = data["email"]
        if "phone" in data:
            user.phone = data["phone"]
        if "whatsapp_number" in data:
            user.whatsapp_number = data["whatsapp_number"]
        if "profile_photo_url" in data:
            user.profile_photo_url = data["profile_photo_url"]
        if "birth_date" in data:
            user.birth_date = data["birth_date"]
        if "gender" in data:
            user.gender = UserGender(data["gender"]) if data["gender"] else None
        if "role" in data:
            user.role = UserRole(data["role"])
        if "status" in data:
            user.status = UserStatus(data["status"])
        if "is_active" in data:
            user.is_active = data["is_active"]

        updated = self.repo.save(user)

        return {
            "id": updated.id,
            "first_name": updated.first_name,
            "last_name": updated.last_name,
            "email": updated.email,
            "phone": updated.phone,
            "whatsapp_number": updated.whatsapp_number,
            "profile_photo_url": updated.profile_photo_url,
            "birth_date": updated.birth_date,
            "gender": updated.gender.value if updated.gender else None,
            "role": updated.role.value,
            "status": updated.status.value,
            "is_active": updated.is_active,
            "email_verified_at": updated.email_verified_at,
            "last_login_at": updated.last_login_at,
            "created_at": updated.created_at,
            "updated_at": updated.updated_at,
        }

    def delete_user(self, user_id: UUID | str):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.status = UserStatus.DELETED
        user.is_active = False
        user.deleted_at = datetime.now(timezone.utc)

        self.repo.save(user)

        return {"message": "User deleted successfully"}