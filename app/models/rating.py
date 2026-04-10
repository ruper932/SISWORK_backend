from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Text, TIMESTAMP, UniqueConstraint, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Rating(Base):
    __tablename__ = "calificaciones_servicio"

    id_calificacion: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_solicitud: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("solicitudes_servicio.id_solicitud", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    id_cliente: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"),
        nullable=False,
    )
    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="RESTRICT"),
        nullable=False,
    )
    puntuacion: Mapped[int] = mapped_column(Integer, nullable=False)
    comentario: Mapped[str | None] = mapped_column(Text)
    verificada: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("TRUE"))
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    solicitud = relationship("ServiceRequest", back_populates="calificacion")
    cliente = relationship("User", back_populates="calificaciones", foreign_keys=[id_cliente])
    perfil_profesional = relationship("ProfessionalProfile", back_populates="calificaciones", foreign_keys=[id_perfil_profesional])

    __table_args__ = (
        CheckConstraint("puntuacion BETWEEN 1 AND 5", name="chk_puntuacion"),
        Index("idx_calificaciones_profesional", "id_perfil_profesional"),
        Index("idx_calificaciones_cliente", "id_cliente"),
        Index("idx_calificaciones_puntuacion", "puntuacion"),
    )