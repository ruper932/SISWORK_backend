from sqlalchemy import CheckConstraint, Enum, ForeignKey, Index, Integer, Text, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import EstadoVerificacionEnum


class ValidationQueue(Base):
    __tablename__ = "cola_validacion_profesionales"

    id_validacion: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    solicitado_por: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"),
        nullable=False,
    )
    asignado_a_soporte: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),
    )
    estado: Mapped[EstadoVerificacionEnum] = mapped_column(
        Enum(EstadoVerificacionEnum, name="estado_verificacion_enum"),
        nullable=False,
        server_default=text("'pendiente'"),
    )
    enviado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    revision_iniciada_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    resuelto_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    motivo_rechazo: Mapped[str | None] = mapped_column(Text)
    tiempo_espera_minutos: Mapped[int | None] = mapped_column(Integer)
    tiempo_revision_minutos: Mapped[int | None] = mapped_column(Integer)
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    perfil_profesional = relationship("ProfessionalProfile")
    solicitante = relationship("User", foreign_keys=[solicitado_por])
    soporte = relationship("User", foreign_keys=[asignado_a_soporte])

    __table_args__ = (
        CheckConstraint(
            "tiempo_espera_minutos IS NULL OR tiempo_espera_minutos >= 0",
            name="chk_tiempo_espera",
        ),
        CheckConstraint(
            "tiempo_revision_minutos IS NULL OR tiempo_revision_minutos >= 0",
            name="chk_tiempo_revision",
        ),
        Index("idx_cola_validacion_estado", "estado"),
        Index("idx_cola_validacion_asignado_a_soporte", "asignado_a_soporte"),
        Index("idx_cola_validacion_enviado_en", "enviado_en"),
    )