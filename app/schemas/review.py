from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    application_id: uuid.UUID
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=1000)


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID
    reviewer_ci: str
    reviewed_user_ci: str
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime