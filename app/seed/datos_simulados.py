"""Siembra la base con la identidad real de PCfix, el catálogo real de servicios
y un historial de publicaciones SIMULADO (basado en el calendario real de
05-Redes/PLAN-DE-CONTENIDOS.md) para que el dashboard tenga algo que mostrar
antes de conectar Instagram/Facebook de verdad.

Todo lo que es simulado queda marcado con origen_datos="simulado" — nunca se
mezcla con datos reales.
"""

import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.auth.seguridad import hashear_password
from app.models import (
    CuentaConectada,
    IdentidadNegocio,
    MetricaPublicacion,
    Publicacion,
    SeguidorHistorico,
    Servicio,
    Usuario,
)

USUARIO_INICIAL_EMAIL = "berenice@pcfix.local"
USUARIO_INICIAL_PASSWORD = "pcfix2026"

random.seed(7)

SERVICIOS = [
    ("Reparación de PC / notebook", "reparacion", "verde"),
    ("Instalación de Windows / drivers", "mantenimiento", "verde"),
    ("Limpieza de virus / optimización", "mantenimiento", "verde"),
    ("Migración a SSD", "actualizacion", "verde"),
    ("Instalación de RAM", "actualizacion", "verde"),
    ("Limpieza física", "mantenimiento", "verde"),
    ("Cambio de discos", "reparacion", "verde"),
    ("Configuración de equipos", "mantenimiento", "verde"),
    ("Recuperación básica de información", "reparacion", "verde"),
    ("Copias de seguridad", "mantenimiento", "verde"),
    ("Soporte remoto", "soporte", "verde"),
    ("Venta de SSD / RAM / accesorios", "venta", "verde"),
    ("Soporte por abono mensual (particulares)", "recurrente", "verde"),
    ("Mantenimiento preventivo programado", "recurrente", "verde"),
    ("Instalación de redes / WiFi / routers", "instalacion", "amarillo"),
    ("Armado de PC gamer", "armado", "amarillo"),
    ("Mantenimiento y soporte para empresas (abono)", "pyme", "amarillo"),
    ("Automatizaciones para negocios", "pyme", "amarillo"),
    ("Inteligencia artificial para PyMEs", "pyme", "amarillo"),
    ("Backups automáticos (empresas)", "pyme", "amarillo"),
    ("NAS / servidores domésticos", "pyme", "amarillo"),
    ("Desarrollo web", "pyme", "amarillo"),
    ("Cámaras IP", "evaluar", "rojo"),
    ("Actualización de equipos (upgrade consultivo)", "evaluar", "rojo"),
    ("Impresoras", "evaluar", "rojo"),
]

# (offset_dias desde el 10-ago-2026, hora, plataforma, formato, pilar, tema, servicio, texto, cta)
INICIO_CALENDARIO = datetime(2026, 8, 10, 0, 0)

