from sqlalchemy import Enum, ForeignKey, Index, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import TipoReporteEnum


class AdminReport(Base):
    __tablename__ = "reportes_administrativos"

    id_reporte: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    generado_por: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="RESTRICT"),
        nullable=False,
    )
    tipo_reporte: Mapped[TipoReporteEnum] = mapped_column(
        Enum(TipoReporteEnum, name="tipo_reporte_enum"),
        nullable=False,
    )
    parametros_json: Mapped[dict | None] = mapped_column(JSONB)
    generado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    archivo_url: Mapped[str | None] = mapped_column(Text)

    generador = relationship("User", foreign_keys=[generado_por])

    __table_args__ = (
        Index("idx_reportes_administrativos_generado_por", "generado_por"),
        Index("idx_reportes_administrativos_tipo", "tipo_reporte"),
    )