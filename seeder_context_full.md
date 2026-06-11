# Dump de archivos

## `app/db/database.py`

```python
from sqlalchemy import create_engine

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

from app.config import settings


DATABASE_URL = settings.DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    echo=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()
```

## `app/db/enums.py`

```python
import enum


class RoleEnum(str, enum.Enum):
    CLIENT = "CLIENT"
    PROFESSIONAL = "PROFESSIONAL"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    SUPERADMIN = "SUPERADMIN"


class VerificationStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class VerificationDocumentTypeEnum(str, enum.Enum):
    ID_CARD_FRONT = "ID_CARD_FRONT"
    ID_CARD_BACK = "ID_CARD_BACK"
    SELFIE = "SELFIE"
    CERTIFICATE = "CERTIFICATE"
    PDF_CERTIFICATION = "PDF_CERTIFICATION"


class RequestStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ApplicationStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class UrgencyLevelEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
```

## `app/db/__init__.py`

```python

```

## `app/db/mixins.py`

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class SoftDeleteMixin:

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class UUIDMixin:

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
```

## `app/db/session.py`

```python
from app.db.database import SessionLocal


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
```

## `app/models/application.py`

```python
import uuid

from sqlalchemy import (
    Text,
    ForeignKey,
    Numeric,
    Integer,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.models.mixins import TimestampMixin
from app.db.enums import (
    ApplicationStatusEnum,
)


class Application(
    Base,
    TimestampMixin,
):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("requests.id"),
        nullable=False,
        index=True,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    proposal_message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    proposed_price: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    estimated_time_hours: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[ApplicationStatusEnum] = mapped_column(
        Enum(
            ApplicationStatusEnum,
            name="application_status_enum",
        ),
        default=ApplicationStatusEnum.PENDING,
        nullable=False,
    )

    request = relationship(
        "Request",
        back_populates="applications",
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="applications",
    )

    reviews = relationship(
        "Review",
        back_populates="application",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "request_id",
            "professional_profile_id",
            name="uq_application_request_professional",
        ),
    )
```

## `app/models/audit_log.py`

```python

```

## `app/models/file.py`

```python
import uuid

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class File(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    uploaded_by_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    uploaded_by = relationship(
        "User",
    )
```

## `app/models/__init__.py`

```python
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole

from app.models.file import File

from app.models.specialty import Specialty
from app.models.professional_specialty import ProfessionalSpecialty

from app.models.professional_profile import ProfessionalProfile
from app.models.professional_availability import ProfessionalAvailability

from app.models.verification_request import VerificationRequest
from app.models.verification_document import VerificationDocument

from app.models.request import Request
from app.models.application import Application

from app.models.review import Review
```

## `app/models/mixins.py`

```python
from datetime import datetime, UTC

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from sqlalchemy import DateTime


class TimestampMixin:

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
```

## `app/models/professional_availability.py`

```python
import uuid
from datetime import time

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Time,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class ProfessionalAvailability(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "professional_availabilities"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "day_of_week",
            name="uq_professional_day",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="availabilities",
    )
```

## `app/models/professional_profile.py`

```python
import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.enums import VerificationStatusEnum
from app.db.mixins import TimestampMixin, SoftDeleteMixin


class ProfessionalProfile(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "professional_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        unique=True,
        nullable=False,
        index=True,
    )

    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    verification_status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(
            VerificationStatusEnum,
            name="verification_status_enum",
            create_type=True,
        ),
        default=VerificationStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    rating_average: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    rating_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="professional_profile",
    )

    verification_requests = relationship(
        "VerificationRequest",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    specialties = relationship(
        "ProfessionalSpecialty",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    applications = relationship(
        "Application",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )

    availabilities = relationship(
        "ProfessionalAvailability",
        back_populates="professional_profile",
        cascade="all, delete-orphan",
    )
```

## `app/models/professional_specialty.py`

```python
import uuid

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import TimestampMixin


class ProfessionalSpecialty(
    Base,
    TimestampMixin,
):
    __tablename__ = "professional_specialties"

    __table_args__ = (
        UniqueConstraint(
            "professional_profile_id",
            "specialty_id",
            name="uq_professional_specialty",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    specialty_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("specialties.id"),
        nullable=False,
        index=True,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
    )

    specialty = relationship(
        "Specialty",
        back_populates="professional_specialties",
    )
```

## `app/models/request.py`

```python
import uuid

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Numeric,
    DateTime,
    Enum,
    Boolean,
    Index,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.models.mixins import TimestampMixin
from app.db.enums import (
    RequestStatusEnum,
    UrgencyLevelEnum,
)


class Request(
    Base,
    TimestampMixin,
):
    __tablename__ = "requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    client_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    specialty_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("specialties.id"),
        nullable=False,
        index=True,
    )

    assigned_professional_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professional_profiles.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    budget: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    proposed_final_price: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    scheduled_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    zone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    urgency: Mapped[UrgencyLevelEnum] = mapped_column(
        Enum(
            UrgencyLevelEnum,
            name="urgency_level_enum",
        ),
        default=UrgencyLevelEnum.MEDIUM,
    )

    status: Mapped[RequestStatusEnum] = mapped_column(
        Enum(
            RequestStatusEnum,
            name="request_status_enum",
        ),
        default=RequestStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    is_review_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    cancellation_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    client = relationship(
        "User",
        foreign_keys=[client_ci],
    )

    specialty = relationship(
        "Specialty",
    )

    assigned_professional = relationship(
        "ProfessionalProfile",
        foreign_keys=[assigned_professional_profile_id],
    )

    applications = relationship(
        "Application",
        back_populates="request",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "idx_request_location",
            "city",
            "zone",
        ),
    )
```

## `app/models/review.py`

```python
import uuid

from sqlalchemy import (
    String,
    Text,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.models.mixins import TimestampMixin


class Review(
    Base,
    TimestampMixin,
):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id"),
        nullable=False,
        index=True,
    )

    reviewer_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
    )

    reviewed_user_ci: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.ci"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    application = relationship(
        "Application",
        back_populates="reviews",
    )

    reviewer = relationship(
        "User",
        foreign_keys=[reviewer_ci],
    )

    reviewed_user = relationship(
        "User",
        foreign_keys=[reviewed_user_ci],
    )
```

## `app/models/role.py`

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    user_roles = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )
```

## `app/models/specialty.py`

```python
import uuid

from sqlalchemy import (
    Boolean,
    String,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class Specialty(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "specialties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    professional_specialties = relationship(
        "ProfessionalSpecialty",
        back_populates="specialty",
        cascade="all, delete-orphan",
    )
```

## `app/models/user.py`

```python
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class User(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "users"

    ci: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    mother_last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    phone: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    whatsapp_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    profile_photo_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    zone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    user_roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    professional_profile = relationship(
        "ProfessionalProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
```

## `app/models/user_role.py`

```python
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.mixins import TimestampMixin


class UserRole(
    Base,
    TimestampMixin,
):
    __tablename__ = "user_roles"

    __table_args__ = (
        UniqueConstraint(
            "user_ci",
            "role_id",
            name="uq_user_role",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_ci: Mapped[str] = mapped_column(
        ForeignKey("users.ci"),
        nullable=False,
        index=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="user_roles",
    )

    role = relationship(
        "Role",
        back_populates="user_roles",
    )
```

## `app/models/verification_document.py`

```python
import uuid

from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import (
    ENUM,
    UUID,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.enums import VerificationDocumentTypeEnum
from app.db.mixins import TimestampMixin


class VerificationDocument(
    Base,
    TimestampMixin,
):
    __tablename__ = "verification_documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    verification_request_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("verification_requests.id"),
        nullable=False,
        index=True,
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("files.id"),
        nullable=False,
        index=True,
    )

    document_type: Mapped[VerificationDocumentTypeEnum] = mapped_column(
        ENUM(
            VerificationDocumentTypeEnum,
            name="verification_document_type_enum",
            create_type=True,
        ),
        nullable=False,
    )

    verification_request = relationship(
        "VerificationRequest",
        back_populates="documents",
    )

    file = relationship(
        "File",
    )
```

## `app/models/verification.py`

```python

```

## `app/models/verification_request.py`

