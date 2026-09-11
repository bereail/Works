from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Publicacion(Base):
    """Una publicación (real o simulada) en una red social, con todo su ciclo de aprobación."""

    __tablename__ = "publicaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    plataforma: Mapped[str] = mapped_column(String(40))  # instagram | facebook
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    formato: Mapped[str] = mapped_column(String(40))  # imagen | carrusel | reel | historia | texto
    tema: Mapped[str] = mapped_column(String(255))
    pilar: Mapped[str] = mapped_column(String(60), default="")  # criterio_tecnico | transparencia | confianza | tecnologia
    objetivo: Mapped[str] = mapped_column(String(80), default="")  # generar_consultas | reconocimiento | recuperar_clientes...
    texto: Mapped[str] = mapped_column(Text, default="")
    cta: Mapped[str] = mapped_column(String(255), default="")
    hashtags: Mapped[str] = mapped_column(String(500), default="")  # solo Instagram — separados por espacio, con #
    estado: Mapped[str] = mapped_column(String(20), default="borrador")  # borrador|previsualizado|aprobado|publicado|simulado|error
    origen_datos: Mapped[str] = mapped_column(String(20), default="simulado")  # real | simulado
    id_publicacion_externa: Mapped[str] = mapped_column(String(60), default="")  # post_id (facebook) | media_id (instagram) cuando se publicó de verdad
    servicio_id: Mapped[int | None] = mapped_column(ForeignKey("servicios.id"), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    servicio: Mapped["Servicio"] = relationship(back_populates="publicaciones")
    metricas: Mapped[list["MetricaPublicacion"]] = relationship(back_populates="publicacion", order_by="MetricaPublicacion.fecha_medicion")
    flyers: Mapped[list["Flyer"]] = relationship(back_populates="publicacion")


class MetricaPublicacion(Base):
    """Snapshot de métricas de una publicación en una fecha dada — histórico, no un valor fijo."""

    __tablename__ = "metricas_publicacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    publicacion_id: Mapped[int] = mapped_column(ForeignKey("publicaciones.id"))
    fecha_medicion: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    alcance: Mapped[int] = mapped_column(default=0)
    visualizaciones: Mapped[int] = mapped_column(default=0)
    interacciones: Mapped[int] = mapped_column(default=0)
    comentarios: Mapped[int] = mapped_column(default=0)
    compartidos: Mapped[int] = mapped_column(default=0)
    guardados: Mapped[int] = mapped_column(default=0)
    clics: Mapped[int] = mapped_column(default=0)
    consultas: Mapped[int] = mapped_column(default=0)
    origen_datos: Mapped[str] = mapped_column(String(20), default="simulado")

    publicacion: Mapped["Publicacion"] = relationship(back_populates="metricas")


class SeguidorHistorico(Base):
    """Cantidad de seguidores por plataforma en una fecha, para calcular crecimiento."""

    __tablename__ = "seguidores_historico"

    id: Mapped[int] = mapped_column(primary_key=True)
    plataforma: Mapped[str] = mapped_column(String(40))
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    cantidad: Mapped[int] = mapped_column(default=0)
    origen_datos: Mapped[str] = mapped_column(String(20), default="simulado")


class Flyer(Base):
    """Pieza gráfica generada por composición de plantilla para una publicación."""

    __tablename__ = "flyers"

    id: Mapped[int] = mapped_column(primary_key=True)
    publicacion_id: Mapped[int] = mapped_column(ForeignKey("publicaciones.id"))
    titular: Mapped[str] = mapped_column(String(255))
    subtitulo: Mapped[str] = mapped_column(String(255), default="")
    cta: Mapped[str] = mapped_column(String(120), default="")
    plantilla: Mapped[str] = mapped_column(String(60), default="estandar")
    archivo_generado: Mapped[str] = mapped_column(String(255), default="")
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    publicacion: Mapped["Publicacion"] = relationship(back_populates="flyers")


class Campania(Base):
    """Agrupa publicaciones bajo un objetivo comercial común."""

    __tablename__ = "campanias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255))
    objetivo: Mapped[str] = mapped_column(String(255))
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    fecha_fin: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resultados_resumen: Mapped[str] = mapped_column(Text, default="")
    origen_oportunidad_id: Mapped[int | None] = mapped_column(ForeignKey("oportunidades.id"), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
