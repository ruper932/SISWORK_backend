from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserMeResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: str
    email_verified_at: datetime | None
    last_login_at: datetime | None