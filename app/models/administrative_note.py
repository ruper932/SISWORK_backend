from sqlalchemy import Boolean, ForeignKey, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AdministrativeNote(Base):
    __tablename__ = "notas_administrativas"

    id_nota: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_autor: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )
    entidad_relacionada: Mapped[str] = mapped_column(String(100), nullable=False)
    id_entidad_relacionada: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False)
    nota: Mapped[str] = mapped_column(Text, nullable=False)
    privada: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("TRUE"))
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    autor = relationship("User", foreign_keys=[id_autor])