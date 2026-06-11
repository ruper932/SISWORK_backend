from __future__ import annotations

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.professional import (
    ProfessionalPublicResponse,
    VerificationRequestResponse,
)
from app.services.professional_service import ProfessionalService

router = APIRouter(
    prefix="/professionals",
    tags=["Professionals"],
)


@router.post(
    "/request-verification",
    response_model=VerificationRequestResponse,
)
async def request_verification(
    ci_photo: UploadFile = File(...),
    selfie_photo: UploadFile = File(...),
    certificate_pdf: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        verification_request = await ProfessionalService.request_verification(
            db=db,
            current_user=current_user,
            ci_photo=ci_photo,
            selfie_photo=selfie_photo,
            certificate_pdf=certificate_pdf,
        )
        return verification_request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "",
    response_model=List[ProfessionalPublicResponse],
)
def search_professionals(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None),
    specialty_id: Optional[uuid.UUID] = Query(default=None),
    city: Optional[str] = Query(default=None),
    zone: Optional[str] = Query(default=None),
    min_rating: Optional[float] = Query(default=None, ge=0, le=5),
    is_available: Optional[bool] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
):
    try:
        normalized_q = q.strip() if q and q.strip() else None

        return ProfessionalService.search_public_professionals(
            db=db,
            q=normalized_q,
            specialty_id=specialty_id,
            city=city,
            zone=zone,
            min_rating=min_rating,
            is_available=is_available,
            skip=skip,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/{user_ci}",
    response_model=ProfessionalPublicResponse,
)
def get_professional_detail(
    user_ci: str,
    db: Session = Depends(get_db),
):
    try:
        return ProfessionalService.get_public_professional_detail(db, user_ci)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))