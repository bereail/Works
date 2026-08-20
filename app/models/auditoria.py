from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RegistroAccion(Base):
    """Auditoría de todo lo que hizo el sistema: herramienta usada, datos, resultado y estado de aprobación."""

    __tablename__ = "registro_acciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    herramienta: Mapped[str] = mapped_column(String(120))
    datos_utilizados: Mapped[str] = mapped_column(Text, default="")
    resultado: Mapped[str] = mapped_column(Text, default="")
    requirio_aprobacion: Mapped[bool] = mapped_column(Boolean, default=False)
    aprobado: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
