"""Piezas compartidas por todas las fuentes de ofertas.

Regla del proyecto: cada fuente consume una API o un feed RSS **público y oficial**
de la plataforma. Nada de scraping de HTML ni de plataformas que lo prohíben en sus
términos (LinkedIn, Workana, Upwork, Indeed, Glassdoor).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser

import httpx

AGENTE_USUARIO = "BuscadorFreelance/1.0 (herramienta personal de busqueda laboral)"  # sin tildes: va en una cabecera HTTP
SEGUNDOS_ESPERA = 30
LARGO_MAXIMO_DESCRIPCION = 1200


@dataclass
class OfertaExterna:
    """Una oferta tal como la devuelve una fuente, antes de guardarse en la base."""

    id_externo: str
    titulo: str
    empresa: str = ""
    url: str = ""
    descripcion: str = ""
    ubicacion: str = ""
    salario: str = ""
    etiquetas: list[str] = field(default_factory=list)
    fecha_publicacion: datetime | None = None
    tipo: str = "empleo_relacion_dependencia"

    @property
    def texto_completo(self) -> str:
        """Todo el texto buscable de la oferta, para medir relevancia."""
        return " ".join([self.titulo, self.empresa, self.ubicacion, " ".join(self.etiquetas), self.descripcion]).lower()


class _ExtractorDeTexto(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.partes: list[str] = []

    def handle_data(self, data: str) -> None:
        self.partes.append(data)

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in ("p", "br", "li", "div", "h1", "h2", "h3", "h4"):
            self.partes.append("\n")


def limpiar_html(texto: str, largo_maximo: int = LARGO_MAXIMO_DESCRIPCION) -> str:
    """Convierte el HTML que mandan las APIs en texto plano legible y acotado."""
    if not texto:
        return ""
    extractor = _ExtractorDeTexto()
    try:
        extractor.feed(texto)
    except Exception:
        return unescape(texto)[:largo_maximo]

    plano = unescape("".join(extractor.partes))
    lineas = [linea.strip() for linea in plano.splitlines()]
    limpio = "\n".join(linea for linea in lineas if linea)
    if len(limpio) > largo_maximo:
        limpio = limpio[:largo_maximo].rsplit(" ", 1)[0] + "..."
    return limpio


def fecha_desde_epoch(valor) -> datetime | None:
    try:
        return datetime.fromtimestamp(int(valor), tz=timezone.utc)
    except (TypeError, ValueError):
        return None


def fecha_desde_iso(valor: str) -> datetime | None:
    if not valor:
        return None
    try:
        fecha = datetime.fromisoformat(valor.replace("Z", "+00:00"))
    except ValueError:
        return None
    return fecha if fecha.tzinfo else fecha.replace(tzinfo=timezone.utc)


def pedir_json(url: str, params: dict | None = None):
    respuesta = httpx.get(
        url,
        params=params,
        headers={"User-Agent": AGENTE_USUARIO, "Accept": "application/json"},
        timeout=SEGUNDOS_ESPERA,
        follow_redirects=True,
    )
    respuesta.raise_for_status()
    return respuesta.json()


def pedir_texto(url: str) -> str:
    respuesta = httpx.get(
        url,
        headers={"User-Agent": AGENTE_USUARIO},
        timeout=SEGUNDOS_ESPERA,
        follow_redirects=True,
    )
    respuesta.raise_for_status()
    return respuesta.text
