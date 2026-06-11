from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.admin import router as admin_router
from app.api.v1.professionals import router as professionals_router
from app.api.v1.support import router as support_router
from app.api.v1.requests import router as requests_router
from app.api.v1.applications import router as applications_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.specialties import router as specialties_router

app = FastAPI(
    title="SISWORK API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(professionals_router)
app.include_router(support_router)
app.include_router(requests_router)
app.include_router(applications_router)
app.include_router(reviews_router)
app.include_router(specialties_router)