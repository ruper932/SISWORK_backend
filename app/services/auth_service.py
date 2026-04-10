from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import create_access_token, verify_password, get_password_hash
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.contrasena_hash):
            return None

        token = create_access_token(subject=str(user.id_usuario))

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }

    def register(self, payload):
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo ya está registrado",
            )

        user = User(
            nombres=payload.nombres,
            apellidos=payload.apellidos,
            correo=payload.email,
            contrasena_hash=get_password_hash(payload.password),
            telefono=payload.telefono,
            numero_whatsapp=payload.numero_whatsapp,
            rol="cliente",
            estado="activo",
        )

        created = self.repo.create(user)

        return {
            "id_usuario": str(created.id_usuario),
            "nombres": created.nombres,
            "apellidos": created.apellidos,
            "correo": created.correo,
            "rol": created.rol.value if hasattr(created.rol, "value") else str(created.rol),
            "estado": created.estado.value if hasattr(created.estado, "value") else str(created.estado),
        }