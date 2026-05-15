from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AdministrativeReportCreateRequest(BaseModel):
    generated_by_user_id: UUID
    report_type: str
    parameters_json: dict[str, Any] | None = None
    file_url: str | None = None


class AdministrativeReportUpdateRequest(BaseModel):
    report_type: str | None = None
    parameters_json: dict[str, Any] | None = None
    file_url: str | None = None


class AdministrativeReportResponse(BaseModel):
    id: UUID
    generated_by_user_id: UUID
    report_type: str
    parameters_json: dict | None
    generated_at: datetime
    file_url: str | None

    model_config = ConfigDict(from_attributes=True)