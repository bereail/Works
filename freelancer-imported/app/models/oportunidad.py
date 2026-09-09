from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OportunidadFreelance(Base):
    """Oferta de trabajo o proyecto freelance cargada a mano por Berenice — sin scraping,
    coherente con la decisión de no saltear los términos de servicio de LinkedIn/Workana/etc."""

    __tablename__ = "oportunidades_freelance"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    cliente_o_empresa: Mapped[str] = mapped_column(String(255), default="")
    fuente: Mapped[str] = mapped_column(String(50), default="otro")  # linkedin | getonboard | referido | otro
    url: Mapped[str] = mapped_column(String(500), default="")
    tipo: Mapped[str] = mapped_column(String(30), default="proyecto_freelance")  # proyecto_freelance | empleo_relacion_dependencia | subcontrato
    estado: Mapped[str] = mapped_column(String(30), default="por_postular")  # por_postular | postulada | en_conversacion | ganada | rechazada | descartada
    notas: Mapped[str] = mapped_column(Text, default="")
    fecha_encontrada: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_postulacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
