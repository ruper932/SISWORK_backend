from pydantic import BaseModel, EmailStr


class UserMeResponse(BaseModel):
    id_usuario: str
    nombres: str
    apellidos: str
    correo: EmailStr
    rol: str
    estado: str