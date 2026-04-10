from sqlalchemy import CheckConstraint, Date, Enum, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import EstadoUsuarioEnum, RolUsuarioEnum, SexoEnum


class User(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20))
    numero_whatsapp: Mapped[str | None] = mapped_column(String(20))
    foto_perfil_url: Mapped[str | None] = mapped_column(Text)
    fecha_nacimiento: Mapped[str | None] = mapped_column(Date)
    sexo: Mapped[SexoEnum] = mapped_column(
        Enum(SexoEnum, name="sexo_enum"),
        nullable=False,
        server_default=text("'prefiero_no_decir'"),
    )
    rol: Mapped[RolUsuarioEnum] = mapped_column(
        Enum(RolUsuarioEnum, name="rol_usuario_enum"),
        nullable=False,
        server_default=text("'cliente'"),
    )
    estado: Mapped[EstadoUsuarioEnum] = mapped_column(
        Enum(EstadoUsuarioEnum, name="estado_usuario_enum"),
        nullable=False,
        server_default=text("'activo'"),
    )
    correo_verificado_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    ultimo_acceso_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    intentos_fallidos: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    token_recuperacion: Mapped[str | None] = mapped_column(String(255))
    token_recuperacion_expira_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    eliminado_en: Mapped[str | None] = mapped_column(TIMESTAMP)

    direcciones = relationship("Address", back_populates="usuario", cascade="all, delete-orphan")
    perfil_profesional = relationship("ProfessionalProfile", back_populates="usuario", uselist=False, foreign_keys="ProfessionalProfile.id_usuario")
    solicitudes = relationship("ServiceRequest", back_populates="cliente", foreign_keys="ServiceRequest.id_cliente")
    calificaciones = relationship("Rating", back_populates="cliente", foreign_keys="Rating.id_cliente")
    reportes_generados = relationship("AdminReport", foreign_keys="AdminReport.generado_por")
    registros_auditoria = relationship("AuditLog", foreign_keys="AuditLog.id_usuario_actor")
    notas_administrativas = relationship("AdministrativeNote", foreign_keys="AdministrativeNote.id_autor")

    __table_args__ = (
        CheckConstraint("position('@' in correo) > 1", name="chk_usuarios_correo_formato"),
    )