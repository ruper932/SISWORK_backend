from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Index, TIMESTAMP, Time, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import DiaSemanaEnum


class Availability(Base):
    __tablename__ = "disponibilidades_profesional"

    id_disponibilidad: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="CASCADE"),
        nullable=False,
    )
    dia_semana: Mapped[DiaSemanaEnum] = mapped_column(
        Enum(DiaSemanaEnum, name="dia_semana_enum"),
        nullable=False,
    )
    hora_inicio: Mapped[str] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[str] = mapped_column(Time, nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("TRUE"))
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    perfil_profesional = relationship("ProfessionalProfile")

    __table_args__ = (
        CheckConstraint("hora_inicio < hora_fin", name="chk_horario_disponibilidad"),
        UniqueConstraint(
            "id_perfil_profesional",
            "dia_semana",
            "hora_inicio",
            "hora_fin",
            name="uq_disponibilidad_profesional",
        ),
        Index("idx_disponibilidades_perfil", "id_perfil_profesional"),
        Index("idx_disponibilidades_dia", "dia_semana"),
    )