from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

ORIGEN_MANUAL = "manual"
ORIGEN_IMPORTADA = "importada"


class OportunidadFreelance(Base):
    """Oferta de trabajo o proyecto freelance.

    Puede entrar de dos maneras: cargada a mano por Berenice, o importada
    automáticamente desde una API/RSS pública y oficial de la plataforma
    (nunca por scraping, coherente con la decisión de no saltear los términos
    de servicio de LinkedIn/Workana/etc.).
    """

    __tablename__ = "oportunidades_freelance"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    cliente_o_empresa: Mapped[str] = mapped_column(String(255), default="")
    fuente: Mapped[str] = mapped_column(String(50), default="otro")  # linkedin | getonbrd | remoteok | remotive | weworkremotely | referido | otro
    url: Mapped[str] = mapped_column(String(500), default="")
    tipo: Mapped[str] = mapped_column(String(30), default="proyecto_freelance")  # proyecto_freelance | empleo_relacion_dependencia | subcontrato
    estado: Mapped[str] = mapped_column(String(30), default="por_postular")  # nueva | por_postular | postulada | en_conversacion | ganada | rechazada | descartada
    notas: Mapped[str] = mapped_column(Text, default="")
    fecha_encontrada: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    fecha_postulacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # --- campos que solo se completan cuando la oferta llega importada ---
    origen: Mapped[str] = mapped_column(String(20), default=ORIGEN_MANUAL)
    id_externo: Mapped[str] = mapped_column(String(200), default="")
    descripcion: Mapped[str] = mapped_column(Text, default="")
    ubicacion: Mapped[str] = mapped_column(String(200), default="")
    salario: Mapped[str] = mapped_column(String(120), default="")
    etiquetas: Mapped[str] = mapped_column(String(400), default="")
    puntaje: Mapped[int] = mapped_column(Integer, default=0)
    fecha_publicacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    @property
    def lista_etiquetas(self) -> list[str]:
        return [e.strip() for e in self.etiquetas.split(",") if e.strip()]


class EstadoFuente(Base):
    """Última vez que se consultó cada fuente, para no golpear sus APIs más de lo
    que sus términos permiten (Remotive, por ejemplo, pide un máximo de 4 consultas
    por día) y para poder mostrar en pantalla cuándo fue la última búsqueda."""

    __tablename__ = "estado_fuentes"

    nombre: Mapped[str] = mapped_column(String(50), primary_key=True)
    ultima_consulta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ultimo_resultado: Mapped[str] = mapped_column(String(300), default="")
    ultimo_error: Mapped[str] = mapped_column(String(300), default="")
