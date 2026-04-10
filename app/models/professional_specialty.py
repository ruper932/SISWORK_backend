from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, TIMESTAMP, UniqueConstraint, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import NivelEspecialidadEnum


class ProfessionalSpecialty(Base):
    __tablename__ = "especialidades_profesional"

    id_especialidad_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="CASCADE"),
        nullable=False,
    )
    id_especialidad: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("especialidades.id_especialidad", ondelete="RESTRICT"),
        nullable=False,
    )
    nivel: Mapped[NivelEspecialidadEnum] = mapped_column(
        Enum(NivelEspecialidadEnum, name="nivel_especialidad_enum"),
        nullable=False,
        server_default=text("'basico'"),
    )
    anos_experiencia: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    perfil_profesional = relationship("ProfessionalProfile", back_populates="especialidades")
    especialidad = relationship("Specialty", back_populates="perfiles")

    __table_args__ = (
        UniqueConstraint("id_perfil_profesional", "id_especialidad", name="uq_especialidades_profesional"),
        CheckConstraint("anos_experiencia >= 0", name="chk_anos_exp_especialidad"),
        Index("idx_especialidades_profesional_perfil", "id_perfil_profesional"),
        Index("idx_especialidades_profesional_especialidad", "id_especialidad"),
    )