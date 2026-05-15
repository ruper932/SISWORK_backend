from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ContactChannel


class ServiceContact(Base):
    __tablename__ = "servicecontacts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_request_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("servicerequests.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    client_user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    professional_profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("professionalprofiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    channel: Mapped[ContactChannel] = mapped_column(
        Enum(ContactChannel, name="contact_channel_enum"),
        nullable=False,
        default=ContactChannel.WHATSAPP,
    )
    contacted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    service_request = relationship("ServiceRequest")
    client_user = relationship("User", foreign_keys=[client_user_id])
    professional_profile = relationship("ProfessionalProfile")