from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Listar profesionales")
def list_professionals():
    return {
        "message": "Listado base de profesionales",
        "items": [],
    }