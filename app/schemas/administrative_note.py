from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AdministrativeNoteCreateRequest(BaseModel):
    author_user_id: UUID
    related_entity: str
    related_entity_id: UUID
    note: str
    is_private: bool = True


class AdministrativeNoteUpdateRequest(BaseModel):
    note: str | None = None
    is_private: bool | None = None


class AdministrativeNoteResponse(BaseModel):
    id: UUID
    author_user_id: UUID
    related_entity: str
    related_entity_id: UUID
    note: str
    is_private: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)