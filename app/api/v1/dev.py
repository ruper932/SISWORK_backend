from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.seeders.run_seeders import run_seeders

router = APIRouter()


@router.post("/seed", summary="Ejecutar seeders de desarrollo")
def seed_data(db: Session = Depends(get_db)):
    return run_seeders(db)