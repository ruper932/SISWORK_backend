from fastapi import APIRouter

router = APIRouter()


@router.get("/dashboard", summary="Dashboard admin")
def admin_dashboard():
    return {
        "message": "Dashboard administrativo base",
    }