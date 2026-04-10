from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Listar postulaciones")
def list_applications():
    return {
        "message": "Listado base de postulaciones",
        "items": [],
    }