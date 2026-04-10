from sqlalchemy import ForeignKey, Index, String, TIMESTAMP, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProfessionalZone(Base):
    __tablename__ = "zonas_profesional"

    id_zona_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="CASCADE"),
        nullable=False,
    )
    departamento: Mapped[str] = mapped_column(String(100), nullable=False, server_default=text("'La Paz'"))
    ciudad: Mapped[str] = mapped_column(String(100), nullable=False, server_default=text("'La Paz'"))
    zona: Mapped[str] = mapped_column(String(100), nullable=False)
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    perfil_profesional = relationship("ProfessionalProfile")

    __table_args__ = (
        UniqueConstraint(
            "id_perfil_profesional",
            "departamento",
            "ciudad",
            "zona",
            name="uq_zona_profesional",
        ),
        Index("idx_zonas_profesional_perfil", "id_perfil_profesional"),
        Index("idx_zonas_profesional_zona", "zona"),
    )