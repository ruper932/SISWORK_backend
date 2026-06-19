from datetime import datetime, timedelta, UTC

from jose import jwt
from jose import JWTError
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            hours=settings.ACCESS_TOKEN_EXPIRE_HOURS
        )

    to_encode = {
        "sub": subject,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None
def create_temp_token(subject: str) -> str:
    """Token temporal de 5 minutos para el proceso de 2FA."""
    return create_access_token(
        subject=subject,
        expires_delta=timedelta(minutes=5)
    )

createtemptoken = create_temp_token

# Compatibilidad con imports viejos
hashpassword = hash_password
verifypassword = verify_password
createaccesstoken = create_access_token
decodetoken = decode_token