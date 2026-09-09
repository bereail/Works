"""Generador de copy por plantillas (Fase 1: sin IA generativa, por decisión
de no sumar costo de API todavía — ver plan de arquitectura).

Cada plantilla está atada a un objetivo comercial y usa el tagline real de
marca ("Se entiende lo que te arreglan.", 01-Marca/FASE-3-POSICIONAMIENTO.md).
"""

from dataclasses import dataclass

TAGLINE = "Se entiende lo que te arreglan."

PLANTILLAS_POR_OBJETIVO = {
    "generar_consultas": [
        "¿Tu equipo tiene que ver con {servicio}? Te lo explicamos en criollo antes de tocarlo. {tagline}",
        "Antes de gastar de más: capaz tu problema se resuelve con {servicio}. Te lo confirmamos sin compromiso.",
        "{servicio}, con diagnóstico real — no a prueba y error. Te contamos qué tiene tu equipo, en criollo.",
    ],
    "generar_confianza": [
        "En PCfix el presupuesto de {servicio} sale siempre por escrito, sin letra chica. {tagline}",
        "Te mostramos cómo trabajamos con {servicio} — sin vueltas, sin sorpresas al final.",
        "Dejar tu compu con alguien da un poco de cosa — se ven fotos, cuentas, todo. En PCfix tus datos no se tocan: solo se hace lo del {servicio}, nada más.",
    ],
    "reconocimiento": [
        "{tagline} Así encaramos cada trabajo de {servicio}.",
        "Un poco de cómo trabajamos {servicio} en PCfix — criterio técnico real, explicado en criollo.",
        "En PCfix el diagnóstico se hace con criterio técnico real, no a prueba y error. Así se nota en cada {servicio}.",
    ],
    "recuperar_clientes": [
        "¿Hace tiempo no le hacés mantenimiento a tu equipo? {servicio} puede ser justo lo que necesita.",
    ],
}

CTA_POR_OBJETIVO = {
    "generar_consultas": "Escribinos por mensaje y te contamos cómo sigue.",
    "generar_confianza": "Zona Arroyito, Rosario — te esperamos.",
    "reconocimiento": "Seguinos para más contenido como este.",
    "recuperar_clientes": "Escribinos y vemos cómo está tu equipo.",
}


@dataclass
class CopyGenerado:
    texto: str
    cta: str


def generar_copy(servicio_nombre: str, objetivo: str) -> CopyGenerado:
    plantillas = PLANTILLAS_POR_OBJETIVO.get(objetivo, PLANTILLAS_POR_OBJETIVO["reconocimiento"])
    indice = hash(servicio_nombre) % len(plantillas)
    texto = plantillas[indice].format(servicio=servicio_nombre, tagline=TAGLINE)
    cta = CTA_POR_OBJETIVO.get(objetivo, CTA_POR_OBJETIVO["reconocimiento"])
    return CopyGenerado(texto=texto, cta=cta)
