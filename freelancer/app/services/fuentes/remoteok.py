"""Remote OK — API JSON pública y oficial (https://remoteok.com/api).

Sus términos piden dos cosas que esta app cumple: enlazar de vuelta al aviso
original en remoteok.com (la ficha linkea a `url`) y nombrar a Remote OK como
fuente (se guarda en el campo `fuente` y se muestra en la ficha).
"""

from app.services.fuentes.base import OfertaExterna, fecha_desde_epoch, limpiar_html, pedir_json

NOMBRE = "remoteok"
ETIQUETA = "Remote OK"
SITIO = "https://remoteok.com"
HORAS_ENTRE_CONSULTAS = 6

URL_API = "https://remoteok.com/api"

# Remote OK no tiene un campo de tipo de contrato separado — a veces lo delata un
# tag suelto entre los que ya trae el aviso ("part time", "contract", etc).
TAGS_FREELANCE = {"part time", "part-time", "freelance", "contract", "contractor"}


def obtener() -> list[OfertaExterna]:
    datos = pedir_json(URL_API)

    ofertas = []
    for aviso in datos:
        # El primer elemento del array no es una oferta: es el aviso legal de la API.
        if not isinstance(aviso, dict) or not aviso.get("id"):
            continue

        etiquetas = aviso.get("tags") or []
        if isinstance(etiquetas, str):
            etiquetas = [etiquetas]
        etiquetas = [str(e) for e in etiquetas]

        ofertas.append(OfertaExterna(
            id_externo=str(aviso["id"]),
            titulo=aviso.get("position") or "",
            empresa=aviso.get("company") or "",
            url=aviso.get("url") or aviso.get("apply_url") or "",
            descripcion=limpiar_html(aviso.get("description") or ""),
            ubicacion=aviso.get("location") or "Remoto",
            salario=_armar_salario(aviso),
            etiquetas=etiquetas,
            fecha_publicacion=fecha_desde_epoch(aviso.get("epoch")),
            tipo="proyecto_freelance" if _es_freelance(etiquetas) else "empleo_relacion_dependencia",
        ))
    return ofertas


def _es_freelance(etiquetas: list[str]) -> bool:
    return any(etiqueta.strip().lower() in TAGS_FREELANCE for etiqueta in etiquetas)


def _armar_salario(aviso: dict) -> str:
    minimo, maximo = aviso.get("salary_min"), aviso.get("salary_max")
    if not minimo and not maximo:
        return ""
    try:
        if minimo and maximo:
            return f"USD {int(minimo):,}-{int(maximo):,}".replace(",", ".")
        return f"USD {int(minimo or maximo):,}".replace(",", ".")
    except (TypeError, ValueError):
        return ""