```python
import uuid

from sqlalchemy import (
    ForeignKey,
    String,
)

from sqlalchemy.dialects.postgresql import (
    ENUM,
    UUID,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.enums import VerificationStatusEnum
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
)


class VerificationRequest(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
):
    __tablename__ = "verification_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    professional_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professional_profiles.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[VerificationStatusEnum] = mapped_column(
        ENUM(
            VerificationStatusEnum,
            name="verification_request_status_enum",
            create_type=True,
        ),
        default=VerificationStatusEnum.PENDING,
        nullable=False,
        index=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    reviewed_by_ci: Mapped[str | None] = mapped_column(
        ForeignKey("users.ci"),
        nullable=True,
    )

    professional_profile = relationship(
        "ProfessionalProfile",
    )

    reviewed_by = relationship(
        "User",
    )

    documents = relationship(
        "VerificationDocument",
        back_populates="verification_request",
        cascade="all, delete-orphan",
    )
```

## `app/services/application_service.py`

```python
from __future__ import annotations

from typing import List
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.enums import (
    ApplicationStatusEnum,
    RequestStatusEnum,
    RoleEnum,
    VerificationStatusEnum,
)
from app.models.application import Application
from app.models.professional_profile import ProfessionalProfile
from app.models.request import Request
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.application import ApplicationCreate


class ApplicationService:
    @staticmethod
    def _get_professional_profile(db: Session, current_user: User) -> ProfessionalProfile:
        stmt = select(ProfessionalProfile).where(ProfessionalProfile.user_ci == current_user.ci)
        profile = db.scalar(stmt)

        if not profile:
            raise Exception("Professional profile not found")

        if profile.verification_status != VerificationStatusEnum.APPROVED:
            raise Exception("Only verified professionals can apply to requests")

        if not profile.is_available:
            raise Exception("Professional is not available")

        return profile

    @staticmethod
    def create_application(
        db: Session,
        current_user: User,
        application_data: ApplicationCreate,
    ) -> Application:
        user_roles = RoleRepository.get_user_roles(db, current_user.ci)
        if RoleEnum.PROFESSIONAL.value not in user_roles:
            raise Exception("Only professionals can create applications")

        professional_profile = ApplicationService._get_professional_profile(db, current_user)

        request = db.get(Request, application_data.request_id)
        if not request:
            raise Exception("Request not found")

        if request.status != RequestStatusEnum.PENDING:
            raise Exception("Request is not available for applications")

        if request.client_ci == current_user.ci:
            raise Exception("You cannot apply to your own request")

        existing_application = ApplicationRepository.get_by_request_and_professional(
            db,
            application_data.request_id,
            professional_profile.id,
        )
        if existing_application:
            raise Exception("You have already applied to this request")

        application = Application(
            request_id=application_data.request_id,
            professional_profile_id=professional_profile.id,
            proposal_message=application_data.proposal_message,
            proposed_price=application_data.proposed_price,
            estimated_time_hours=application_data.estimated_time_hours,
            status=ApplicationStatusEnum.PENDING,
        )
        return ApplicationRepository.create(db, application)

    @staticmethod
    def get_application_by_id(db: Session, application_id: uuid.UUID) -> Application:
        application = ApplicationRepository.get_by_id(db, application_id)
        if not application:
            raise Exception("Application not found")
        return application

    @staticmethod
    def list_my_applications(db: Session, current_user: User) -> List[Application]:
        professional_profile = ApplicationService._get_professional_profile(db, current_user)
        return ApplicationRepository.list_by_professional(db, professional_profile.id)

    @staticmethod
    def list_request_applications(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
    ) -> List[Application]:
        request = db.get(Request, request_id)
        if not request:
            raise Exception("Request not found")

        if request.client_ci != current_user.ci:
            raise Exception("You do not have permission to view these applications")

        return ApplicationRepository.list_by_request(db, request_id)

    @staticmethod
    def accept_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Application:
        application = ApplicationRepository.get_by_id_for_request_owner(
            db,
            application_id,
            current_user.ci,
        )
        if not application:
            raise Exception("Application not found")

        request = application.request
        if request.status != RequestStatusEnum.PENDING:
            raise Exception("Request is no longer available for assignment")

        pending_applications = ApplicationRepository.list_by_request(db, request.id)

        for item in pending_applications:
            if item.id == application.id:
                item.status = ApplicationStatusEnum.ACCEPTED
            elif item.status == ApplicationStatusEnum.PENDING:
                item.status = ApplicationStatusEnum.REJECTED

        request.assigned_professional_profile_id = application.professional_profile_id
        request.status = RequestStatusEnum.ASSIGNED
        request.proposed_final_price = application.proposed_price

        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def reject_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Application:
        application = ApplicationRepository.get_by_id_for_request_owner(
            db,
            application_id,
            current_user.ci,
        )
        if not application:
            raise Exception("Application not found")

        if application.status != ApplicationStatusEnum.PENDING:
            raise Exception("Only pending applications can be rejected")

        application.status = ApplicationStatusEnum.REJECTED
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def cancel_my_application(
        db: Session,
        current_user: User,
        application_id: uuid.UUID,
    ) -> Application:
        professional_profile = ApplicationService._get_professional_profile(db, current_user)

        application = ApplicationRepository.get_by_id_for_professional(
            db,
            application_id,
            professional_profile.id,
        )
        if not application:
            raise Exception("Application not found")

        if application.status != ApplicationStatusEnum.PENDING:
            raise Exception("Only pending applications can be cancelled")

        application.status = ApplicationStatusEnum.CANCELLED
        db.commit()
        db.refresh(application)
        return application
```

## `app/services/auth_service.py`

```python
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.models.user_role import UserRole

from app.repositories.role_repository import RoleRepository

class AuthService:

    @staticmethod
    def register(
        db,
        user_data,
    ):

        existing_user = UserRepository.get_by_ci(
            db,
            user_data.ci,
        )

        if existing_user:
            raise Exception("CI already registered")

        existing_email = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing_email:
            raise Exception("Email already registered")

        user = User(
            ci=user_data.ci,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            mother_last_name=user_data.mother_last_name,
            birth_date=user_data.birth_date,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hash_password(
                user_data.password
            ),
            city=user_data.city,
            zone=user_data.zone,
        )

        db.add(user)

        client_role = RoleRepository.get_by_name(
            db,
            "CLIENT",
        )

        if not client_role:
            raise Exception(
                "CLIENT role does not exist"
            )

        user_role = UserRole(
            user_ci=user.ci,
            role_id=client_role.id,
        )

        db.add(user_role)

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def login(
        db,
        identifier: str,
        password: str,
    ):

        user = UserRepository.get_by_ci_or_email(
            db,
            identifier,
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        access_token = create_access_token(
            subject=user.ci,
        )

        return access_token
```

## `app/services/__init__.py`

```python

```

## `app/services/professional_service.py`

