from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric, Text, TIMESTAMP, UniqueConstraint, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import EstadoPostulacionEnum


class Application(Base):
    __tablename__ = "postulaciones_solicitud"

    id_postulacion: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_solicitud: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("solicitudes_servicio.id_solicitud", ondelete="CASCADE"),
        nullable=False,
    )
    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="CASCADE"),
        nullable=False,
    )
    mensaje_propuesta: Mapped[str | None] = mapped_column(Text)
    precio_estimado: Mapped[float | None] = mapped_column(Numeric(10, 2))
    estado: Mapped[EstadoPostulacionEnum] = mapped_column(
        Enum(EstadoPostulacionEnum, name="estado_postulacion_enum"),
        nullable=False,
        server_default=text("'pendiente'"),
    )
    postulado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    respondido_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    cancelado_en: Mapped[str | None] = mapped_column(TIMESTAMP)

    solicitud = relationship("ServiceRequest", back_populates="postulaciones")
    perfil_profesional = relationship("ProfessionalProfile", back_populates="postulaciones")

    __table_args__ = (
        UniqueConstraint("id_solicitud", "id_perfil_profesional", name="uq_postulacion_solicitud_profesional"),
        CheckConstraint(
            "precio_estimado IS NULL OR precio_estimado >= 0",
            name="chk_precio_estimado",
        ),
        Index("idx_postulaciones_solicitud", "id_solicitud"),
        Index("idx_postulaciones_profesional", "id_perfil_profesional"),
        Index("idx_postulaciones_estado", "estado"),
    )