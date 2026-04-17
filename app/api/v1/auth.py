from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth import (
    
    LoginRequiresTwoFactorResponse,
    LoginRequest,
    LoginTokenResponse,
    RegisterRequest,
    TwoFactorConfirmRequest,
    TwoFactorDisableRequest,
    TwoFactorSetupResponse,
    VerifyTwoFactorRequest,
)
from app.schemas.user import UserMeResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(payload)


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(payload.email, payload.password)


@router.post("/login/verify-2fa", response_model=LoginTokenResponse)
def verify_two_factor(payload: VerifyTwoFactorRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.verify_two_factor_login(
        challenge_token=payload.challenge_token,
        code=payload.code,
    )


@router.get("/me", response_model=UserMeResponse)
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role.value,
        "status": current_user.status.value,
        "email_verified_at": current_user.email_verified_at,
        "last_login_at": current_user.last_login_at,
    }

@router.post("/2fa/setup", response_model=TwoFactorSetupResponse)
def setup_two_factor(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.setup_two_factor(current_user)


@router.post("/2fa/confirm")
def confirm_two_factor(
    payload: TwoFactorConfirmRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.confirm_two_factor(current_user, payload.code)


@router.post("/2fa/disable")
def disable_two_factor(
    payload: TwoFactorDisableRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.disable_two_factor(current_user, payload.password)