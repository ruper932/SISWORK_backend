from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Numeric, String, TIMESTAMP, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SearchHistory(Base):
    __tablename__ = "historial_busquedas"

    id_busqueda: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    id_usuario: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="SET NULL"))
    termino_busqueda: Mapped[str | None] = mapped_column(String(255))
    id_especialidad: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("especialidades.id_especialidad", ondelete="SET NULL"))
    zona: Mapped[str | None] = mapped_column(String(100))
    calificacion_minima: Mapped[float | None] = mapped_column(Numeric(2, 1))
    disponible_ahora: Mapped[bool | None] = mapped_column(Boolean)
    cantidad_resultados: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    buscado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    especialidad = relationship("Specialty", back_populates="busquedas")

    __table_args__ = (
        CheckConstraint(
            "calificacion_minima IS NULL OR (calificacion_minima >= 0 AND calificacion_minima <= 5)",
            name="chk_calificacion_minima",
        ),
    )