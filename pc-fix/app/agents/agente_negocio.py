"""PCfix Business Agent — orquesta análisis, contenido, oportunidades y aprendizaje
usando herramientas Python con permisos mínimos (sección 18 del pedido).

En esta fase no usa un modelo de LLM (decisión: sin costo de API todavía) —
cada "herramienta" es una función determinística sobre datos reales/simulados
de la base. Toda ejecución queda registrada en `registro_acciones` (sección 19),
y ninguna herramienta publica nada por sí sola (sección 11: siempre
generar → previsualizar → aprobar → publicar).
"""

import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Flyer, IdentidadNegocio, Publicacion, RegistroAccion, Servicio
from app.services import analitica
from app.services.aprendizajes import generar_aprendizajes
from app.services.generador_copy import generar_copy
from app.services.generador_flyer import generar_flyer
from app.services.oportunidades import detectar_oportunidades


class AgentePCfix:
    def __init__(self, sesion: Session):
        self.sesion = sesion

    def _registrar(self, herramienta: str, datos_utilizados: str, resultado: str, requirio_aprobacion: bool = False) -> None:
        self.sesion.add(RegistroAccion(
            herramienta=herramienta,
            datos_utilizados=datos_utilizados,
            resultado=resultado,
            requirio_aprobacion=requirio_aprobacion,
        ))
        self.sesion.commit()

    def herramienta_analizar_publicaciones(self) -> dict:
        analizadas = analitica.obtener_publicaciones_analizadas(self.sesion)
        resultado = {
            "resumen": analitica.resumen_general(analizadas),
            "mejores": analitica.mejores_publicaciones(analizadas, n=3),
            "peores": analitica.peores_publicaciones(analizadas, n=3),
            "por_formato": analitica.rendimiento_por_formato(analizadas),
            "por_pilar": analitica.rendimiento_por_pilar(analizadas),
            "por_plataforma": analitica.rendimiento_por_plataforma(analizadas),
            "por_horario": analitica.rendimiento_por_horario(analizadas),
            "mejor_horario": analitica.mejor_horario(analizadas),
        }
        self._registrar(
            "herramienta_analizar_publicaciones",
            f"{len(analizadas)} publicaciones con métricas",
            f"resumen={resultado['resumen']}",
        )
        return {"analizadas": analizadas, **resultado}

    def herramienta_detectar_oportunidades(self, analizadas) -> list:
        oportunidades = detectar_oportunidades(self.sesion, analizadas)
        self._registrar(
            "herramienta_detectar_oportunidades",
            f"{len(analizadas)} publicaciones analizadas",
            f"{len(oportunidades)} oportunidades detectadas",
        )
        return oportunidades

    def herramienta_generar_aprendizajes(self, analizadas) -> list:
        aprendizajes = generar_aprendizajes(self.sesion, analizadas)
        self._registrar(
            "herramienta_generar_aprendizajes",
            f"{len(analizadas)} publicaciones analizadas",
            f"{len(aprendizajes)} aprendizajes generados",
        )
        return aprendizajes

    def ejecutar_automatizacion_integral(self) -> dict:
        """Corre el botón 🤖 AUTOMATIZAR: analiza, detecta oportunidades y genera aprendizajes."""
        analisis = self.herramienta_analizar_publicaciones()
        oportunidades = self.herramienta_detectar_oportunidades(analisis["analizadas"])
        aprendizajes = self.herramienta_generar_aprendizajes(analisis["analizadas"])
        return {"analisis": analisis, "oportunidades": oportunidades, "aprendizajes": aprendizajes}

    def herramienta_proponer_publicacion(self) -> dict:
        analizadas = analitica.obtener_publicaciones_analizadas(self.sesion)
        por_pilar = analitica.rendimiento_por_pilar(analizadas) if analizadas else {}
        por_formato = analitica.rendimiento_por_formato(analizadas) if analizadas else {}
        mejor_horario = analitica.mejor_horario(analizadas) if analizadas else None

        pilar_recomendado = next(iter(por_pilar), "criterio_tecnico")
        formato_recomendado = next(iter(por_formato), "carrusel")

        servicio_candidato = self._elegir_servicio_a_promocionar()

        propuesta = {
            "servicio": servicio_candidato,
            "pilar": pilar_recomendado,
            "objetivo": "generar_consultas",
            "formato": formato_recomendado,
            "horario_recomendado": mejor_horario or "20:00",
            "justificacion": (
                f"Pilar '{pilar_recomendado}' y formato '{formato_recomendado}' vienen rindiendo mejor en el "
                f"historial disponible." if analizadas else
                "Todavía no hay historial de publicaciones — se propone un punto de partida razonable, no una conclusión de datos."
            ),
        }
        self._registrar(
            "herramienta_proponer_publicacion",
            f"{len(analizadas)} publicaciones analizadas",
            json.dumps({"pilar": pilar_recomendado, "formato": formato_recomendado}, ensure_ascii=False),
        )
        return propuesta

    def herramienta_generar_copy(self, servicio_nombre: str, objetivo: str, plataforma: str = "instagram", pilar: str = ""):
        copy = generar_copy(servicio_nombre, objetivo, plataforma=plataforma, pilar=pilar)
        self._registrar(
            "herramienta_generar_copy",
            f"servicio={servicio_nombre}, objetivo={objetivo}, plataforma={plataforma}",
            copy.texto,
        )
        return copy

    def _elegir_servicio_a_promocionar(self) -> Servicio | None:
        """Prioriza servicios de prioridad alta que todavía no tuvieron ninguna publicación;
        si todos ya tuvieron alguna, elige el que hace más tiempo no se promociona."""
        servicios_verdes = (
            self.sesion.query(Servicio)
            .filter(Servicio.prioridad == "verde", Servicio.activo.is_(True))
            .order_by(Servicio.id)
            .all()
        )
        if not servicios_verdes:
            return None

        ultima_fecha_por_servicio: dict[int, datetime] = {}
        for pub in self.sesion.query(Publicacion).filter(Publicacion.servicio_id.isnot(None)).all():
            actual = ultima_fecha_por_servicio.get(pub.servicio_id)
            if actual is None or pub.fecha > actual:
                ultima_fecha_por_servicio[pub.servicio_id] = pub.fecha

        nunca_promocionados = [s for s in servicios_verdes if s.id not in ultima_fecha_por_servicio]
        if nunca_promocionados:
            return nunca_promocionados[0]

        return min(servicios_verdes, key=lambda s: ultima_fecha_por_servicio[s.id])

    def generar_publicacion_automatica(self) -> list[Publicacion]:
        """Botón único: analiza, decide qué publicar, arma el copy y el flyer para
        Instagram y Facebook (mismo contenido, adaptado por red — ver generador_copy)
        y deja las dos publicaciones listas en 'previsualizado'. Instagram queda con
        su kit de copiar/descargar para publicar a mano (decisión de Berenice de no
        conectar esa red por API); Facebook queda a un solo click de salir de verdad."""
        propuesta = self.herramienta_proponer_publicacion()
        servicio = propuesta["servicio"]
        if servicio is None:
            raise ValueError("No hay servicios activos en el catálogo para proponer una publicación.")

        identidad = self.sesion.query(IdentidadNegocio).first()
        publicaciones: list[Publicacion] = []
        ruta_flyer: str | None = None

        for plataforma in ("instagram", "facebook"):
            copy = self.herramienta_generar_copy(servicio.nombre, propuesta["objetivo"], plataforma=plataforma, pilar=propuesta["pilar"])

            publicacion = Publicacion(
                plataforma=plataforma,
                fecha=datetime.now(),
                formato=propuesta["formato"],
                pilar=propuesta["pilar"],
                objetivo=propuesta["objetivo"],
                tema=f"{servicio.nombre} — {propuesta['objetivo'].replace('_', ' ')}",
                texto=copy.texto,
                cta=copy.cta,
                hashtags=copy.hashtags,
                estado="previsualizado",
                origen_datos="simulado",
                servicio_id=servicio.id,
            )
            self.sesion.add(publicacion)
            self.sesion.commit()
            self.sesion.refresh(publicacion)

            if ruta_flyer is None:
                ruta_flyer = generar_flyer(
                    titular=servicio.nombre,
                    subtitulo=copy.texto,
                    cta=copy.cta,
                    nombre_comercial=identidad.nombre_comercial,
                    tagline=identidad.tagline,
                    color_primario=identidad.color_primario,
                    color_acento=identidad.color_acento,
                )
            self.sesion.add(Flyer(
                publicacion_id=publicacion.id, titular=publicacion.tema, subtitulo=copy.texto,
                cta=copy.cta, archivo_generado=ruta_flyer,
            ))
            self._registrar("herramienta_generar_flyer", f"publicacion_id={publicacion.id}", ruta_flyer)
            publicaciones.append(publicacion)

        return publicaciones
