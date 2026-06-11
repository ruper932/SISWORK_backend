from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    requires_2fa: bool = False
    access_token: str | None = None
    token_type: str = "bearer"
    temp_token: str | None = None
    message: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)