PUBLICACIONES_SEMILLA = [
    dict(
        dias=0, hora=20, plataforma="instagram", formato="carrusel", pilar="transparencia",
        tema="Así armamos un presupuesto: sin letra chica", servicio="Reparación de PC / notebook",
        objetivo="generar_confianza",
        texto="Mano de obra separada de insumos, todo por escrito, sin sorpresas al retirar el equipo.",
        cta="Escribinos por mensaje y te contamos cómo armamos el tuyo.",
    ),
    dict(
        dias=1, hora=20, plataforma="facebook", formato="carrusel", pilar="transparencia",
        tema="Así armamos un presupuesto: sin letra chica (repost)", servicio="Reparación de PC / notebook",
        objetivo="generar_confianza",
        texto="Mano de obra separada de insumos, todo por escrito, sin sorpresas al retirar el equipo.",
        cta="Escribinos por mensaje y te contamos cómo armamos el tuyo.",
    ),
    dict(
        dias=7, hora=20, plataforma="instagram", formato="carrusel", pilar="confianza",
        tema="Proceso recepción → diagnóstico → entrega", servicio="Reparación de PC / notebook",
        objetivo="reconocimiento",
        texto="Te mostramos paso a paso qué pasa con tu equipo desde que lo dejás hasta que lo retirás.",
        cta="Zona Rosario — te esperamos.",
    ),
    dict(
        dias=14, hora=20, plataforma="instagram", formato="reel", pilar="criterio_tecnico",
        tema="3 señales de que tu PC necesita SSD, no una PC nueva", servicio="Migración a SSD",
        objetivo="generar_consultas",
        texto="Antes de gastar en una compu nueva, mirá si tu problema tiene una solución mucho más barata.",
        cta="Consultanos si tu equipo es candidato a SSD.",
    ),
    dict(
        dias=15, hora=10, plataforma="facebook", formato="reel", pilar="criterio_tecnico",
        tema="3 señales de que tu PC necesita SSD, no una PC nueva (repost)", servicio="Migración a SSD",
        objetivo="generar_consultas",
        texto="Antes de gastar en una compu nueva, mirá si tu problema tiene una solución mucho más barata.",
        cta="Consultanos si tu equipo es candidato a SSD.",
    ),
    dict(
        dias=21, hora=14, plataforma="instagram", formato="post estático", pilar="transparencia",
        tema="Precio de referencia de 3 servicios de entrada", servicio="Limpieza de virus / optimización",
        objetivo="generar_consultas",
        texto="Limpieza, migración a SSD y formateo: precios de referencia claros, antes de que preguntes.",
        cta="Precios exactos según equipo — escribinos.",
    ),
    dict(
        dias=28, hora=20, plataforma="instagram", formato="reel", pilar="criterio_tecnico",
        tema="Mito: formatear arregla todo", servicio="Limpieza de virus / optimización",
        objetivo="reconocimiento",
        texto="Cuándo sí conviene formatear y cuándo es matar una mosca a cañonazos.",
        cta="Si no estás seguro, primero preguntanos.",
    ),
    dict(
        dias=35, hora=20, plataforma="instagram", formato="carrusel", pilar="tecnologia",
        tema="Automatización/IA para PyMEs, ejemplo simple", servicio="Automatizaciones para negocios",
        objetivo="reconocimiento",
        texto="Un ejemplo real y simple de cómo una PyME de Rosario puede ahorrar tiempo con automatización.",
        cta="Si tenés un comercio y esto te interesa, escribinos.",
    ),
    dict(
        dias=42, hora=20, plataforma="instagram", formato="reel", pilar="tecnologia",
        tema="Le mandás un WhatsApp a las 2 AM y te contesta igual", servicio="Soporte remoto",
        objetivo="reconocimiento",
        texto="Mostramos cómo el triage automático de WhatsApp responde incluso fuera de horario.",
        cta="Probalo vos mismo — mandanos un mensaje.",
    ),
    dict(
        dias=2, hora=14, plataforma="facebook", formato="post estático", pilar="confianza",
        tema="Garantía explicada en criollo", servicio="Reparación de PC / notebook",
        objetivo="generar_confianza",
        texto="Toda reparación sale con garantía por escrito. Te contamos qué cubre y por cuánto tiempo.",
        cta="Dudas sobre tu garantía, escribinos.",
    ),
    dict(
        dias=9, hora=10, plataforma="instagram", formato="historia", pilar="confianza",
        tema="Detrás de escena de un diagnóstico", servicio="Reparación de PC / notebook",
        objetivo="reconocimiento",
        texto="Un vistazo rápido a cómo se ve un diagnóstico en el banco de trabajo.",
        cta="",
    ),
    dict(
        dias=16, hora=10, plataforma="instagram", formato="historia", pilar="tecnologia",
        tema="Encuesta: ¿tu PC tarda más en prender que en apagarse?", servicio="Migración a SSD",
        objetivo="reconocimiento",
        texto="Encuesta rápida para la audiencia sobre lentitud de arranque.",
        cta="",
    ),
    dict(
        dias=23, hora=14, plataforma="instagram", formato="post estático", pilar="criterio_tecnico",
        tema="Ram vs SSD: qué conviene actualizar primero", servicio="Instalación de RAM",
        objetivo="generar_consultas",
        texto="Dos upgrades comunes, resultados muy distintos según el cuello de botella real de tu equipo.",
        cta="Te decimos cuál te conviene a vos.",
    ),
    dict(
        dias=30, hora=20, plataforma="instagram", formato="reel", pilar="criterio_tecnico",
        tema="Notebook lenta no siempre es un virus", servicio="Limpieza de virus / optimización",
        objetivo="generar_consultas",
        texto="Los 4 motivos más comunes de lentitud, y cómo distinguirlos antes de gastar de más.",
        cta="Traela y la revisamos sin cargo el diagnóstico inicial.",
    ),
    dict(
        dias=37, hora=10, plataforma="facebook", formato="post estático", pilar="transparencia",
        tema="Plan de mantenimiento para comercios", servicio="Mantenimiento y soporte para empresas (abono)",
        objetivo="generar_consultas",
        texto="Un abono mensual fijo en vez de un susto grande una vez al año.",
        cta="Si tenés un comercio, escribinos por el plan.",
    ),
    dict(
        dias=44, hora=20, plataforma="instagram", formato="carrusel", pilar="confianza",
        tema="Primer testimonio real", servicio="Reparación de PC / notebook",
        objetivo="reconocimiento",
        texto="Un cliente real nos cuenta cómo fue el proceso, de punta a punta.",
        cta="",
    ),
]


