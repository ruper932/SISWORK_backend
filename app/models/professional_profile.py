from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Integer, Numeric, String, Text, TIMESTAMP, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import EstadoVerificacionEnum


class ProfessionalProfile(Base):
    __tablename__ = "perfiles_profesionales"

    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_usuario: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    biografia: Mapped[str | None] = mapped_column(Text)
    anos_experiencia: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    zona_principal: Mapped[str] = mapped_column(String(100), nullable=False)
    radio_servicio_km: Mapped[float | None] = mapped_column(Numeric(5, 2), server_default=text("5.00"))
    referencia_trabajo: Mapped[str | None] = mapped_column(Text)
    documento_identidad_url: Mapped[str | None] = mapped_column(Text)
    estado_verificacion: Mapped[EstadoVerificacionEnum] = mapped_column(
        Enum(EstadoVerificacionEnum, name="estado_verificacion_enum"),
        nullable=False,
        server_default=text("'pendiente'"),
    )
    verificacion_solicitada_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    verificacion_resuelta_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    verificado_por: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),
    )
    calificacion_promedio: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False, server_default=text("0.00"))
    cantidad_calificaciones: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    cantidad_servicios_completados: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    disponible_ahora: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("FALSE"))
    contacto_publico_habilitado: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("TRUE"))
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    usuario = relationship("User", back_populates="perfil_profesional", foreign_keys=[id_usuario])
    usuario_verificador = relationship("User", foreign_keys=[verificado_por])
    especialidades = relationship("ProfessionalSpecialty", back_populates="perfil_profesional", cascade="all, delete-orphan")
    certificaciones = relationship("Certification", cascade="all, delete-orphan")
    disponibilidades = relationship("Availability", cascade="all, delete-orphan")
    zonas = relationship("ProfessionalZone", cascade="all, delete-orphan")
    solicitudes_asignadas = relationship("ServiceRequest", back_populates="profesional_asignado", foreign_keys="ServiceRequest.id_profesional_asignado")
    postulaciones = relationship("Application", back_populates="perfil_profesional", cascade="all, delete-orphan")
    calificaciones = relationship("Rating", back_populates="perfil_profesional", foreign_keys="Rating.id_perfil_profesional")
    cola_validacion = relationship("ValidationQueue", uselist=False)

    __table_args__ = (
        CheckConstraint("anos_experiencia >= 0", name="chk_anos_experiencia"),
        CheckConstraint("calificacion_promedio >= 0 AND calificacion_promedio <= 5", name="chk_calificacion_promedio"),
        Index("idx_perfiles_profesionales_id_usuario", "id_usuario"),
        Index("idx_perfiles_profesionales_estado_verificacion", "estado_verificacion"),
        Index("idx_perfiles_profesionales_zona_principal", "zona_principal"),
        Index("idx_perfiles_profesionales_disponible_ahora", "disponible_ahora"),
        Index("idx_perfiles_profesionales_calificacion_promedio", "calificacion_promedio"),
    )