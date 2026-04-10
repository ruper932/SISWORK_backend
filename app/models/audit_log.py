from sqlalchemy import Enum, ForeignKey, Index, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import AccionAuditoriaEnum


class AuditLog(Base):
    __tablename__ = "registros_auditoria"

    id_registro: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_usuario_actor: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),
    )
    accion: Mapped[AccionAuditoriaEnum] = mapped_column(
        Enum(AccionAuditoriaEnum, name="accion_auditoria_enum"),
        nullable=False,
    )
    entidad: Mapped[str] = mapped_column(String(100), nullable=False)
    id_entidad: Mapped[str | None] = mapped_column(UUID(as_uuid=True))
    valores_anteriores: Mapped[dict | None] = mapped_column(JSONB)
    valores_nuevos: Mapped[dict | None] = mapped_column(JSONB)
    direccion_ip: Mapped[str | None] = mapped_column(INET)
    agente_usuario: Mapped[str | None] = mapped_column(Text)
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    usuario_actor = relationship("User", foreign_keys=[id_usuario_actor])

    __table_args__ = (
        Index("idx_registros_auditoria_usuario_actor", "id_usuario_actor"),
        Index("idx_registros_auditoria_accion", "accion"),
        Index("idx_registros_auditoria_entidad", "entidad", "id_entidad"),
        Index("idx_registros_auditoria_creado_en", "creado_en"),
    )