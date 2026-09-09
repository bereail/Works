"""Get on Board — API JSON pública y oficial (https://www.getonbrd.com/api/v0).

Es la fuente más relevante para Berenice: avisos de LatAm (Chile, Argentina, Perú,
Colombia, México), muchos en español y con modalidad remota o híbrida.
"""

from app.services.fuentes.base import OfertaExterna, fecha_desde_epoch, limpiar_html, pedir_json

NOMBRE = "getonbrd"
ETIQUETA = "Get on Board"
SITIO = "https://www.getonbrd.com"
HORAS_ENTRE_CONSULTAS = 6

URL_CATEGORIA = "https://www.getonbrd.com/api/v0/categories/{categoria}/jobs"
CATEGORIAS = ["programming"]
AVISOS_POR_PAGINA = 50
PAGINAS = 2


def obtener() -> list[OfertaExterna]:
    ofertas = []
    for categoria in CATEGORIAS:
        for pagina in range(1, PAGINAS + 1):
            datos = pedir_json(
                URL_CATEGORIA.format(categoria=categoria),
                params={"page": pagina, "per_page": AVISOS_POR_PAGINA, "expand[]": "company"},
            )
            avisos = datos.get("data", [])
            ofertas.extend(_convertir(aviso) for aviso in avisos)
            if pagina >= datos.get("meta", {}).get("total_pages", 1):
                break
    return [o for o in ofertas if o.titulo]


def _convertir(aviso: dict) -> OfertaExterna:
    atributos = aviso.get("attributes", {})
    identificador = str(aviso.get("id", ""))

    return OfertaExterna(
        id_externo=identificador,
        titulo=atributos.get("title") or "",
        empresa=_nombre_empresa(atributos),
        url=f"{SITIO}/jobs/{identificador}",
        descripcion=limpiar_html(atributos.get("description") or ""),
        ubicacion=_armar_ubicacion(atributos),
        salario=_armar_salario(atributos),
        etiquetas=_armar_etiquetas(atributos),
        fecha_publicacion=fecha_desde_epoch(atributos.get("published_at")),
    )


def _nombre_empresa(atributos: dict) -> str:
    empresa = (atributos.get("company") or {}).get("data") or {}
    return (empresa.get("attributes") or {}).get("name", "")


def _armar_ubicacion(atributos: dict) -> str:
    paises = atributos.get("countries") or []
    modalidad = {"fully_remote": "Remoto", "hybrid": "Híbrido", "no_remote": "Presencial"}.get(
        atributos.get("remote_modality") or "", ""
    )
    partes = [p for p in [modalidad, ", ".join(str(p) for p in paises)] if p]
    return " - ".join(partes)


def _armar_salario(atributos: dict) -> str:
    minimo, maximo = atributos.get("min_salary"), atributos.get("max_salary")
    if not minimo and not maximo:
        return ""
    try:
        if minimo and maximo:
            return f"USD {int(minimo):,}-{int(maximo):,}".replace(",", ".")
        return f"USD {int(minimo or maximo):,}".replace(",", ".")
    except (TypeError, ValueError):
        return ""


def _armar_etiquetas(atributos: dict) -> list[str]:
    etiquetas = []
    if atributos.get("category_name"):
        etiquetas.append(str(atributos["category_name"]))
    if atributos.get("remote_modality") == "fully_remote":
        etiquetas.append("remote")
    for beneficio in (atributos.get("perks") or [])[:4]:
        etiquetas.append(str(beneficio).replace("_", " "))
    return etiquetas
