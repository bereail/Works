from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Aprendizaje(Base):
    """Conclusión obtenida a partir de datos. El campo `tipo` distingue dato/interpretación/hipótesis/recomendación."""

    __tablename__ = "aprendizajes"

    id: Mapped[int] = mapped_column(primary_key=True)
    texto: Mapped[str] = mapped_column(Text)
    tipo: Mapped[str] = mapped_column(String(20))  # DATO | INTERPRETACION | HIPOTESIS | RECOMENDACION
    nivel_confianza: Mapped[str] = mapped_column(String(20), default="media")  # baja | media | alta
    fuente: Mapped[str] = mapped_column(Text, default="")  # descripción de qué publicaciones/datos lo sostienen
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Oportunidad(Base):
    """Oportunidad comercial detectada por reglas sobre datos existentes."""

    __tablename__ = "oportunidades"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    explicacion: Mapped[str] = mapped_column(Text)
    datos_utilizados: Mapped[str] = mapped_column(Text)
    nivel_confianza: Mapped[str] = mapped_column(String(20), default="media")
    accion_recomendada: Mapped[str] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(30), default="nueva")  # nueva | convertida_en_campania | descartada
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Decision(Base):
    """Bitácora de decisiones y recomendaciones tomadas, con su contexto y resultado."""

    __tablename__ = "decisiones"

    id: Mapped[int] = mapped_column(primary_key=True)
    texto: Mapped[str] = mapped_column(Text)
    contexto: Mapped[str] = mapped_column(Text, default="")
    resultado: Mapped[str] = mapped_column(Text, default="")
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Precio(Base):
    """Precio de un servicio en una fecha. Queda vacía hasta tener datos confiables — nunca se inventa."""

    __tablename__ = "precios"

    id: Mapped[int] = mapped_column(primary_key=True)
    servicio_id: Mapped[int] = mapped_column(ForeignKey("servicios.id"))
    precio: Mapped[float] = mapped_column()
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    observaciones: Mapped[str] = mapped_column(Text, default="")

    servicio: Mapped["Servicio"] = relationship(back_populates="precios")
