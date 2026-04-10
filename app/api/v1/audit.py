from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Listar auditoría")
def list_audit_logs():
    return {
        "message": "Listado base de auditoría",
        "items": [],
    }