from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SearchHistoryCreateRequest(BaseModel):
    user_id: UUID | None = None
    search_term: str | None = None
    specialty_id: UUID | None = None
    zone: str | None = None
    minimum_rating: Decimal | None = None
    available_now: bool | None = None
    results_count: int = 0


class SearchHistoryResponse(BaseModel):
    id: UUID
    user_id: UUID | None
    search_term: str | None
    specialty_id: UUID | None
    zone: str | None
    minimum_rating: Decimal | None
    available_now: bool | None
    results_count: int
    searched_at: datetime

    model_config = ConfigDict(from_attributes=True)