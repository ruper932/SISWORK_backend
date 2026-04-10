from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Listar reportes")
def list_reports():
    return {
        "message": "Listado base de reportes",
        "items": [],
    }