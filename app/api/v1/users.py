from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user

router = APIRouter()


@router.get("/me", summary="Usuario autenticado actual")
def get_me(current_user=Depends(get_current_user)):
    return {
        "message": "Usuario autenticado",
        "user": current_user,
    }