from sqlalchemy import Boolean, String, Text, TIMESTAMP, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Specialty(Base):
    __tablename__ = "especialidades"

    id_especialidad: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    codigo: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("TRUE"))
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    perfiles = relationship("ProfessionalSpecialty", back_populates="especialidad")
    solicitudes = relationship("ServiceRequest", back_populates="especialidad")
    busquedas = relationship("SearchHistory", back_populates="especialidad")

    __table_args__ = (
        Index("idx_especialidades_codigo", "codigo"),
    )