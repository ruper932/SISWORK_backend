from sqlalchemy import Boolean, ForeignKey, Numeric, String, TIMESTAMP, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Address(Base):
    __tablename__ = "direcciones_usuario"

    id_direccion: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    id_usuario: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )

    departamento: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        server_default=text("'La Paz'")
    )
    ciudad: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        server_default=text("'La Paz'")
    )
    zona: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str | None] = mapped_column(String(255))
    referencia: Mapped[str | None] = mapped_column(String)
    latitud: Mapped[float | None] = mapped_column(Numeric(10, 7))
    longitud: Mapped[float | None] = mapped_column(Numeric(10, 7))
    es_principal: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("TRUE")
    )
    creado_en: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    actualizado_en: Mapped[str] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    usuario = relationship("User", back_populates="direcciones")

    __table_args__ = (
        Index(
            "uq_direccion_principal_usuario",
            "id_usuario",
            unique=True,
            postgresql_where=text("es_principal = TRUE"),
        ),
        Index("idx_direcciones_usuario_id_usuario", "id_usuario"),
        Index("idx_direcciones_usuario_zona", "zona"),
    )