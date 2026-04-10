from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, String, Text, TIMESTAMP, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.utils.enums import TipoDocumentoEnum


class Certification(Base):
    __tablename__ = "certificaciones"

    id_certificacion: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_perfil_profesional: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("perfiles_profesionales.id_perfil_profesional", ondelete="CASCADE"),
        nullable=False,
    )
    tipo_documento: Mapped[TipoDocumentoEnum] = mapped_column(
        Enum(TipoDocumentoEnum, name="tipo_documento_enum"),
        nullable=False,
        server_default=text("'certificado'"),
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    institucion: Mapped[str | None] = mapped_column(String(150))
    ano_emision: Mapped[int | None] = mapped_column(Integer)
    archivo_url: Mapped[str] = mapped_column(Text, nullable=False)
    verificada: Mapped[bool] = mapped_column(nullable=False, server_default=text("FALSE"))
    verificada_por: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="SET NULL"),
    )
    verificada_en: Mapped[str | None] = mapped_column(TIMESTAMP)
    creado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    actualizado_en: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    perfil_profesional = relationship("ProfessionalProfile")
    verificador = relationship("User", foreign_keys=[verificada_por])

    __table_args__ = (
        CheckConstraint(
            "ano_emision IS NULL OR (ano_emision >= 1950 AND ano_emision <= EXTRACT(YEAR FROM CURRENT_DATE) + 1)",
            name="chk_ano_emision",
        ),
        Index("idx_certificaciones_perfil", "id_perfil_profesional"),
        Index("idx_certificaciones_verificada", "verificada"),
    )