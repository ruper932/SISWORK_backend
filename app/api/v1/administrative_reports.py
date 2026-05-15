from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.administrative_report import (
    AdministrativeReportCreateRequest,
    AdministrativeReportResponse,
    AdministrativeReportUpdateRequest,
)
from app.services.administrative_report_service import AdministrativeReportService

router = APIRouter(prefix="/administrative-reports", tags=["Administrative Reports"])


@router.get("", response_model=list[AdministrativeReportResponse])
def list_items(db: Session = Depends(get_db)):
    return AdministrativeReportService(db).list_items()


@router.get("/{item_id}", response_model=AdministrativeReportResponse)
def get_item(item_id: str, db: Session = Depends(get_db)):
    return AdministrativeReportService(db).get_item(item_id)


@router.post("", response_model=AdministrativeReportResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: AdministrativeReportCreateRequest, db: Session = Depends(get_db)):
    return AdministrativeReportService(db).create_item(payload)


@router.patch("/{item_id}", response_model=AdministrativeReportResponse)
def update_item(item_id: str, payload: AdministrativeReportUpdateRequest, db: Session = Depends(get_db)):
    return AdministrativeReportService(db).update_item(item_id, payload)


@router.delete("/{item_id}")
def delete_item(item_id: str, db: Session = Depends(get_db)):
    return AdministrativeReportService(db).delete_item(item_id)