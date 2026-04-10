from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Listar calificaciones")
def list_ratings():
    return {
        "message": "Listado base de calificaciones",
        "items": [],
    }