from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SavedProfessionalCreateRequest(BaseModel):
    user_id: UUID
    professional_profile_id: UUID


class SavedProfessionalResponse(BaseModel):
    id: UUID
    user_id: UUID
    professional_profile_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)