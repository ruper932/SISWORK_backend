from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Listar solicitudes")
def list_service_requests():
    return {
        "message": "Listado base de solicitudes",
        "items": [],
    }