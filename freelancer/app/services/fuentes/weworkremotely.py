"""We Work Remotely — feed RSS público y oficial de la categoría de programación.

RSS es justamente el canal que la plataforma publica para que terceros redistribuyan
sus avisos, así que no hace falta tocar el HTML del sitio.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from app.services.fuentes.base import OfertaExterna, limpiar_html, pedir_texto

NOMBRE = "weworkremotely"
ETIQUETA = "We Work Remotely"
SITIO = "https://weworkremotely.com"
HORAS_ENTRE_CONSULTAS = 6

URL_RSS = "https://weworkremotely.com/categories/remote-programming-jobs.rss"


def obtener() -> list[OfertaExterna]:
    xml = pedir_texto(URL_RSS)
    raiz = ET.fromstring(xml.encode("utf-8"))

    ofertas = []
    for item in raiz.findall("./channel/item"):
        enlace = _texto(item, "link")
        if not enlace:
            continue

        empresa, titulo = _separar_empresa_y_puesto(_texto(item, "title"))
        categoria = _texto(item, "category")

        ofertas.append(OfertaExterna(
            id_externo=_texto(item, "guid") or enlace,
            titulo=titulo,
            empresa=empresa,
            url=enlace,
            descripcion=limpiar_html(_texto(item, "description")),
            ubicacion=_texto(item, "region") or "Remoto",
            etiquetas=[categoria] if categoria else [],
            fecha_publicacion=_fecha(_texto(item, "pubDate")),
        ))
    return ofertas


def _texto(item: ET.Element, etiqueta: str) -> str:
    nodo = item.find(etiqueta)
    return (nodo.text or "").strip() if nodo is not None else ""


def _separar_empresa_y_puesto(titulo: str) -> tuple[str, str]:
    """En este feed el título viene como 'Empresa: Puesto'."""
    if ": " in titulo:
        empresa, puesto = titulo.split(": ", 1)
        return empresa.strip(), puesto.strip()
    return "", titulo.strip()


def _fecha(valor: str) -> datetime | None:
    if not valor:
        return None
    try:
        fecha = parsedate_to_datetime(valor)
    except (TypeError, ValueError):
        return None
    return fecha if fecha.tzinfo else fecha.replace(tzinfo=timezone.utc)
