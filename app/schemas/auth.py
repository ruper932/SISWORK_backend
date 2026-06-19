from pydantic import BaseModel, Field

from app.schemas.user import UserResponse


class LoginResponse(BaseModel):
    requires_2fa: bool = False
    access_token: str | None = None
    token_type: str = "bearer"
    temp_token: str | None = None
    message: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)


class TwoFactorSetupResponse(BaseModel):
    qr_code_base64: str
    secret: str
    message: str


class TwoFactorVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)


class TwoFactorValidateRequest(BaseModel):
    temp_token: str
    code: str = Field(..., min_length=6, max_length=6)


class TwoFactorDisableRequest(BaseModel):
    password: str = Field(..., min_length=1)
    code: str = Field(..., min_length=6, max_length=6)


class CurrentUserResponse(UserResponse):
    totp_enabled: bool = False