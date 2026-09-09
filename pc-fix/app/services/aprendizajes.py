"""Motor de aprendizaje: convierte los resultados de la analítica en filas de
`aprendizajes`, distinguiendo siempre DATO / INTERPRETACION / HIPOTESIS / RECOMENDACION
(sección 5 del pedido: nunca presentar una hipótesis como si fuera un dato).

Umbral de confianza por volumen de muestra — coherente con la regla ya
definida en 07-CRM/ESPECIFICACION-CRM.md: no se predice nada con poco volumen.
"""

from sqlalchemy.orm import Session

from app.models import Aprendizaje
from app.services.analitica import (
    PublicacionAnalizada,
    rendimiento_por_formato,
    rendimiento_por_horario,
    rendimiento_por_pilar,
)

UMBRAL_CONFIANZA_ALTA = 7
UMBRAL_CONFIANZA_MEDIA = 3


def _nivel_confianza(cantidad_publicaciones: int) -> str:
    if cantidad_publicaciones >= UMBRAL_CONFIANZA_ALTA:
        return "alta"
    if cantidad_publicaciones >= UMBRAL_CONFIANZA_MEDIA:
        return "media"
    return "baja"


def generar_aprendizajes(sesion: Session, analizadas: list[PublicacionAnalizada]) -> list[Aprendizaje]:
    if not analizadas:
        return []

    nuevos: list[Aprendizaje] = []
    total_publicaciones = len(analizadas)

    por_pilar = rendimiento_por_pilar(analizadas)
    por_formato = rendimiento_por_formato(analizadas)
    por_horario = rendimiento_por_horario(analizadas)

    if por_pilar:
        pilar_top, datos_pilar = next(iter(por_pilar.items()))
        nuevos.append(Aprendizaje(
            texto=f"El pilar de contenido '{pilar_top}' tuvo la tasa de interacción promedio más alta "
                  f"({datos_pilar['tasa_interaccion_promedio']:.1%}) sobre {datos_pilar['cantidad_publicaciones']} "
                  f"publicación(es) de un total de {total_publicaciones}.",
            tipo="DATO",
            nivel_confianza=_nivel_confianza(datos_pilar["cantidad_publicaciones"]),
            fuente=f"rendimiento_por_pilar sobre {total_publicaciones} publicaciones analizadas",
        ))

    if por_formato:
        formato_top, datos_formato = next(iter(por_formato.items()))
        nuevos.append(Aprendizaje(
            texto=f"El formato '{formato_top}' tuvo la tasa de interacción promedio más alta "
                  f"({datos_formato['tasa_interaccion_promedio']:.1%}) sobre {datos_formato['cantidad_publicaciones']} publicación(es).",
            tipo="DATO",
            nivel_confianza=_nivel_confianza(datos_formato["cantidad_publicaciones"]),
            fuente=f"rendimiento_por_formato sobre {total_publicaciones} publicaciones analizadas",
        ))

        if por_pilar and por_formato:
            confianza_combinada = min(datos_pilar["cantidad_publicaciones"], datos_formato["cantidad_publicaciones"])
            nuevos.append(Aprendizaje(
                texto=f"El contenido de '{pilar_top}' en formato '{formato_top}' parece ser la combinación que más "
                      f"interés genera hasta ahora.",
                tipo="INTERPRETACION" if confianza_combinada >= UMBRAL_CONFIANZA_MEDIA else "HIPOTESIS",
                nivel_confianza=_nivel_confianza(confianza_combinada),
                fuente=f"cruce de rendimiento_por_pilar y rendimiento_por_formato ({confianza_combinada} publicaciones en común)",
            ))

    if por_horario:
        horario_top, datos_horario = next(iter(por_horario.items()))
        nuevos.append(Aprendizaje(
            texto=f"Las publicaciones a las {horario_top} tuvieron, en promedio, mejor tasa de interacción "
                  f"({datos_horario['tasa_interaccion_promedio']:.1%}) que el resto de los horarios probados.",
            tipo="DATO" if datos_horario["cantidad_publicaciones"] >= UMBRAL_CONFIANZA_MEDIA else "HIPOTESIS",
            nivel_confianza=_nivel_confianza(datos_horario["cantidad_publicaciones"]),
            fuente=f"rendimiento_por_horario sobre {total_publicaciones} publicaciones analizadas",
        ))

    if por_pilar:
        pilar_top, datos_pilar = next(iter(por_pilar.items()))
        nuevos.append(Aprendizaje(
            texto=f"Conviene seguir probando contenido del pilar '{pilar_top}'"
                  + (f", en formato '{next(iter(por_formato))}'" if por_formato else "")
                  + (f" y publicado cerca de las {next(iter(por_horario))}" if por_horario else "")
                  + " para confirmar si el patrón se sostiene con más volumen.",
            tipo="RECOMENDACION",
            nivel_confianza=_nivel_confianza(datos_pilar["cantidad_publicaciones"]),
            fuente="combinación de los aprendizajes de esta misma corrida de Automatizar",
        ))

    sesion.add_all(nuevos)
    sesion.commit()
    return nuevos
