from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Listar especialidades")
def list_specialties():
    return {
        "message": "Listado base de especialidades",
        "items": [],
    }