```python
from __future__ import annotations

import os
import uuid
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy import select

from app.models.file import File
from app.models.professional_profile import ProfessionalProfile
from app.models.professional_specialty import ProfessionalSpecialty
from app.models.specialty import Specialty
from app.models.user import User
from app.models.verification_document import VerificationDocument
from app.models.verification_request import VerificationRequest
from app.repositories.professional_repository import ProfessionalRepository
from app.schemas.professional import ProfessionalPublicResponse
from app.db.enums import VerificationStatusEnum, VerificationDocumentTypeEnum

UPLOAD_DIR = "uploads/verification"


class ProfessionalService:
    @staticmethod
    async def request_verification(db, current_user, ci_photo: UploadFile, selfie_photo: UploadFile, certificate_pdf: UploadFile):
        existing_profile = db.scalar(
            select(ProfessionalProfile).where(ProfessionalProfile.user_ci == current_user.ci)
        )

        if not existing_profile:
            profile = ProfessionalProfile(
                user_ci=current_user.ci,
                verification_status=VerificationStatusEnum.PENDING,
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        else:
            profile = existing_profile

        verification_request = VerificationRequest(
            professional_profile_id=profile.id,
            status=VerificationStatusEnum.PENDING,
        )
        db.add(verification_request)
        db.commit()
        db.refresh(verification_request)

        files_data = [
            (ci_photo, VerificationDocumentTypeEnum.ID_CARD_FRONT),
            (selfie_photo, VerificationDocumentTypeEnum.SELFIE),
            (certificate_pdf, VerificationDocumentTypeEnum.PDF_CERTIFICATION),
        ]

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        for upload_file, doc_type in files_data:
            extension = upload_file.filename.split(".")[-1]
            generated_name = f"{uuid.uuid4()}.{extension}"
            file_path = os.path.join(UPLOAD_DIR, generated_name)

            content = await upload_file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)

            file_record = File(
                uploaded_by_ci=current_user.ci,
                original_filename=upload_file.filename,
                stored_filename=generated_name,
                file_path=file_path,
                mimetype=upload_file.content_type,
                file_size=len(content),
            )
            db.add(file_record)
            db.commit()
            db.refresh(file_record)

            verification_document = VerificationDocument(
                verification_request_id=verification_request.id,
                file_id=file_record.id,
                document_type=doc_type,
            )
            db.add(verification_document)
            db.commit()

        return verification_request

    @staticmethod
    def search_public_professionals(
        db,
        q: Optional[str] = None,
        specialty_id: Optional[uuid.UUID] = None,
        city: Optional[str] = None,
        zone: Optional[str] = None,
        min_rating: Optional[float] = None,
        is_available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ):
        profiles = ProfessionalRepository.search_public_professionals(
            db=db,
            q=q,
            specialty_id=specialty_id,
            city=city,
            zone=zone,
            min_rating=min_rating,
            is_available=is_available,
            skip=skip,
            limit=limit,
        )

        results = []
        for profile in profiles:
            full_name_parts = [
                profile.user.firstname,
                profile.user.lastname,
                profile.user.mother_lastname,
            ]
            full_name = " ".join([part for part in full_name_parts if part])

            specialties = []
            for item in profile.specialties:
                if item.specialty:
                    specialties.append(
                        {
                            "id": item.specialty.id,
                            "name": item.specialty.name,
                            "description": item.specialty.description,
                        }
                    )

            availabilities = []
            for item in profile.availabilities:
                availabilities.append(
                    {
                        "id": item.id,
                        "day_of_week": item.day_of_week,
                        "start_time": item.start_time,
                        "end_time": item.end_time,
                        "is_active": item.is_active,
                    }
                )

            results.append(
                {
                    "id": profile.id,
                    "user_ci": profile.user_ci,
                    "full_name": full_name,
                    "bio": profile.bio,
                    "experience_years": profile.experience_years,
                    "verification_status": profile.verification_status,
                    "rating_average": profile.rating_average,
                    "rating_count": profile.rating_count,
                    "is_available": profile.is_available,
                    "city": profile.user.city,
                    "zone": profile.user.zone,
                    "specialties": specialties,
                    "availabilities": availabilities,
                }
            )

        return results

    @staticmethod
    def get_public_professional_detail(db, user_ci: str):
        profile = ProfessionalRepository.get_by_user_ci(db, user_ci)
        if not profile:
            raise Exception("Professional profile not found")

        if profile.verification_status != VerificationStatusEnum.APPROVED:
            raise Exception("Professional profile is not public")

        full_name_parts = [
            profile.user.firstname,
            profile.user.lastname,
            profile.user.mother_lastname,
        ]
        full_name = " ".join([part for part in full_name_parts if part])

        specialties = []
        for item in profile.specialties:
            if item.specialty:
                specialties.append(
                    {
                        "id": item.specialty.id,
                        "name": item.specialty.name,
                        "description": item.specialty.description,
                    }
                )

        availabilities = []
        for item in profile.availabilities:
            availabilities.append(
                {
                    "id": item.id,
                    "day_of_week": item.day_of_week,
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                    "is_active": item.is_active,
                }
            )

        return {
            "id": profile.id,
            "user_ci": profile.user_ci,
            "full_name": full_name,
            "bio": profile.bio,
            "experience_years": profile.experience_years,
            "verification_status": profile.verification_status,
            "rating_average": profile.rating_average,
            "rating_count": profile.rating_count,
            "is_available": profile.is_available,
            "city": profile.user.city,
            "zone": profile.user.zone,
            "specialties": specialties,
            "availabilities": availabilities,
        }
```

## `app/services/request_service.py`

```python
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.enums import (
    RequestStatusEnum,
    RoleEnum,
    ApplicationStatusEnum,
    UrgencyLevelEnum,
)
from app.models.application import Application
from app.models.request import Request
from app.models.specialty import Specialty
from app.models.user import User
from app.repositories.request_repository import RequestRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.request import RequestCreate, RequestUpdate


class RequestService:
    @staticmethod
    def create_request(db: Session, current_user: User, request_data: RequestCreate) -> Request:
        user_roles = RoleRepository.get_user_roles(db, current_user.ci)
        if RoleEnum.CLIENT.value not in user_roles:
            raise Exception("Only clients can create requests")

        specialty = db.get(Specialty, request_data.specialty_id)
        if not specialty or not specialty.is_active:
            raise Exception("Specialty not found or inactive")

        request = Request(
            client_ci=current_user.ci,
            specialty_id=request_data.specialty_id,
            title=request_data.title,
            description=request_data.description,
            budget=request_data.budget,
            proposed_final_price=request_data.proposed_final_price,
            scheduled_date=request_data.scheduled_date,
            city=request_data.city,
            zone=request_data.zone,
            latitude=request_data.latitude,
            longitude=request_data.longitude,
            urgency=request_data.urgency,
            status=RequestStatusEnum.PENDING,
            is_review_enabled=False,
        )
        return RequestRepository.create(db, request)

    @staticmethod
    def get_request_by_id(db: Session, request_id: uuid.UUID) -> Request:
        request = RequestRepository.get_by_id(db, request_id)
        if not request:
            raise Exception("Request not found")
        return request

    @staticmethod
    def list_public_requests(db: Session, skip: int = 0, limit: int = 50):
        return RequestRepository.list_public_open_requests(db, skip=skip, limit=limit)

    @staticmethod
    def search_public_requests(
        db: Session,
        q: str | None = None,
        specialty_id: uuid.UUID | None = None,
        city: str | None = None,
        zone: str | None = None,
        urgency: UrgencyLevelEnum | None = None,
        skip: int = 0,
        limit: int = 50,
    ):
        return RequestRepository.search_public_requests(
            db=db,
            q=q,
            specialty_id=specialty_id,
            city=city,
            zone=zone,
            urgency=urgency,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def list_my_requests(db: Session, current_user: User, skip: int = 0, limit: int = 50):
        return RequestRepository.list_by_client(db, current_user.ci, skip=skip, limit=limit)

    @staticmethod
    def update_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
        request_data: RequestUpdate,
    ) -> Request:
        request = RequestRepository.get_by_id_for_owner(db, request_id, current_user.ci)
        if not request:
            raise Exception("Request not found")

        if request.status != RequestStatusEnum.PENDING:
            raise Exception("Only pending requests can be updated")

        if request_data.specialty_id is not None:
            specialty = db.get(Specialty, request_data.specialty_id)
            if not specialty or not specialty.is_active:
                raise Exception("Specialty not found or inactive")
            request.specialty_id = request_data.specialty_id

        if request_data.title is not None:
            request.title = request_data.title

        if request_data.description is not None:
            request.description = request_data.description

        if request_data.budget is not None:
            request.budget = request_data.budget

        if request_data.proposed_final_price is not None:
            request.proposed_final_price = request_data.proposed_final_price

        if request_data.scheduled_date is not None:
            request.scheduled_date = request_data.scheduled_date

        if request_data.city is not None:
            request.city = request_data.city

        if request_data.zone is not None:
            request.zone = request_data.zone

        if request_data.latitude is not None:
            request.latitude = request_data.latitude

        if request_data.longitude is not None:
            request.longitude = request_data.longitude

        if request_data.urgency is not None:
            request.urgency = request_data.urgency

        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def cancel_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
        cancellation_reason: str | None = None,
    ) -> Request:
        request = RequestRepository.get_by_id_for_owner(db, request_id, current_user.ci)
        if not request:
            raise Exception("Request not found")

        if request.status in [RequestStatusEnum.COMPLETED, RequestStatusEnum.CANCELLED]:
            raise Exception("Request cannot be cancelled")

        request.status = RequestStatusEnum.CANCELLED
        request.cancellation_reason = cancellation_reason or "Cancelled by client"

        pending_or_accepted_applications = db.scalars(
            select(Application).where(
                Application.request_id == request.id,
                Application.status.in_([
                    ApplicationStatusEnum.PENDING,
                    ApplicationStatusEnum.ACCEPTED,
                ]),
            )
        ).all()

        for application in pending_or_accepted_applications:
            application.status = ApplicationStatusEnum.CANCELLED

        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def start_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
    ) -> Request:
        request = RequestRepository.get_by_id(db, request_id)
        if not request:
            raise Exception("Request not found")

        is_client = request.client_ci == current_user.ci
        is_assigned_professional = (
            request.assigned_professional is not None
            and request.assigned_professional.user_ci == current_user.ci
        )

        if not is_client and not is_assigned_professional:
            raise Exception("You do not have permission to start this request")

        if request.status != RequestStatusEnum.ASSIGNED:
            raise Exception("Only assigned requests can be started")

        accepted_application = db.scalar(
            select(Application).where(
                Application.request_id == request.id,
                Application.status == ApplicationStatusEnum.ACCEPTED,
            )
        )
        if not accepted_application:
            raise Exception("Accepted application not found for this request")

        request.status = RequestStatusEnum.IN_PROGRESS
        db.commit()
        db.refresh(request)
        return request

    @staticmethod
    def complete_request(
        db: Session,
        current_user: User,
        request_id: uuid.UUID,
    ) -> Request:
        request = RequestRepository.get_by_id(db, request_id)
        if not request:
            raise Exception("Request not found")

        is_client = request.client_ci == current_user.ci
        is_assigned_professional = (
            request.assigned_professional is not None
            and request.assigned_professional.user_ci == current_user.ci
        )

        if not is_client and not is_assigned_professional:
            raise Exception("You do not have permission to complete this request")

        if request.status != RequestStatusEnum.IN_PROGRESS:
            raise Exception("Only requests in progress can be completed")

        accepted_application = db.scalar(
            select(Application).where(
                Application.request_id == request.id,
                Application.status == ApplicationStatusEnum.ACCEPTED,
            )
        )
        if not accepted_application:
            raise Exception("Accepted application not found for this request")

        request.status = RequestStatusEnum.COMPLETED
        request.is_review_enabled = True
        accepted_application.status = ApplicationStatusEnum.COMPLETED

        db.commit()
        db.refresh(request)
        return request
```

