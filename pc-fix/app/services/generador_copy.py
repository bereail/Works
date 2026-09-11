"""Generador de copy por plantillas (Fase 1: sin IA generativa, por decisión
de no sumar costo de API todavía — ver plan de arquitectura).

Cada plantilla está atada a un objetivo comercial y usa el tagline real de
marca ("Se entiende lo que te arreglan.", 01-Marca/FASE-3-POSICIONAMIENTO.md).

El texto base es el mismo para Instagram y Facebook (mismo contenido, cross-post
— ver 05-Redes/PLAN-DE-CONTENIDOS.md), pero el CTA y los hashtags se adaptan por
plataforma: Facebook tiene un público más adulto y con más peso de dueños de
comercio (Fase 2), así que su CTA apunta a "la página" en tono más formal; los
hashtags solo se generan para Instagram porque ahí sí ayudan al alcance —
en Facebook la práctica no aporta y solo ensucia el texto.
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

CTA_POR_OBJETIVO_INSTAGRAM = {
    "generar_consultas": "Escribinos por mensaje y te contamos cómo sigue.",
    "generar_confianza": "Zona Arroyito, Rosario — te esperamos.",
    "reconocimiento": "Seguinos para más contenido como este.",
    "recuperar_clientes": "Escribinos y vemos cómo está tu equipo.",
}

CTA_POR_OBJETIVO_FACEBOOK = {
    "generar_consultas": "Envianos un mensaje a la página y coordinamos el diagnóstico.",
    "generar_confianza": "Zona Arroyito, Rosario — consultanos por tu equipo o el de tu negocio.",
    "reconocimiento": "Seguí la página para más contenido como este.",
    "recuperar_clientes": "Escribinos a la página y vemos cómo está tu equipo.",
}

CTA_POR_PLATAFORMA = {
    "instagram": CTA_POR_OBJETIVO_INSTAGRAM,
    "facebook": CTA_POR_OBJETIVO_FACEBOOK,
}

HASHTAGS_BASE = ["#Rosario", "#RosarioArgentina", "#ServicioTecnico", "#ReparacionDePC"]

HASHTAGS_POR_PILAR = {
    "criterio_tecnico": ["#TipsDeCompu", "#SoporteTecnico", "#Notebook", "#Tecnologia"],
    "transparencia": ["#PresupuestoSinCargo", "#ServicioTecnicoRosario", "#Confianza"],
    "confianza": ["#ClientesConformes", "#GarantiaDeTrabajo", "#ServicioTecnicoRosario"],
    "tecnologia": ["#Automatizacion", "#PyMEs", "#TecnologiaRosario", "#InnovacionRosario"],
}


@dataclass
class CopyGenerado:
    texto: str
    cta: str
    hashtags: str = ""


def generar_hashtags(pilar: str) -> str:
    """Set curado de 8-9 hashtags (nunca genéricos de más — mejor pocos relevantes
    que treinta que no aportan alcance real)."""
    especificos = HASHTAGS_POR_PILAR.get(pilar, [])
    return " ".join(HASHTAGS_BASE + especificos)


def generar_copy(servicio_nombre: str, objetivo: str, plataforma: str = "instagram", pilar: str = "") -> CopyGenerado:
    plantillas = PLANTILLAS_POR_OBJETIVO.get(objetivo, PLANTILLAS_POR_OBJETIVO["reconocimiento"])
    indice = hash(servicio_nombre) % len(plantillas)
    texto = plantillas[indice].format(servicio=servicio_nombre, tagline=TAGLINE)

    tabla_cta = CTA_POR_PLATAFORMA.get(plataforma, CTA_POR_OBJETIVO_INSTAGRAM)
    cta = tabla_cta.get(objetivo, tabla_cta["reconocimiento"])

    hashtags = generar_hashtags(pilar) if plataforma == "instagram" else ""

    return CopyGenerado(texto=texto, cta=cta, hashtags=hashtags)
