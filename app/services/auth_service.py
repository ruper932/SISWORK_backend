from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def register(db: Session, user_data: UserCreate) -> User:
        existing_by_ci = UserRepository.get_by_ci(db, user_data.ci)
        if existing_by_ci:
            raise ValueError("User with this CI already exists")

        existing_by_email = UserRepository.get_by_email(db, user_data.email)
        if existing_by_email:
            raise ValueError("User with this email already exists")

        existing_by_phone = UserRepository.get_by_phone(db, user_data.phone)
        if existing_by_phone:
            raise ValueError("User with this phone already exists")

        user = User(
            ci=user_data.ci,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            mother_last_name=user_data.mother_last_name,
            birth_date=user_data.birth_date,
            email=user_data.email,
            phone=user_data.phone,
            whatsapp_enabled=True,
            password_hash=hash_password(user_data.password),
            city=user_data.city,
            zone=user_data.zone,
            is_active=True,
            is_verified=False,
            failed_login_attempts=0,
        )

        created_user = UserRepository.create(db, user)
        RoleRepository.assign_role_to_user(db, created_user.ci, "client")
        db.commit()
        db.refresh(created_user)

        return created_user

    @staticmethod
    def login(db: Session, identifier: str, password: str) -> dict | None:
        clean_identifier = identifier.strip()
        user = UserRepository.get_by_ci_or_email(db, clean_identifier)

        if not user:
            return None

        if not user.password_hash:
            return None

        password_ok = verify_password(password, user.password_hash)
        if not password_ok:
            user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
            UserRepository.update(db, user)
            return None

        if not user.is_active:
            raise ValueError("Inactive user")

        user.failed_login_attempts = 0
        user.last_login = datetime.now(UTC)
        UserRepository.update(db, user)

        access_token = create_access_token(subject=user.ci)

        return {
            "requires_2fa": False,
            "access_token": access_token,
            "token_type": "bearer",
            "temp_token": None,
            "message": "Login successful",
        }

    @staticmethod
    def change_password(
        db: Session,
        current_user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        if not current_user.password_hash:
            raise ValueError("User has no password configured")

        if not verify_password(current_password, current_user.password_hash):
            raise ValueError("Current password is incorrect")

        if current_password == new_password:
            raise ValueError("New password must be different from current password")

        current_user.password_hash = hash_password(new_password)
        UserRepository.update(db, current_user)