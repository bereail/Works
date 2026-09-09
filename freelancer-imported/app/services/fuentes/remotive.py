"""Remotive — API JSON pública y oficial (https://remotive.com/api-documentation).

Sus términos piden enlazar de vuelta al aviso en remotive.com y nombrar a Remotive
como fuente (ambas cosas se cumplen en la ficha de la oferta), y explícitamente
piden **no consultar más de 4 veces por día**: por eso `HORAS_ENTRE_CONSULTAS`
es 6 y la ingesta respeta ese mínimo.
"""

from app.services.fuentes.base import OfertaExterna, fecha_desde_iso, limpiar_html, pedir_json

NOMBRE = "remotive"
ETIQUETA = "Remotive"
SITIO = "https://remotive.com"
HORAS_ENTRE_CONSULTAS = 6

URL_API = "https://remotive.com/api/remote-jobs"

TIPOS_POR_CONTRATO = {
    "contract": "proyecto_freelance",
    "freelance": "proyecto_freelance",
    "part_time": "proyecto_freelance",
}


def obtener() -> list[OfertaExterna]:
    datos = pedir_json(URL_API)

    ofertas = []
    for aviso in datos.get("jobs", []):
        etiquetas = aviso.get("tags") or []
        if isinstance(etiquetas, str):
            etiquetas = [etiquetas]

        ofertas.append(OfertaExterna(
            id_externo=str(aviso.get("id", "")),
            titulo=aviso.get("title") or "",
            empresa=aviso.get("company_name") or "",
            url=aviso.get("url") or "",
            descripcion=limpiar_html(aviso.get("description") or ""),
            ubicacion=aviso.get("candidate_required_location") or "Remoto",
            salario=aviso.get("salary") or "",
            etiquetas=[str(e) for e in etiquetas],
            fecha_publicacion=fecha_desde_iso(aviso.get("publication_date") or ""),
            tipo=TIPOS_POR_CONTRATO.get(aviso.get("job_type", ""), "empleo_relacion_dependencia"),
        ))
    return ofertas
