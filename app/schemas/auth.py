from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequiresTwoFactorResponse(BaseModel):
    requires_2fa: bool = True
    challenge_token: str
    token_type: str = "bearer"


class VerifyTwoFactorRequest(BaseModel):
    challenge_token: str
    code: str = Field(min_length=6, max_length=6)

class TwoFactorSetupResponse(BaseModel):
    secret: str
    otpauth_uri: str
    backup_codes: list[str]
    already_enabled: bool = False


class TwoFactorDisableRequest(BaseModel):
    password: str = Field(min_length=8, max_length=128)