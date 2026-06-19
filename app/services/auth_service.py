import base64
from datetime import UTC, datetime
from io import BytesIO

import pyotp
import qrcode
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_temp_token,
    decode_token,
    hash_password,
    verify_password,
)
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

        # ── MODIFICACIÓN 2FA AQUÍ ──
        if user.totp_enabled:
            return {
                "requires_2fa": True,
                "access_token": None,
                "token_type": "bearer",
                "temp_token": create_temp_token(subject=user.ci),
                "message": "2FA required",
            }

        access_token = create_access_token(subject=user.ci)
        return {
            "requires_2fa": False,
            "access_token": access_token,
            "token_type": "bearer",
            "temp_token": None,
            "message": "Login successful",
        }

    @staticmethod
    def change_password(db: Session, current_user: User, current_password: str, new_password: str) -> None:
        if not current_user.password_hash:
            raise ValueError("User has no password configured")

        if not verify_password(current_password, current_user.password_hash):
            raise ValueError("Current password is incorrect")

        if current_password == new_password:
            raise ValueError("New password must be different from current password")

        current_user.password_hash = hash_password(new_password)
        UserRepository.update(db, current_user)

    # ── MÉTODOS 2FA ──────────────────────────────────────────────────────────

    @staticmethod
    def setup_2fa(db: Session, current_user: User) -> dict:
        if current_user.totp_enabled:
            raise ValueError("2FA is already enabled")

        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=current_user.email, issuer_name="SISWORK")

        img = qrcode.make(uri)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()

        current_user.totp_secret = secret
        current_user.totp_pending_verification = True
        UserRepository.update(db, current_user)

        return {
            "qr_code_base64": qr_b64,
            "secret": secret,
            "message": "Scan QR and verify",
        }

    @staticmethod
    def verify_2fa_setup(db: Session, current_user: User, code: str) -> bool:
        if not current_user.totp_secret or not current_user.totp_pending_verification:
            raise ValueError("2FA setup not initiated")

        totp = pyotp.TOTP(current_user.totp_secret)
        if not totp.verify(code, valid_window=1):
            raise ValueError("Invalid TOTP code")

        current_user.totp_enabled = True
        current_user.totp_pending_verification = False
        UserRepository.update(db, current_user)
        return True

    @staticmethod
    def validate_2fa_login(db: Session, temp_token: str, code: str) -> dict:
        payload = decode_token(temp_token)
        if not payload:
            raise ValueError("Invalid temporary token")

        ci = payload.get("sub")
        user = UserRepository.get_by_ci(db, ci)
        
        if not user or not user.totp_enabled or not user.totp_secret:
            raise ValueError("2FA not configured")

        totp = pyotp.TOTP(user.totp_secret)
        if not totp.verify(code, valid_window=1):
            raise ValueError("Invalid TOTP code")

        access_token = create_access_token(subject=user.ci)
        return {
            "requires_2fa": False,
            "access_token": access_token,
            "token_type": "bearer",
            "temp_token": None,
            "message": "Login successful",
        }

    @staticmethod
    def disable_2fa(db: Session, current_user: User, password: str, code: str) -> bool:
        if not current_user.totp_enabled:
            raise ValueError("2FA is not enabled")

        if not verify_password(password, current_user.password_hash):
            raise ValueError("Incorrect password")

        totp = pyotp.TOTP(current_user.totp_secret)
        if not totp.verify(code, valid_window=1):
            raise ValueError("Invalid TOTP code")

        current_user.totp_enabled = False
        current_user.totp_secret = None
        current_user.totp_pending_verification = False
        UserRepository.update(db, current_user)
        return True