## `app/services/review_service.py`

```python
from __future__ import annotations

from typing import List
import uuid

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.professional_profile import ProfessionalProfile
from app.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate
from app.db.enums import ApplicationStatusEnum, RequestStatusEnum


class ReviewService:
    @staticmethod
    def create_review(
        db: Session,
        current_user,
        review_data: ReviewCreate,
    ) -> Review:
        application = db.scalar(
            select(Application).where(Application.id == review_data.application_id)
        )
        if not application:
            raise Exception("Application not found")

        request = application.request
        if not request:
            raise Exception("Request not found")

        if request.status != RequestStatusEnum.COMPLETED:
            raise Exception("Reviews are only allowed for completed requests")

        if not request.is_review_enabled:
            raise Exception("Reviews are not enabled for this request")

        if application.status != ApplicationStatusEnum.COMPLETED:
            raise Exception("Only completed applications can be reviewed")

        existing_review = ReviewRepository.get_by_application_and_reviewer(
            db,
            review_data.application_id,
            current_user.ci,
        )
        if existing_review:
            raise Exception("You have already reviewed this application")

        assigned_profile = application.professional_profile
        if not assigned_profile:
            raise Exception("Professional profile not found")

        is_client = request.client_ci == current_user.ci
        is_professional = assigned_profile.user_ci == current_user.ci

        if not is_client and not is_professional:
            raise Exception("You do not have permission to review this application")

        reviewed_user_ci = assigned_profile.user_ci if is_client else request.client_ci

        if reviewed_user_ci == current_user.ci:
            raise Exception("You cannot review yourself")

        review = Review(
            application_id=review_data.application_id,
            reviewer_ci=current_user.ci,
            reviewed_user_ci=reviewed_user_ci,
            rating=review_data.rating,
            comment=review_data.comment,
        )
        created_review = ReviewRepository.create(db, review)

        if reviewed_user_ci == assigned_profile.user_ci:
            ReviewService._recalculate_professional_rating(db, assigned_profile.id)

        return created_review

    @staticmethod
    def get_review_by_id(db: Session, review_id: uuid.UUID) -> Review:
        review = ReviewRepository.get_by_id(db, review_id)
        if not review:
            raise Exception("Review not found")
        return review

    @staticmethod
    def list_reviews_for_me(db: Session, current_user) -> List[Review]:
        return ReviewRepository.list_by_reviewed_user(db, current_user.ci)

    @staticmethod
    def _recalculate_professional_rating(db: Session, professional_profile_id: uuid.UUID) -> None:
        profile = db.scalar(
            select(ProfessionalProfile).where(ProfessionalProfile.id == professional_profile_id)
        )
        if not profile:
            return

        stmt = (
            select(func.avg(Review.rating), func.count(Review.id))
            .join(Application, Application.id == Review.application_id)
            .where(Application.professional_profile_id == professional_profile_id)
        )
        avg_rating, rating_count = db.execute(stmt).one()

        profile.rating_average = float(avg_rating or 0.0)
        profile.rating_count = int(rating_count or 0)

        db.commit()
```

## `app/services/verification_service.py`

```python
from sqlalchemy import select

from app.models.role import Role

from app.models.user_role import UserRole

from app.models.professional_profile import (
    ProfessionalProfile,
)

from app.models.verification_request import (
    VerificationRequest,
)

from app.db.enums import VerificationStatusEnum


class VerificationService:

    @staticmethod
    def approve_verification(
        db,
        verification_request_id,
        reviewer_ci,
    ):

        verification_request = db.scalar(
            select(VerificationRequest).where(
                VerificationRequest.id
                == verification_request_id
            )
        )

        if not verification_request:
            raise Exception(
                "Verification request not found"
            )

        verification_request.status = (
            VerificationStatusEnum.APPROVED
        )

        verification_request.reviewed_by_ci = (
            reviewer_ci
        )

        profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id
                == verification_request.professional_profile_id
            )
        )

        profile.verification_status = (
            VerificationStatusEnum.APPROVED
        )

        role = db.scalar(
            select(Role).where(
                Role.name == "PROFESSIONAL"
            )
        )

        existing_role = db.scalar(
            select(UserRole).where(
                UserRole.user_ci == profile.user_ci,
                UserRole.role_id == role.id,
            )
        )

        if not existing_role:

            user_role = UserRole(
                user_ci=profile.user_ci,
                role_id=role.id,
            )

            db.add(user_role)

        db.commit()

        return verification_request

    @staticmethod
    def reject_verification(
        db,
        verification_request_id,
        reviewer_ci,
        rejection_reason,
    ):

        verification_request = db.scalar(
            select(VerificationRequest).where(
                VerificationRequest.id
                == verification_request_id
            )
        )

        if not verification_request:
            raise Exception(
                "Verification request not found"
            )

        verification_request.status = (
            VerificationStatusEnum.REJECTED
        )

        verification_request.reviewed_by_ci = (
            reviewer_ci
        )

        verification_request.rejection_reason = (
            rejection_reason
        )

        profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id
                == verification_request.professional_profile_id
            )
        )

        profile.verification_status = (
            VerificationStatusEnum.REJECTED
        )

        db.commit()

        return verification_request
```

## `scripts/seed_demo_data.py`

