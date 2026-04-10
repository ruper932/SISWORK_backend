from fastapi import APIRouter

router = APIRouter()


@router.get("/professionals", summary="Buscar profesionales")
def search_professionals():
    return {
        "message": "Búsqueda base de profesionales",
        "items": [],
    }