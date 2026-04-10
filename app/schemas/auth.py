from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    telefono: str | None = Field(default=None, max_length=20)
    numero_whatsapp: str | None = Field(default=None, max_length=20)

class RegisterResponse(BaseModel):
    id_usuario: str
    nombres: str
    apellidos: str
    correo: EmailStr
    rol: str
    estado: str