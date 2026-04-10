from fastapi import APIRouter
from app.api.v1.dev import router as dev_router

from app.api.v1 import (
    admin,
    applications,
    audit,
    auth,
    professionals,
    ratings,
    reports,
    search,
    service_requests,
    specialties,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(professionals.router, prefix="/professionals", tags=["Professionals"])
api_router.include_router(specialties.router, prefix="/specialties", tags=["Specialties"])
api_router.include_router(service_requests.router, prefix="/service-requests", tags=["Service Requests"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])
api_router.include_router(dev_router, prefix="/dev", tags=["Dev"])