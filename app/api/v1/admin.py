from fastapi import (
    APIRouter,
    Depends,
)

from app.api.deps.auth import require_roles

from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_roles(
            ["ADMIN", "SUPERADMIN"],
        )
    ),
):

    return {
        "message": "Welcome admin",
        "user": current_user.ci,
    }