```python
from __future__ import annotations

import random
from datetime import date, datetime, timedelta, time, UTC
from decimal import Decimal
from typing import Iterable

from sqlalchemy import select, func

from app.core.security import hashpassword
from app.db.enums import (
    ApplicationStatusEnum,
    RequestStatusEnum,
    RoleEnum,
    UrgencyLevelEnum,
    VerificationStatusEnum,
)
from app.db.session import SessionLocal
from app.models.application import Application
from app.models.professionalavailability import ProfessionalAvailability
from app.models.professionalprofile import ProfessionalProfile
from app.models.professionalspecialty import ProfessionalSpecialty
from app.models.request import Request
from app.models.review import Review
from app.models.role import Role
from app.models.specialty import Specialty
from app.models.user import User
from app.models.userrole import UserRole


RANDOM_SEED = 42
DEFAULT_PASSWORD = "demons312es"


SPECIALTIES = [
    ("Electricista", "Instalaciones eléctricas, tomacorrientes, tableros y mantenimiento."),
    ("Plomería", "Reparación de fugas, grifería, tuberías y sanitarios."),
    ("Albañilería", "Obra fina, refacciones, revoque y ampliaciones."),
    ("Pintura", "Pintado interior y exterior, resanes y acabados."),
    ("Carpintería", "Muebles, puertas, closets y estructuras de madera."),
    ("Cerrajería", "Apertura, cambio de chapas, cerraduras y refuerzos."),
    ("Jardinería", "Mantenimiento de jardines, poda y diseño básico."),
    ("Limpieza", "Limpieza profunda, postobra y mantenimiento doméstico."),
    ("Gasfitería", "Instalaciones de gas, revisiones y mantenimiento."),
    ("Técnico de electrodomésticos", "Reparación de lavadoras, refrigeradores y cocinas."),
    ("Soldadura", "Rejas, estructuras metálicas y reparaciones."),
    ("Yesero", "Cielos falsos, yeso y terminaciones interiores."),
]

CLIENTS = [
    {
        "ci": "CLI1001",
        "firstname": "María",
        "lastname": "Lopez",
        "motherlastname": "Quispe",
        "birthdate": date(1992, 3, 15),
        "email": "maria.lopez@siswork.demo",
        "phone": "71000001",
        "city": "La Paz",
        "zone": "Sopocachi",
        "latitude": -16.5111,
        "longitude": -68.1246,
    },
    {
        "ci": "CLI1002",
        "firstname": "Carlos",
        "lastname": "Fernandez",
        "motherlastname": "Rojas",
        "birthdate": date(1988, 7, 11),
        "email": "carlos.fernandez@siswork.demo",
        "phone": "71000002",
        "city": "La Paz",
        "zone": "Miraflores",
        "latitude": -16.4998,
        "longitude": -68.1193,
    },
    {
        "ci": "CLI1003",
        "firstname": "Lucía",
        "lastname": "Mamani",
        "motherlastname": "Flores",
        "birthdate": date(1995, 1, 22),
        "email": "lucia.mamani@siswork.demo",
        "phone": "71000003",
        "city": "La Paz",
        "zone": "Calacoto",
        "latitude": -16.5348,
        "longitude": -68.0875,
    },
    {
        "ci": "CLI1004",
        "firstname": "Andrés",
        "lastname": "Vargas",
        "motherlastname": "Mendoza",
        "birthdate": date(1990, 9, 2),
        "email": "andres.vargas@siswork.demo",
        "phone": "71000004",
        "city": "La Paz",
        "zone": "San Miguel",
        "latitude": -16.5400,
        "longitude": -68.0770,
    },
    {
        "ci": "CLI1005",
        "firstname": "Daniela",
        "lastname": "Choque",
        "motherlastname": "Nina",
        "birthdate": date(1994, 6, 18),
        "email": "daniela.choque@siswork.demo",
        "phone": "71000005",
        "city": "La Paz",
        "zone": "Achumani",
        "latitude": -16.5533,
        "longitude": -68.0642,
    },
    {
        "ci": "CLI1006",
        "firstname": "José",
        "lastname": "Rivera",
        "motherlastname": "Aliaga",
        "birthdate": date(1987, 11, 5),
        "email": "jose.rivera@siswork.demo",
        "phone": "71000006",
        "city": "El Alto",
        "zone": "Ciudad Satélite",
        "latitude": -16.5130,
        "longitude": -68.1637,
    },
    {
        "ci": "CLI1007",
        "firstname": "Paola",
        "lastname": "Torrez",
        "motherlastname": "Gutiérrez",
        "birthdate": date(1991, 12, 8),
        "email": "paola.torrez@siswork.demo",
        "phone": "71000007",
        "city": "La Paz",
        "zone": "Obrajes",
        "latitude": -16.5231,
        "longitude": -68.1022,
    },
    {
        "ci": "CLI1008",
        "firstname": "Miguel",
        "lastname": "Soria",
        "motherlastname": "Lima",
        "birthdate": date(1989, 4, 9),
        "email": "miguel.soria@siswork.demo",
        "phone": "71000008",
        "city": "La Paz",
        "zone": "Villa Fátima",
        "latitude": -16.4795,
        "longitude": -68.1132,
    },
    {
        "ci": "CLI1009",
        "firstname": "Valeria",
        "lastname": "Calle",
        "motherlastname": "Paredes",
        "birthdate": date(1996, 2, 12),
        "email": "valeria.calle@siswork.demo",
        "phone": "71000009",
        "city": "La Paz",
        "zone": "Centro",
        "latitude": -16.4959,
        "longitude": -68.1336,
    },
    {
        "ci": "CLI1010",
        "firstname": "Raúl",
        "lastname": "Condori",
        "motherlastname": "Apaza",
        "birthdate": date(1986, 8, 29),
        "email": "raul.condori@siswork.demo",
        "phone": "71000010",
        "city": "El Alto",
        "zone": "16 de Julio",
        "latitude": -16.4951,
        "longitude": -68.1942,
    },
]

PROFESSIONALS = [
    {
        "ci": "PRO2001",
        "firstname": "Jorge",
        "lastname": "Mendoza",
        "motherlastname": "Quisbert",
        "birthdate": date(1985, 5, 10),
        "email": "jorge.mendoza@siswork.demo",
        "phone": "72000001",
        "city": "La Paz",
        "zone": "Sopocachi",
        "latitude": -16.5120,
        "longitude": -68.1280,
        "bio": "Electricista con experiencia en instalaciones domiciliarias, tableros y mantenimiento preventivo.",
        "experience_years": 12,
        "is_available": True,
        "specialties": ["Electricista"],
    },
    {
        "ci": "PRO2002",
        "firstname": "Patricia",
        "lastname": "Luna",
        "motherlastname": "Mamani",
        "birthdate": date(1990, 1, 20),
        "email": "patricia.luna@siswork.demo",
        "phone": "72000002",
        "city": "La Paz",
        "zone": "Miraflores",
        "latitude": -16.5005,
        "longitude": -68.1189,
        "bio": "Especialista en plomería, cambio de grifería, fugas y mantenimiento de baños y cocinas.",
        "experience_years": 8,
        "is_available": True,
        "specialties": ["Plomería", "Gasfitería"],
    },
    {
        "ci": "PRO2003",
        "firstname": "Wilson",
        "lastname": "Choque",
        "motherlastname": "Ticona",
        "birthdate": date(1983, 6, 14),
        "email": "wilson.choque@siswork.demo",
        "phone": "72000003",
        "city": "El Alto",
        "zone": "Ciudad Satélite",
        "latitude": -16.5121,
        "longitude": -68.1645,
        "bio": "Maestro albañil para refacciones, ampliaciones, obra fina y mantenimiento general.",
        "experience_years": 15,
        "is_available": True,
        "specialties": ["Albañilería", "Yesero"],
    },
    {
        "ci": "PRO2004",
        "firstname": "Carla",
        "lastname": "Rojas",
        "motherlastname": "Flores",
        "birthdate": date(1992, 3, 7),
        "email": "carla.rojas@siswork.demo",
        "phone": "72000004",
        "city": "La Paz",
        "zone": "Calacoto",
        "latitude": -16.5340,
        "longitude": -68.0881,
        "bio": "Pintora de interiores y exteriores, con enfoque en acabados limpios y resane de muros.",
        "experience_years": 7,
        "is_available": True,
        "specialties": ["Pintura"],
    },
    {
        "ci": "PRO2005",
        "firstname": "Eduardo",
        "lastname": "Paredes",
        "motherlastname": "Cruz",
        "birthdate": date(1987, 9, 1),
        "email": "eduardo.paredes@siswork.demo",
        "phone": "72000005",
        "city": "La Paz",
        "zone": "San Miguel",
        "latitude": -16.5392,
        "longitude": -68.0765,
        "bio": "Carpintero para muebles a medida, puertas, closets y reparaciones de madera.",
        "experience_years": 10,
        "is_available": True,
        "specialties": ["Carpintería"],
    },
    {
        "ci": "PRO2006",
        "firstname": "Roxana",
        "lastname": "Arce",
        "motherlastname": "Salazar",
        "birthdate": date(1991, 8, 30),
        "email": "roxana.arce@siswork.demo",
        "phone": "72000006",
        "city": "La Paz",
        "zone": "Obrajes",
        "latitude": -16.5227,
        "longitude": -68.1030,
        "bio": "Servicio de limpieza profunda, postobra y mantenimiento de departamentos y oficinas.",
        "experience_years": 6,
        "is_available": True,
        "specialties": ["Limpieza"],
    },
    {
        "ci": "PRO2007",
        "firstname": "Luis",
        "lastname": "Acuña",
        "motherlastname": "Vargas",
        "birthdate": date(1984, 12, 17),
        "email": "luis.acuna@siswork.demo",
        "phone": "72000007",
        "city": "El Alto",
        "zone": "16 de Julio",
        "latitude": -16.4962,
        "longitude": -68.1935,
        "bio": "Cerrajero con atención rápida para apertura, cambio de chapas y refuerzo de puertas.",
        "experience_years": 11,
        "is_available": True,
        "specialties": ["Cerrajería"],
    },
    {
        "ci": "PRO2008",
        "firstname": "Mónica",
        "lastname": "Quiroga",
        "motherlastname": "Navia",
        "birthdate": date(1989, 10, 26),
        "email": "monica.quiroga@siswork.demo",
        "phone": "72000008",
        "city": "La Paz",
        "zone": "Achumani",
        "latitude": -16.5525,
        "longitude": -68.0635,
        "bio": "Jardinera para poda, mantenimiento y mejora estética de jardines y patios.",
        "experience_years": 9,
        "is_available": True,
        "specialties": ["Jardinería"],
    },
    {
        "ci": "PRO2009",
        "firstname": "Sergio",
        "lastname": "Velasco",
        "motherlastname": "Peñaranda",
        "birthdate": date(1986, 2, 3),
        "email": "sergio.velasco@siswork.demo",
        "phone": "72000009",
        "city": "La Paz",
        "zone": "Villa Fátima",
        "latitude": -16.4803,
        "longitude": -68.1127,
        "bio": "Técnico en electrodomésticos con experiencia en línea blanca y mantenimiento correctivo.",
        "experience_years": 13,
        "is_available": True,
        "specialties": ["Técnico de electrodomésticos"],
    },
    {
        "ci": "PRO2010",
        "firstname": "Ana",
        "lastname": "Condori",
        "motherlastname": "López",
        "birthdate": date(1993, 11, 19),
        "email": "ana.condori@siswork.demo",
        "phone": "72000010",
        "city": "La Paz",
        "zone": "Centro",
        "latitude": -16.4950,
        "longitude": -68.1341,
        "bio": "Soldadora y técnica en estructuras metálicas, rejas, barandas y reparaciones.",
        "experience_years": 7,
        "is_available": True,
        "specialties": ["Soldadura"],
    },
]

REQUEST_TEMPLATES = [
    ("Cambio de instalación eléctrica en cocina", "Necesito revisar cableado, cambiar tomas y asegurar que el tablero soporte nuevos equipos."),
    ("Reparación de fuga en baño principal", "Hay una fuga constante debajo del lavamanos y también se debe revisar la presión del agua."),
    ("Pintado completo de departamento", "Busco pintar sala, comedor y dos habitaciones con resane previo de grietas pequeñas."),
    ("Armado de muebles de cocina", "Necesito apoyo para instalar módulos nuevos y ajustar puertas de melamina."),
    ("Cambio de chapa principal", "La cerradura principal falla y necesito una solución segura el mismo día."),
    ("Mantenimiento de jardín delantero", "Poda, limpieza, retiro de maleza y recomendación para mejorar el diseño del espacio."),
    ("Refacción de pared con humedad", "Una pared presenta humedad y desprendimiento de yeso. Se requiere evaluación y reparación."),
    ("Limpieza profunda post obra", "Necesito limpieza profunda después de una remodelación, incluyendo polvo fino y residuos."),
    ("Revisión de cocina a gas", "Se requiere inspección de conexiones y cambio de una válvula con fuga."),
    ("Reparación de refrigerador", "El refrigerador dejó de enfriar correctamente y hace ruido al encender."),
    ("Instalación de reja metálica", "Necesito fabricar e instalar una reja para ventana con medidas específicas."),
    ("Cambio de puertas de closet", "Quiero reemplazar puertas antiguas y nivelar rieles en un closet empotrado."),
    ("Nivelación y acabado de muro", "Se debe emparejar un muro interior y dejarlo listo para pintar."),
    ("Instalación de lámparas y apliques", "Colocar tres lámparas, dos apliques y revisar una llave térmica."),
    ("Mantenimiento integral de baño", "Cambio de grifería, ajuste de sanitario y revisión de filtraciones menores."),
]

REVIEW_COMMENTS = [
    "Excelente trabajo, llegó puntual y dejó todo funcionando correctamente.",
    "Muy buena atención y explicación clara del problema y la solución.",
    "Cumplió con el tiempo acordado y el acabado fue mejor de lo esperado.",
    "Trabajo responsable, ordenado y con buena comunicación en todo momento.",
    "Recomendado, resolvió el problema sin complicaciones y con buen trato.",
    "Muy profesional, cuidó los detalles y dejó el área limpia.",
    "Buena experiencia, volvería a contratar este servicio sin problema.",
    "Atención rápida y resultado sólido, quedó conforme toda la familia.",
    "Mostró experiencia y dio alternativas útiles para evitar futuros problemas.",
    "Servicio correcto, transparente con el precio y puntual con la visita.",
]


def random_decimal(min_value: int, max_value: int) -> Decimal:
    return Decimal(str(random.randint(min_value, max_value)))


def ensure_role(db, name: str, description: str | None = None) -> Role:
    role = db.scalar(select(Role).where(Role.name == name))
    if role:
        return role
    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def ensure_user(
    db,
    *,
    ci: str,
    firstname: str,
    lastname: str,
    motherlastname: str | None,
    birthdate: date,
    email: str,
    phone: str,
    city: str | None,
    zone: str | None,
    latitude: float | None = None,
    longitude: float | None = None,
    isverified: bool = True,
) -> User:
    user = db.scalar(select(User).where(User.ci == ci))
    if user:
        changed = False
        for field, value in {
            "firstname": firstname,
            "lastname": lastname,
            "motherlastname": motherlastname,
            "birthdate": birthdate,
            "email": email,
            "phone": phone,
            "city": city,
            "zone": zone,
            "latitude": latitude,
            "longitude": longitude,
            "isverified": isverified,
            "isactive": True,
        }.items():
            if getattr(user, field) != value:
                setattr(user, field, value)
                changed = True
        if changed:
            db.commit()
            db.refresh(user)
        return user

    user = User(
        ci=ci,
        firstname=firstname,
        lastname=lastname,
        motherlastname=motherlastname,
        birthdate=birthdate,
        email=email,
        phone=phone,
        passwordhash=hashpassword(DEFAULT_PASSWORD),
        city=city,
        zone=zone,
        latitude=latitude,
        longitude=longitude,
        isactive=True,
        isverified=isverified,
        failedloginattempts=0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def ensure_user_role(db, userci: str, rolename: str) -> UserRole:
    role = db.scalar(select(Role).where(Role.name == rolename))
    existing = db.scalar(
        select(UserRole).where(
            UserRole.userci == userci,
            UserRole.roleid == role.id,
        )
    )
    if existing:
        return existing
    user_role = UserRole(userci=userci, roleid=role.id)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


def ensure_specialty(db, name: str, description: str) -> Specialty:
    specialty = db.scalar(select(Specialty).where(Specialty.name == name))
    if specialty:
        changed = False
        if specialty.description != description:
            specialty.description = description
            changed = True
        if specialty.isactive is not True:
            specialty.isactive = True
            changed = True
        if changed:
            db.commit()
            db.refresh(specialty)
        return specialty

    specialty = Specialty(
        name=name,
        description=description,
        isactive=True,
    )
    db.add(specialty)
    db.commit()
    db.refresh(specialty)
    return specialty


def ensure_professional_profile(
    db,
    *,
    userci: str,
    bio: str,
    experience_years: int,
    is_available: bool,
    verification_status: VerificationStatusEnum = VerificationStatusEnum.APPROVED,
) -> ProfessionalProfile:
    profile = db.scalar(select(ProfessionalProfile).where(ProfessionalProfile.userci == userci))
    if profile:
        profile.bio = bio
        profile.experienceyears = experience_years
        profile.isavailable = is_available
        profile.verificationstatus = verification_status
        db.commit()
        db.refresh(profile)
        return profile

    profile = ProfessionalProfile(
        userci=userci,
        bio=bio,
        experienceyears=experience_years,
        verificationstatus=verification_status,
        ratingaverage=0.0,
        ratingcount=0,
        isavailable=is_available,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def ensure_professional_specialty(db, professionalprofileid, specialtyid) -> ProfessionalSpecialty:
    link = db.scalar(
        select(ProfessionalSpecialty).where(
            ProfessionalSpecialty.professionalprofileid == professionalprofileid,
            ProfessionalSpecialty.specialtyid == specialtyid,
        )
    )
    if link:
        return link

    link = ProfessionalSpecialty(
        professionalprofileid=professionalprofileid,
        specialtyid=specialtyid,
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def ensure_availability(
    db,
    professionalprofileid,
    day_of_week: int,
    start_at: time,
    end_at: time,
    is_active: bool = True,
) -> ProfessionalAvailability:
    availability = db.scalar(
        select(ProfessionalAvailability).where(
            ProfessionalAvailability.professionalprofileid == professionalprofileid,
            ProfessionalAvailability.dayofweek == day_of_week,
        )
    )
    if availability:
        availability.starttime = start_at
        availability.endtime = end_at
        availability.isactive = is_active
        db.commit()
        db.refresh(availability)
        return availability

    availability = ProfessionalAvailability(
        professionalprofileid=professionalprofileid,
        dayofweek=day_of_week,
        starttime=start_at,
        endtime=end_at,
        isactive=is_active,
    )
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


def ensure_request(
    db,
    *,
    clientci: str,
    specialtyid,
    title: str,
    description: str,
    city: str,
    zone: str | None,
    latitude: float | None,
    longitude: float | None,
    budget: Decimal | None,
    urgency: UrgencyLevelEnum,
    scheduled_date: datetime | None,
) -> Request:
    request = db.scalar(
        select(Request).where(
            Request.clientci == clientci,
            Request.title == title,
        )
    )
    if request:
        return request

    request = Request(
        clientci=clientci,
        specialtyid=specialtyid,
        title=title,
        description=description,
        budget=budget,
        proposedfinalprice=None,
        scheduleddate=scheduled_date,
        city=city,
        zone=zone,
        latitude=latitude,
        longitude=longitude,
        urgency=urgency,
        status=RequestStatusEnum.PENDING,
        isreviewenabled=False,
        cancellationreason=None,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def ensure_application(
    db,
    *,
    requestid,
    professionalprofileid,
    proposal_message: str,
    proposed_price: Decimal | None,
    estimated_hours: int | None,
) -> Application:
    application = db.scalar(
        select(Application).where(
            Application.requestid == requestid,
            Application.professionalprofileid == professionalprofileid,
        )
    )
    if application:
        return application

    application = Application(
        requestid=requestid,
        professionalprofileid=professionalprofileid,
        proposalmessage=proposal_message,
        proposedprice=proposed_price,
        estimatedtimehours=estimated_hours,
        status=ApplicationStatusEnum.PENDING,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def ensure_review(
    db,
    *,
    applicationid,
    reviewerci: str,
    revieweduserci: str,
    rating: int,
    comment: str,
) -> Review:
    review = db.scalar(
        select(Review).where(
            Review.applicationid == applicationid,
            Review.reviewerci == reviewerci,
        )
    )
    if review:
        return review

    review = Review(
        applicationid=applicationid,
        reviewerci=reviewerci,
        revieweduserci=revieweduserci,
        rating=rating,
        comment=comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def recalculate_professional_ratings(db) -> None:
    profiles = db.scalars(select(ProfessionalProfile)).all()
    for profile in profiles:
        avg_rating, rating_count = db.execute(
            select(
                func.avg(Review.rating),
                func.count(Review.id),
            )
            .join(Application, Application.id == Review.applicationid)
            .where(Application.professionalprofileid == profile.id)
        ).one()
        profile.ratingaverage = float(avg_rating or 0.0)
        profile.ratingcount = int(rating_count or 0)
    db.commit()


def seed_roles(db) -> None:
    ensure_role(db, RoleEnum.CLIENT.value, "Cliente del marketplace")
    ensure_role(db, RoleEnum.PROFESSIONAL.value, "Profesional del marketplace")
    ensure_role(db, RoleEnum.ADMIN.value, "Administrador")
    ensure_role(db, RoleEnum.SUPPORT.value, "Soporte")
    ensure_role(db, RoleEnum.SUPERADMIN.value, "Super administrador")


def seed_specialties(db) -> dict[str, Specialty]:
    result: dict[str, Specialty] = {}
    for name, description in SPECIALTIES:
        result[name] = ensure_specialty(db, name, description)
    return result


def seed_clients(db) -> list[User]:
    users: list[User] = []
    for item in CLIENTS:
        user = ensure_user(
            db,
            ci=item["ci"],
            firstname=item["firstname"],
            lastname=item["lastname"],
            motherlastname=item["motherlastname"],
            birthdate=item["birthdate"],
            email=item["email"],
            phone=item["phone"],
            city=item["city"],
            zone=item["zone"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            isverified=True,
        )
        ensure_user_role(db, user.ci, RoleEnum.CLIENT.value)
        users.append(user)
    return users


def seed_professionals(db, specialties_by_name: dict[str, Specialty]) -> list[ProfessionalProfile]:
    profiles: list[ProfessionalProfile] = []

    for item in PROFESSIONALS:
        user = ensure_user(
            db,
            ci=item["ci"],
            firstname=item["firstname"],
            lastname=item["lastname"],
            motherlastname=item["motherlastname"],
            birthdate=item["birthdate"],
            email=item["email"],
            phone=item["phone"],
            city=item["city"],
            zone=item["zone"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            isverified=True,
        )
        ensure_user_role(db, user.ci, RoleEnum.PROFESSIONAL.value)

        profile = ensure_professional_profile(
            db,
            userci=user.ci,
            bio=item["bio"],
            experience_years=item["experience_years"],
            is_available=item["is_available"],
            verification_status=VerificationStatusEnum.APPROVED,
        )

        for specialty_name in item["specialties"]:
            ensure_professional_specialty(db, profile.id, specialties_by_name[specialty_name].id)

        ensure_availability(db, profile.id, 1, time(8, 0), time(12, 0))
        ensure_availability(db, profile.id, 3, time(14, 0), time(18, 0))
        ensure_availability(db, profile.id, 5, time(9, 0), time(13, 0))

        profiles.append(profile)

    return profiles


def seed_requests(
    db,
    clients: list[User],
    profiles: list[ProfessionalProfile],
    specialties_by_name: dict[str, Specialty],
) -> list[Request]:
    requests: list[Request] = []

    profile_by_specialty: dict[str, list[ProfessionalProfile]] = {}
    for profile in profiles:
        prof = db.scalar(
            select(ProfessionalProfile).where(ProfessionalProfile.id == profile.id)
        )
        for ps in prof.specialties:
            specialty_name = ps.specialty.name
            profile_by_specialty.setdefault(specialty_name, []).append(prof)

    now = datetime.now(UTC)

    request_plan = [
        ("Electricista", 0, RequestStatusEnum.PENDING),
        ("Plomería", 1, RequestStatusEnum.PENDING),
        ("Pintura", 2, RequestStatusEnum.PENDING),
        ("Carpintería", 3, RequestStatusEnum.PENDING),
        ("Cerrajería", 4, RequestStatusEnum.PENDING),
        ("Jardinería", 5, RequestStatusEnum.PENDING),
        ("Albañilería", 6, RequestStatusEnum.ASSIGNED),
        ("Limpieza", 7, RequestStatusEnum.ASSIGNED),
        ("Gasfitería", 8, RequestStatusEnum.ASSIGNED),
        ("Técnico de electrodomésticos", 9, RequestStatusEnum.INPROGRESS),
        ("Soldadura", 0, RequestStatusEnum.INPROGRESS),
        ("Yesero", 1, RequestStatusEnum.INPROGRESS),
        ("Electricista", 2, RequestStatusEnum.COMPLETED),
        ("Plomería", 3, RequestStatusEnum.COMPLETED),
        ("Carpintería", 4, RequestStatusEnum.COMPLETED),
    ]

    for idx, (specialty_name, client_idx, target_status) in enumerate(request_plan):
        title, description = REQUEST_TEMPLATES[idx]
        client = clients[client_idx]
        specialty = specialties_by_name[specialty_name]

        request = ensure_request(
            db,
            clientci=client.ci,
            specialtyid=specialty.id,
            title=title,
            description=description,
            city=client.city,
            zone=client.zone,
            latitude=client.latitude,
            longitude=client.longitude,
            budget=random_decimal(120, 1500),
            urgency=random.choice(
                [UrgencyLevelEnum.LOW, UrgencyLevelEnum.MEDIUM, UrgencyLevelEnum.HIGH]
            ),
            scheduled_date=now + timedelta(days=idx + 1),
        )

        request.status = target_status if target_status == RequestStatusEnum.PENDING else RequestStatusEnum.PENDING
        request.assignedprofessionalprofileid = None
        request.proposedfinalprice = None
        request.isreviewenabled = False
        request.cancellationreason = None
        db.commit()
        db.refresh(request)
        requests.append(request)

    return requests


def seed_applications_and_state_flow(
    db,
    requests: list[Request],
    profiles: list[ProfessionalProfile],
) -> tuple[list[Application], list[Request]]:
    applications: list[Application] = []
    now_profiles = {
        profile.id: db.scalar(select(ProfessionalProfile).where(ProfessionalProfile.id == profile.id))
        for profile in profiles
    }

    for idx, request in enumerate(requests):
        fresh_request = db.scalar(select(Request).where(Request.id == request.id))
        matching_profiles = db.scalars(
            select(ProfessionalProfile)
            .join(ProfessionalSpecialty, ProfessionalSpecialty.professionalprofileid == ProfessionalProfile.id)
            .where(ProfessionalSpecialty.specialtyid == fresh_request.specialtyid)
        ).all()

        if not matching_profiles:
            matching_profiles = list(now_profiles.values())

        random.shuffle(matching_profiles)
        candidates = matching_profiles[: min(3, len(matching_profiles))]

        for j, profile in enumerate(candidates):
            if profile.userci == fresh_request.clientci:
                continue

            app = ensure_application(
                db,
                requestid=fresh_request.id,
                professionalprofileid=profile.id,
                proposal_message=(
                    f"Puedo ayudarte con '{fresh_request.title.lower()}'. "
                    f"Tengo experiencia en trabajos similares y disponibilidad esta semana."
                ),
                proposed_price=random_decimal(100, 1600),
                estimated_hours=random.randint(2, 12),
            )
            applications.append(app)

        db.refresh(fresh_request)

        if fresh_request.status == RequestStatusEnum.PENDING and idx >= 6:
            request_apps = db.scalars(
                select(Application).where(Application.requestid == fresh_request.id)
            ).all()

            if request_apps:
                accepted = request_apps[0]
                for item in request_apps:
                    item.status = (
                        ApplicationStatusEnum.ACCEPTED
                        if item.id == accepted.id
                        else ApplicationStatusEnum.REJECTED
                    )

                fresh_request.assignedprofessionalprofileid = accepted.professionalprofileid
                fresh_request.proposedfinalprice = accepted.proposedprice

                if idx in [6, 7, 8]:
                    fresh_request.status = RequestStatusEnum.ASSIGNED
                    fresh_request.isreviewenabled = False
                elif idx in [9, 10, 11]:
                    fresh_request.status = RequestStatusEnum.INPROGRESS
                    fresh_request.isreviewenabled = False
                elif idx in [12, 13, 14]:
                    fresh_request.status = RequestStatusEnum.COMPLETED
                    fresh_request.isreviewenabled = True
                    accepted.status = ApplicationStatusEnum.COMPLETED

                db.commit()
                db.refresh(fresh_request)

    return applications, requests


def seed_reviews(db, requests: list[Request]) -> list[Review]:
    reviews: list[Review] = []
    comment_idx = 0

    completed_requests = db.scalars(
        select(Request).where(Request.status == RequestStatusEnum.COMPLETED)
    ).all()

    for request in completed_requests:
        accepted_application = db.scalar(
            select(Application).where(
                Application.requestid == request.id,
                Application.status == ApplicationStatusEnum.COMPLETED,
            )
        )
        if not accepted_application:
            continue

        assigned_profile = db.scalar(
            select(ProfessionalProfile).where(
                ProfessionalProfile.id == accepted_application.professionalprofileid
            )
        )
        if not assigned_profile:
            continue

        rating = random.randint(4, 5)
        comment = REVIEW_COMMENTS[comment_idx % len(REVIEW_COMMENTS)]
        comment_idx += 1

        review = ensure_review(
            db,
            applicationid=accepted_application.id,
            reviewerci=request.clientci,
            revieweduserci=assigned_profile.userci,
            rating=rating,
            comment=comment,
        )
        reviews.append(review)

    recalculate_professional_ratings(db)
    return reviews


def print_summary(db) -> None:
    counts = {
        "roles": db.scalar(select(func.count(Role.id))),
        "users": db.scalar(select(func.count(User.ci))),
        "specialties": db.scalar(select(func.count(Specialty.id))),
        "professional_profiles": db.scalar(select(func.count(ProfessionalProfile.id))),
        "professional_specialties": db.scalar(select(func.count(ProfessionalSpecialty.id))),
        "availabilities": db.scalar(select(func.count(ProfessionalAvailability.id))),
        "requests": db.scalar(select(func.count(Request.id))),
        "applications": db.scalar(select(func.count(Application.id))),
        "reviews": db.scalar(select(func.count(Review.id))),
    }

    print("\nSeed demo completado:")
    for key, value in counts.items():
        print(f"- {key}: {value}")


def run_seed_demo() -> None:
    random.seed(RANDOM_SEED)
    db = SessionLocal()

    try:
        print("Iniciando seed demo...")
        seed_roles(db)
        specialties_by_name = seed_specialties(db)
        clients = seed_clients(db)
        profiles = seed_professionals(db, specialties_by_name)
        requests = seed_requests(db, clients, profiles, specialties_by_name)
        seed_applications_and_state_flow(db, requests, profiles)
        seed_reviews(db, requests)
        print_summary(db)
        print(f"\nContraseña por defecto para usuarios demo: {DEFAULT_PASSWORD}")
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()


if __name__ == "__main__":
    run_seed_demo()
```

