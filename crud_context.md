# CRUD context

## `app/api/v1/users.py`

```python
from fastapi import (
    APIRouter,
    Depends,
)

from app.api.deps.auth import get_current_user

from app.models.user import User

from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):

    roles = [
        user_role.role.name
        for user_role in current_user.user_roles
    ]

    return {
        "ci": current_user.ci,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "mother_last_name": current_user.mother_last_name,
        "birth_date": current_user.birth_date,
        "email": current_user.email,
        "phone": current_user.phone,
        "city": current_user.city,
        "zone": current_user.zone,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "roles": roles,
    }
```

## `app/api/v1/professionals.py`

```python
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
        return ProfessionalService.search_public_professionals(
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
```

## `app/api/v1/admin.py`

```python
from fastapi import (
    APIRouter,
    Depends,
)

from app.api.deps.auth import require_roles

from app.models.user import User


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_roles(
            ["ADMIN", "SUPERADMIN"],
        )
    ),
):

    return {
        "message": "Welcome admin",
        "user": current_user.ci,
    }
```

## `app/schemas/user.py`

```python
from datetime import date
from datetime import UTC
from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)


class UserCreate(BaseModel):

    ci: str

    first_name: str
    last_name: str
    mother_last_name: str | None = None

    birth_date: date

    email: EmailStr

    phone: str

    password: str

    city: str | None = None
    zone: str | None = None

    @field_validator("birth_date")
    @classmethod
    def validate_age(
        cls,
        value: date,
    ):

        today = datetime.now(UTC).date()

        age = (
            today.year
            - value.year
            - (
                (today.month, today.day)
                < (value.month, value.day)
            )
        )

        if age < 18:
            raise ValueError(
                "User must be at least 18 years old"
            )

        return value


class UserLogin(BaseModel):

    ci: str
    password: str


class UserResponse(BaseModel):

    ci: str

    first_name: str
    last_name: str
    mother_last_name: str | None = None

    birth_date: date

    email: str

    phone: str

    city: str | None = None
    zone: str | None = None

    is_active: bool
    is_verified: bool

    roles: list[str] = []

    class Config:
        from_attributes = True

    ci: str

    first_name: str
    last_name: str
    mother_last_name: str | None = None

    birth_date: date

    email: str

    phone: str

    city: str | None = None
    zone: str | None = None

    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True
```

## `app/schemas/professional.py`

```python
from __future__ import annotations

import uuid
from datetime import time
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.db.enums import VerificationStatusEnum


class VerificationRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: VerificationStatusEnum
    rejection_reason: Optional[str] = None


class ProfessionalAvailabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool


class SpecialtySimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: Optional[str] = None


class ProfessionalPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_ci: str
    full_name: str
    bio: Optional[str] = None
    experience_years: int
    verification_status: VerificationStatusEnum
    rating_average: float
    rating_count: int
    is_available: bool
    city: Optional[str] = None
    zone: Optional[str] = None
    specialties: List[SpecialtySimpleResponse]
    availabilities: List[ProfessionalAvailabilityResponse]
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

## `app/repositories/professional_repository.py`

```python
from __future__ import annotations

import uuid
from typing import Optional, List

from sqlalchemy import select, or_
from sqlalchemy.orm import Session, selectinload, joinedload

from app.db.enums import VerificationStatusEnum
from app.models.professional_profile import ProfessionalProfile
from app.models.professional_specialty import ProfessionalSpecialty
from app.models.specialty import Specialty
from app.models.user import User


class ProfessionalRepository:
    @staticmethod
    def get_by_user_ci(db: Session, user_ci: str) -> Optional[ProfessionalProfile]:
        stmt = (
            select(ProfessionalProfile)
            .options(
                joinedload(ProfessionalProfile.user),
                selectinload(ProfessionalProfile.specialties).joinedload(ProfessionalSpecialty.specialty),
                selectinload(ProfessionalProfile.availabilities),
            )
            .where(ProfessionalProfile.user_ci == user_ci)
        )
        return db.scalar(stmt)

    @staticmethod
    def search_public_professionals(
        db: Session,
        q: Optional[str] = None,
        specialty_id: Optional[uuid.UUID] = None,
        city: Optional[str] = None,
        zone: Optional[str] = None,
        min_rating: Optional[float] = None,
        is_available: Optional[bool] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ProfessionalProfile]:
        stmt = (
            select(ProfessionalProfile)
            .options(
                joinedload(ProfessionalProfile.user),
                selectinload(ProfessionalProfile.specialties).joinedload(ProfessionalSpecialty.specialty),
                selectinload(ProfessionalProfile.availabilities),
            )
            .where(ProfessionalProfile.verification_status == VerificationStatusEnum.APPROVED)
        )

        if q:
            like_value = f"%{q.strip()}%"
            stmt = stmt.join(ProfessionalProfile.user).where(
                or_(
                    User.firstname.ilike(like_value),
                    User.lastname.ilike(like_value),
                    User.mother_lastname.ilike(like_value),
                    ProfessionalProfile.bio.ilike(like_value),
                )
            )

        if specialty_id:
            stmt = stmt.join(ProfessionalProfile.specialties).where(
                ProfessionalSpecialty.specialty_id == specialty_id
            )

        if city:
            stmt = stmt.join(ProfessionalProfile.user).where(User.city.ilike(f"%{city.strip()}%"))

        if zone:
            stmt = stmt.join(ProfessionalProfile.user).where(User.zone.ilike(f"%{zone.strip()}%"))

        if min_rating is not None:
            stmt = stmt.where(ProfessionalProfile.rating_average >= min_rating)

        if is_available is not None:
            stmt = stmt.where(ProfessionalProfile.is_available == is_available)

        stmt = stmt.order_by(
            ProfessionalProfile.rating_average.desc(),
            ProfessionalProfile.rating_count.desc(),
            ProfessionalProfile.created_at.desc(),
        ).offset(skip).limit(limit)

        return list(db.scalars(stmt).unique().all())
```

## `app/repositories/user_repository.py`

```python

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User

from sqlalchemy.orm import joinedload

from app.models.user_role import UserRole
from app.models.role import Role
from sqlalchemy import or_

class UserRepository:

    @staticmethod
    def get_by_ci(
        db: Session,
        ci: str,
    ):
        stmt = (
            select(User)
            .options(
                joinedload(User.user_roles)
                .joinedload(UserRole.role)
            )
            .where(
                User.ci == ci,
                User.deleted_at.is_(None),
            )
        )

        return db.scalar(stmt)

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ):
        stmt = select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )

        return db.scalar(stmt)

    @staticmethod
    def create(
        db: Session,
        user: User,
    ):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    @staticmethod
    def get_by_ci_or_email(
        db: Session,
        identifier: str,
    ):

        stmt = (
            select(User)
            .where(
                or_(
                    User.ci == identifier,
                    User.email == identifier,
                ),
                User.deleted_at.is_(None),
            )
        )

        return db.scalar(stmt)
```

## `app/repositories/role_repository.py`

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_role import UserRole
from app.models.role import Role


class RoleRepository:

    @staticmethod
    def get_user_roles(
        db: Session,
        user_ci: str,
    ):

        stmt = (
            select(Role.name)
            .join(
                UserRole,
                UserRole.role_id == Role.id,
            )
            .where(
                UserRole.user_ci == user_ci,
            )
        )

        result = db.execute(stmt)

        return result.scalars().all()
    
    @staticmethod
    def get_by_name(
        db: Session,
        role_name: str,
    ):

        stmt = select(Role).where(
            Role.name == role_name,
        )

        return db.scalar(stmt)
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

