from datetime import datetime, timezone

from fastapi import HTTPException, status
from jose import JWTError

from app.core.security import (
    build_totp_uri,
    create_access_token,
    create_challenge_token,
    decode_token,
    generate_backup_codes,
    generate_totp_secret,
    get_password_hash,
    hash_backup_codes,
    verify_password,
    verify_totp_code,
)
from app.models.user_two_factor import UserTwoFactor
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    def register(self, payload):
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password_hash=get_password_hash(payload.password),
        )

        created = self.repo.create(user)

        return {
            "id": created.id,
            "first_name": created.first_name,
            "last_name": created.last_name,
            "email": created.email,
            "role": created.role.value,
            "status": created.status.value,
            "email_verified_at": created.email_verified_at,
            "last_login_at": created.last_login_at,
        }

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if user.status.value != "active" or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not active",
            )

        if user.two_factor and user.two_factor.is_enabled and user.two_factor.secret:
            challenge_token = create_challenge_token(subject=str(user.id))
            return {
                "requires_2fa": True,
                "challenge_token": challenge_token,
                "token_type": "bearer",
            }

        user.last_login_at = datetime.now(timezone.utc)
        self.repo.save(user)

        access_token = create_access_token(subject=str(user.id))

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def verify_two_factor_login(self, challenge_token: str, code: str):
        try:
            payload = decode_token(challenge_token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired challenge token",
            )

        if payload.get("type") != "2fa_challenge":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid challenge token type",
            )

        user_id = payload.get("sub")
        user = self.repo.get_by_id(user_id)

        if not user or not user.two_factor or not user.two_factor.secret:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="2FA configuration not found",
            )

        if not verify_totp_code(user.two_factor.secret, code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid 2FA code",
            )

        user.last_login_at = datetime.now(timezone.utc)
        self.repo.save(user)

        access_token = create_access_token(subject=str(user.id))

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    def setup_two_factor(self, current_user):
        if current_user.two_factor and current_user.two_factor.is_enabled:
            return {
                "secret": current_user.two_factor.secret,
                "otpauth_uri": build_totp_uri(current_user.email, current_user.two_factor.secret),
                "backup_codes": [],
                "already_enabled": True,
            }

        secret = generate_totp_secret()
        backup_codes = generate_backup_codes()

        if current_user.two_factor:
            current_user.two_factor.secret = secret
            current_user.two_factor.is_enabled = False
            current_user.two_factor.confirmed_at = None
            current_user.two_factor.backup_codes = hash_backup_codes(backup_codes)
        else:
            current_user.two_factor = UserTwoFactor(
                secret=secret,
                is_enabled=False,
                confirmed_at=None,
                backup_codes=hash_backup_codes(backup_codes),
            )

        self.repo.save(current_user)

        return {
            "secret": secret,
            "otpauth_uri": build_totp_uri(current_user.email, secret),
            "backup_codes": backup_codes,
            "already_enabled": False,
        }

    def confirm_two_factor(self, current_user, code: str):
        if not current_user.two_factor or not current_user.two_factor.secret:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="2FA setup not initialized",
            )

        if not verify_totp_code(current_user.two_factor.secret, code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid 2FA code",
            )

        current_user.two_factor.is_enabled = True
        current_user.two_factor.confirmed_at = datetime.now(timezone.utc)
        self.repo.save(current_user)

        return {"message": "2FA enabled successfully"}

    def disable_two_factor(self, current_user, password: str):
        if not verify_password(password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )

        if not current_user.two_factor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="2FA not configured",
            )

        current_user.two_factor.is_enabled = False
        current_user.two_factor.secret = None
        current_user.two_factor.confirmed_at = None
        current_user.two_factor.backup_codes = None
        self.repo.save(current_user)

        return {"message": "2FA disabled successfully"}