## `scripts/seed.py`

```python
from datetime import date

from sqlalchemy import select

from app.db.session import SessionLocal

from app.core.security import hash_password

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


db = SessionLocal()


def seed_roles():

    roles = [
        "CLIENT",
        "PROFESSIONAL",
        "ADMIN",
        "SUPPORT",
        "SUPERADMIN",
    ]

    for role_name in roles:

        existing = db.scalar(
            select(Role).where(
                Role.name == role_name
            )
        )

        if not existing:

            role = Role(
                name=role_name,
            )

            db.add(role)

    db.commit()

    print("Roles seeded")


def seed_superadmin():

    existing = db.scalar(
        select(User).where(
            User.ci == "SUPERADMIN"
        )
    )

    if existing:
        print("Superadmin already exists")
        return

    user = User(
        ci="SUPERADMIN",
        first_name="Super",
        last_name="Admin",
        mother_last_name="System",
        birth_date=date(1990, 1, 1),
        email="superadmin@siswork.com",
        phone="70000000",
        password_hash=hash_password(
            "demons312es"
        ),
        city="La Paz",
        zone="Central",
        is_verified=True,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    role = db.scalar(
        select(Role).where(
            Role.name == "SUPERADMIN"
        )
    )

    user_role = UserRole(
        user_ci=user.ci,
        role_id=role.id,
    )

    db.add(user_role)

    db.commit()

    print("Superadmin seeded")


def seed_client():

    existing = db.scalar(
        select(User).where(
            User.ci == "CLIENT001"
        )
    )

    if existing:
        print("Client already exists")
        return

    user = User(
        ci="CLIENT001",
        first_name="Test",
        last_name="Client",
        mother_last_name="User",
        birth_date=date(1998, 5, 10),
        email="client@siswork.com",
        phone="71111111",
        password_hash=hash_password(
            "demons312es"
        ),
        city="La Paz",
        zone="Sopocachi",
        is_verified=False,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    role = db.scalar(
        select(Role).where(
            Role.name == "CLIENT"
        )
    )

    user_role = UserRole(
        user_ci=user.ci,
        role_id=role.id,
    )

    db.add(user_role)

    db.commit()

    print("Client seeded")


def run_seed():

    print("Starting seed...")

    seed_roles()

    seed_superadmin()

    seed_client()

    print("Seed completed")


if __name__ == "__main__":
    run_seed()
```

