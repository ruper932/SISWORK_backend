from fastapi import APIRouter

from app.api.v1.administrative_notes import router as administrative_notes_router
from app.api.v1.administrative_reports import router as administrative_reports_router
from app.api.v1.auth import router as auth_router
from app.api.v1.certifications import router as certifications_router
from app.api.v1.health import router as health_router
from app.api.v1.professional_availabilities import router as professional_availabilities_router
from app.api.v1.professional_profiles import router as professional_profiles_router
from app.api.v1.professional_specialties import router as professional_specialties_router
from app.api.v1.professional_validation_queue import router as professional_validation_queue_router
from app.api.v1.professional_zones import router as professional_zones_router
from app.api.v1.saved_professionals import router as saved_professionals_router
from app.api.v1.search_history import router as search_history_router
from app.api.v1.service_applications import router as service_applications_router
from app.api.v1.service_contacts import router as service_contacts_router
from app.api.v1.service_ratings import router as service_ratings_router
from app.api.v1.service_requests import router as service_requests_router
from app.api.v1.specialties import router as specialties_router
from app.api.v1.user_addresses import router as user_addresses_router
from app.api.v1.users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(specialties_router)
api_router.include_router(professional_profiles_router)
api_router.include_router(professional_specialties_router)
api_router.include_router(professional_zones_router)
api_router.include_router(professional_availabilities_router)
api_router.include_router(certifications_router)
api_router.include_router(service_requests_router)
api_router.include_router(service_applications_router)
api_router.include_router(service_contacts_router)
api_router.include_router(service_ratings_router)
api_router.include_router(saved_professionals_router)
api_router.include_router(search_history_router)
api_router.include_router(professional_validation_queue_router)
api_router.include_router(administrative_notes_router)
api_router.include_router(administrative_reports_router)
api_router.include_router(user_addresses_router)