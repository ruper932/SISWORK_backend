from datetime import datetime, timedelta, timezone
from typing import Any

import pyotp
from jose import jwt
import secrets
import json
from pwdlib import PasswordHash

from app.core.config import settings


password_hash = PasswordHash.recommended()
backup_code_hasher = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )

    payload = {
        "sub": str(subject),
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def create_challenge_token(subject: str | Any, expires_minutes: int = 5) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    payload = {
        "sub": str(subject),
        "exp": expire,
        "type": "2fa_challenge",
    }

    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])

def generate_totp_secret() -> str:
    return pyotp.random_base32()


def build_totp_uri(email: str, secret: str) -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.totp_issuer)

def verify_totp_code(secret: str, code: str) -> bool:
    clean_code = str(code).strip().replace(" ", "")
    totp = pyotp.TOTP(secret)
    return totp.verify(clean_code, valid_window=1)


def generate_backup_codes(count: int = 8) -> list[str]:
    codes = []
    for _ in range(count):
        code = secrets.token_hex(4).upper()
        codes.append(code)
    return codes


def hash_backup_codes(codes: list[str]) -> str:
    hashed = [backup_code_hasher.hash(code) for code in codes]
    return json.dumps(hashed)


def verify_backup_code(plain_code: str, backup_codes_json: str | None) -> tuple[bool, str | None]:
    if not backup_codes_json:
        return False, backup_codes_json

    hashed_codes = json.loads(backup_codes_json)

    for idx, hashed in enumerate(hashed_codes):
        if backup_code_hasher.verify(plain_code, hashed):
            remaining = hashed_codes[:idx] + hashed_codes[idx + 1 :]
            return True, json.dumps(remaining)

    return False, backup_codes_json