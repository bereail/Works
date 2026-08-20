from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class IdentidadNegocio(Base):
    """Fila única con la identidad comercial de PCfix. Se siembra una vez y solo se edita desde Configuración."""

    __tablename__ = "identidad_negocio"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_comercial: Mapped[str] = mapped_column(String(120))
    actividad: Mapped[str] = mapped_column(String(255))
    zona: Mapped[str] = mapped_column(String(120))
    tagline: Mapped[str] = mapped_column(String(255), default="")
    modo_operacion: Mapped[str] = mapped_column(String(20), default="simulacion")  # simulacion | real
    color_primario: Mapped[str] = mapped_column(String(20), default="#2563eb")
    color_acento: Mapped[str] = mapped_column(String(20), default="#0ea5a4")
    identidad_visual_definitiva: Mapped[bool] = mapped_column(default=False)
    actualizado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Servicio(Base):
    """Catálogo de servicios reales de PCfix (sembrado desde 01-Marca/FASE-4-CATALOGO-SERVICIOS.md)."""

    __tablename__ = "servicios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    categoria: Mapped[str] = mapped_column(String(80))
    prioridad: Mapped[str] = mapped_column(String(20))  # verde | amarillo | rojo
    activo: Mapped[bool] = mapped_column(default=True)

    publicaciones: Mapped[list["Publicacion"]] = relationship(back_populates="servicio")
    precios: Mapped[list["Precio"]] = relationship(back_populates="servicio")


class CuentaConectada(Base):
    """Cuentas de redes sociales habilitadas. Tipo siempre 'comercial' — nunca personal."""

    __tablename__ = "cuentas_conectadas"

    id: Mapped[int] = mapped_column(primary_key=True)
    plataforma: Mapped[str] = mapped_column(String(40))  # instagram | facebook
    nombre_cuenta: Mapped[str] = mapped_column(String(120))
    tipo: Mapped[str] = mapped_column(String(20), default="comercial")
    estado_conexion: Mapped[str] = mapped_column(String(20), default="simulado")  # simulado | conectada | error
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
