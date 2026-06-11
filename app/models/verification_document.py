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