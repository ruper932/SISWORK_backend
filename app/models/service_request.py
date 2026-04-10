from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Numeric, String, Text, TIMESTAMP, Date, Time, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import CanalContactoEnum, EstadoSolicitudEnum


class ServiceRequest(Base):
    __tablename__ = "solicitudes_servicio"

    id_solicitud: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_cliente: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"),
        nullable=False,
    )
    id_especialidad: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("especialidades.id_especialidad", ondelete="RESTRICT"),
        nullable=False,
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    departamento: Mapped[str] = mapped_column(String(100), nullable=False, server_default=text("'La Paz'"))
    ciudad: Mapped[str] = mapped_column(String(100), nullable=False, server_default=text("'La Paz'"))
    zona: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str | None] = mapped_column(String(255))
    referencia: Mapped[str | None] = mapped_column(Text)
    fecha_preferida: Mapped[str | None] = mapped_column(Date)
    hora_preferida_inicio: Mapped[str | None] = mapped_column(Time)
    hora_preferida_fin: Mapped[str | None] = mapped_column(Time)
    presupuesto_minimo: Mapped[float | None] = mapped_column(Numeric(10, 2))
    presupuesto_maximo: Mapped[float | None] = mapped_column(Numeric(10, 2))
    estado: Mapped[EstadoSolicitudEnum] = mapped_column(
        Enum(EstadoSolicitudEnum, name="estado_solicitud_enum"),
        nullable=False,
        server_default=text("'abierta'"),
    )
    id_profesional_asignado: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="SET NULL"),
    )
    canal_contacto: Mapped[CanalContactoEnum] = mapped_column(
        Enum(CanalContactoEnum, name="canal_contacto_enum"),
        nullable=False,
        server_default=text("'whatsapp'"),
    )
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("TRUE"))
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    cerrado_en: Mapped[str | None] = mapped_column(TIMESTAMP)

    cliente = relationship("User", back_populates="solicitudes", foreign_keys=[id_cliente])
    especialidad = relationship("Specialty", back_populates="solicitudes")
    profesional_asignado = relationship("ProfessionalProfile", back_populates="solicitudes_asignadas", foreign_keys=[id_profesional_asignado])
    postulaciones = relationship("Application", back_populates="solicitud", cascade="all, delete-orphan")
    calificacion = relationship("Rating", back_populates="solicitud", uselist=False)

    __table_args__ = (
        CheckConstraint(
            """
            (
                presupuesto_minimo IS NULL AND presupuesto_maximo IS NULL
            ) OR (
                presupuesto_minimo IS NOT NULL AND presupuesto_maximo IS NOT NULL
                AND presupuesto_minimo >= 0
                AND presupuesto_maximo >= presupuesto_minimo
            )
            """,
            name="chk_presupuesto_solicitud",
        ),
        CheckConstraint(
            """
            (
                hora_preferida_inicio IS NULL AND hora_preferida_fin IS NULL
            ) OR (
                hora_preferida_inicio IS NOT NULL AND hora_preferida_fin IS NOT NULL
                AND hora_preferida_inicio < hora_preferida_fin
            )
            """,
            name="chk_horario_preferido",
        ),
        Index("idx_solicitudes_cliente", "id_cliente"),
        Index("idx_solicitudes_especialidad", "id_especialidad"),
        Index("idx_solicitudes_estado", "estado"),
        Index("idx_solicitudes_zona", "zona"),
        Index("idx_solicitudes_creado_en", "creado_en"),
        Index("idx_solicitudes_profesional_asignado", "id_profesional_asignado"),
    )