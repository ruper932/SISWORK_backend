from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RegisterRequest
from app.schemas.user import UserMeResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Registrar usuario")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(payload)


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    result = service.login(payload.email, payload.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
    }


@router.get("/me", response_model=UserMeResponse, summary="Usuario autenticado")
def me(current_user=Depends(get_current_user)):
    return {
        "id_usuario": str(current_user.id_usuario),
        "nombres": current_user.nombres,
        "apellidos": current_user.apellidos,
        "correo": current_user.correo,
        "rol": current_user.rol.value,
        "estado": current_user.estado.value,
    }


@router.get("/health", summary="Health check de auth")
def auth_health():
    return {
        "module": "auth",
        "status": "ok",
    }