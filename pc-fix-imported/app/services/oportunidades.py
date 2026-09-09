"""Detección de oportunidades comerciales por reglas explicables sobre datos
existentes — nada de predicción con poco volumen (misma regla que el CRM)."""

from sqlalchemy.orm import Session

from app.models import Oportunidad, Publicacion, Servicio
from app.services.analitica import PublicacionAnalizada, rendimiento_por_formato, rendimiento_por_horario, rendimiento_por_pilar

FORMATOS_ESTANDAR = ["imagen", "carrusel", "reel", "historia", "post estático"]
UMBRAL_MUESTRA_CHICA = 3


def detectar_oportunidades(sesion: Session, analizadas: list[PublicacionAnalizada]) -> list[Oportunidad]:
    if not analizadas:
        return []

    nuevas: list[Oportunidad] = []

    por_pilar = rendimiento_por_pilar(analizadas)
    if por_pilar:
        pilar_top, datos = next(iter(por_pilar.items()))
        if datos["cantidad_publicaciones"] < UMBRAL_MUESTRA_CHICA:
            nuevas.append(Oportunidad(
                titulo=f"Profundizar contenido de '{pilar_top}'",
                explicacion=f"Es el pilar con mejor tasa de interacción promedio hasta ahora "
                            f"({datos['tasa_interaccion_promedio']:.1%}), pero todavía con pocas publicaciones "
                            f"({datos['cantidad_publicaciones']}) como para confirmarlo con solidez.",
                datos_utilizados=f"rendimiento_por_pilar: {datos}",
                nivel_confianza="baja" if datos["cantidad_publicaciones"] < 2 else "media",
                accion_recomendada=f"Programar 2-3 publicaciones más del pilar '{pilar_top}' en las próximas semanas.",
            ))

    formatos_probados = set(rendimiento_por_formato(analizadas).keys())
    for formato in FORMATOS_ESTANDAR:
        if formato not in formatos_probados:
            nuevas.append(Oportunidad(
                titulo=f"Probar el formato '{formato}'",
                explicacion=f"Todavía no hay publicaciones registradas en formato '{formato}' — no se puede saber "
                            f"si funciona mejor o peor que los formatos ya probados.",
                datos_utilizados=f"formatos ya probados: {sorted(formatos_probados)}",
                nivel_confianza="baja",
                accion_recomendada=f"Probar una publicación en formato '{formato}' para tener un primer dato.",
            ))

    por_horario = rendimiento_por_horario(analizadas)
    if len(por_horario) >= 2:
        horario_top, datos_top = next(iter(por_horario.items()))
        total_en_top = datos_top["cantidad_publicaciones"]
        total_general = sum(d["cantidad_publicaciones"] for d in por_horario.values())
        if total_en_top < total_general / 2:
            nuevas.append(Oportunidad(
                titulo=f"Concentrar más publicaciones a las {horario_top}",
                explicacion=f"Las publicaciones a las {horario_top} tienen la mejor tasa de interacción promedio "
                            f"({datos_top['tasa_interaccion_promedio']:.1%}), pero son minoría del calendario actual "
                            f"({total_en_top} de {total_general}).",
                datos_utilizados=f"rendimiento_por_horario: {por_horario}",
                nivel_confianza="media" if total_en_top >= UMBRAL_MUESTRA_CHICA else "baja",
                accion_recomendada=f"Mover el próximo lote de publicaciones al horario de las {horario_top}.",
            ))

    servicios_promocionados = {p.servicio_nombre for p in analizadas}
    servicios_prioritarios = sesion.query(Servicio).filter(Servicio.prioridad == "verde", Servicio.activo.is_(True)).all()
    for servicio in servicios_prioritarios:
        if servicio.nombre not in servicios_promocionados:
            nuevas.append(Oportunidad(
                titulo=f"Contenido sin probar: {servicio.nombre}",
                explicacion=f"'{servicio.nombre}' es un servicio de prioridad alta en el catálogo "
                            f"(01-Marca/FASE-4-CATALOGO-SERVICIOS.md) que todavía no tiene ninguna publicación asociada.",
                datos_utilizados="catálogo de servicios (prioridad verde) vs. servicios ya promocionados en publicaciones",
                nivel_confianza="baja",
                accion_recomendada=f"Planificar una publicación sobre '{servicio.nombre}'.",
            ))

    sesion.add_all(nuevas)
    sesion.commit()
    return nuevas