def _generar_metricas(pilar: str, formato: str, hora: int, plataforma: str) -> dict:
    """Genera métricas simuladas con sesgos deliberados y reproducibles (seed fija)
    para que el motor de análisis tenga patrones reales que detectar:
    reels de criterio técnico / tecnología rinden mejor, y el horario 20hs supera al 10-14hs.
    """
    base_alcance = 600 if plataforma == "instagram" else 350
    factor_formato = {"reel": 1.9, "carrusel": 1.3, "post estático": 0.9, "historia": 0.5}.get(formato, 1.0)
    factor_pilar = {"criterio_tecnico": 1.4, "tecnologia": 1.35, "confianza": 1.05, "transparencia": 0.95}.get(pilar, 1.0)
    factor_horario = 1.25 if hora == 20 else (1.0 if hora == 14 else 0.8)

    factor = factor_formato * factor_pilar * factor_horario
    ruido = random.uniform(0.85, 1.15)

    alcance = int(base_alcance * factor * ruido)
    visualizaciones = int(alcance * random.uniform(1.1, 1.6)) if formato in ("reel", "historia") else int(alcance * random.uniform(0.3, 0.6))
    interacciones = int(alcance * random.uniform(0.04, 0.12) * factor_pilar)
    comentarios = max(0, int(interacciones * random.uniform(0.05, 0.15)))
    compartidos = max(0, int(interacciones * random.uniform(0.05, 0.2)))
    guardados = max(0, int(interacciones * random.uniform(0.1, 0.3)))
    clics = max(0, int(alcance * random.uniform(0.01, 0.04)))
    consultas = max(0, int(clics * random.uniform(0.1, 0.35)))

    return dict(
        alcance=alcance, visualizaciones=visualizaciones, interacciones=interacciones,
        comentarios=comentarios, compartidos=compartidos, guardados=guardados,
        clics=clics, consultas=consultas,
    )


def sembrar(sesion: Session) -> None:
    """Idempotente: si ya hay identidad de negocio cargada, no vuelve a sembrar."""
    if sesion.query(IdentidadNegocio).first() is not None:
        return

    identidad = IdentidadNegocio(
        nombre_comercial="PCfix Informática",
        actividad="Reparación y mantenimiento de computadoras y notebooks",
        zona="Arroyito, Rosario, Santa Fe",
        tagline="Se entiende lo que te arreglan.",
        modo_operacion="simulacion",
        identidad_visual_definitiva=False,
    )
    sesion.add(identidad)

    sesion.add(CuentaConectada(plataforma="instagram", nombre_cuenta="pcfix.informatica", tipo="comercial", estado_conexion="simulado"))
    sesion.add(CuentaConectada(plataforma="facebook", nombre_cuenta="PC Fix", tipo="comercial", estado_conexion="simulado"))

    sesion.add(Usuario(
        nombre="Berenice",
        email=USUARIO_INICIAL_EMAIL,
        hash_password=hashear_password(USUARIO_INICIAL_PASSWORD),
    ))

    servicios_por_nombre: dict[str, Servicio] = {}
    for nombre, categoria, prioridad in SERVICIOS:
        servicio = Servicio(nombre=nombre, categoria=categoria, prioridad=prioridad)
        sesion.add(servicio)
        servicios_por_nombre[nombre] = servicio
    sesion.flush()  # asigna IDs antes de referenciarlos en publicaciones

    for semilla in PUBLICACIONES_SEMILLA:
        fecha = INICIO_CALENDARIO + timedelta(days=semilla["dias"], hours=semilla["hora"])
        publicacion = Publicacion(
            plataforma=semilla["plataforma"],
            fecha=fecha,
            formato=semilla["formato"],
            tema=semilla["tema"],
            pilar=semilla["pilar"],
            objetivo=semilla["objetivo"],
            texto=semilla["texto"],
            cta=semilla["cta"],
            estado="publicado",
            origen_datos="simulado",
            servicio_id=servicios_por_nombre[semilla["servicio"]].id,
        )
        sesion.add(publicacion)
        sesion.flush()

        metricas = _generar_metricas(semilla["pilar"], semilla["formato"], semilla["hora"], semilla["plataforma"])
        sesion.add(MetricaPublicacion(
            publicacion_id=publicacion.id,
            fecha_medicion=fecha + timedelta(days=3),
            origen_datos="simulado",
            **metricas,
        ))

    seguidores_ig = 480
    seguidores_fb = 310
    for semana in range(7):
        fecha = INICIO_CALENDARIO + timedelta(weeks=semana)
        seguidores_ig += random.randint(3, 14)
        seguidores_fb += random.randint(1, 6)
        sesion.add(SeguidorHistorico(plataforma="instagram", fecha=fecha, cantidad=seguidores_ig, origen_datos="simulado"))
        sesion.add(SeguidorHistorico(plataforma="facebook", fecha=fecha, cantidad=seguidores_fb, origen_datos="simulado"))

    sesion.commit()
