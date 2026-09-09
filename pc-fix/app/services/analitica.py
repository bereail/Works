"""Cálculos de rendimiento sobre publicaciones y métricas ya guardadas.

No inventa nada: si no hay publicaciones o métricas, las funciones devuelven
listas/valores vacíos y la UI debe mostrar "No hay datos suficientes para
determinarlo." — nunca un número inventado.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import MetricaPublicacion, Publicacion, SeguidorHistorico, Servicio


@dataclass
class PublicacionAnalizada:
    publicacion: Publicacion
    servicio_nombre: str
    alcance: int
    visualizaciones: int
    interacciones: int
    comentarios: int
    compartidos: int
    guardados: int
    clics: int
    consultas: int

    @property
    def tasa_interaccion(self) -> float:
        return round(self.interacciones / self.alcance, 4) if self.alcance else 0.0


def obtener_publicaciones_analizadas(sesion: Session, desde: datetime | None = None, hasta: datetime | None = None) -> list[PublicacionAnalizada]:
    consulta = sesion.query(Publicacion).join(MetricaPublicacion, isouter=True)
    if desde is not None:
        consulta = consulta.filter(Publicacion.fecha >= desde)
    if hasta is not None:
        consulta = consulta.filter(Publicacion.fecha <= hasta)
    publicaciones = consulta.order_by(Publicacion.fecha.desc()).all()

    analizadas = []
    for publicacion in publicaciones:
        if not publicacion.metricas:
            continue
        metrica_mas_reciente = publicacion.metricas[-1]
        analizadas.append(PublicacionAnalizada(
            publicacion=publicacion,
            servicio_nombre=publicacion.servicio.nombre if publicacion.servicio else "Sin servicio asociado",
            alcance=metrica_mas_reciente.alcance,
            visualizaciones=metrica_mas_reciente.visualizaciones,
            interacciones=metrica_mas_reciente.interacciones,
            comentarios=metrica_mas_reciente.comentarios,
            compartidos=metrica_mas_reciente.compartidos,
            guardados=metrica_mas_reciente.guardados,
            clics=metrica_mas_reciente.clics,
            consultas=metrica_mas_reciente.consultas,
        ))
    return analizadas


def mejores_publicaciones(analizadas: list[PublicacionAnalizada], n: int = 5) -> list[PublicacionAnalizada]:
    return sorted(analizadas, key=lambda p: p.tasa_interaccion, reverse=True)[:n]


def peores_publicaciones(analizadas: list[PublicacionAnalizada], n: int = 5) -> list[PublicacionAnalizada]:
    return sorted(analizadas, key=lambda p: p.tasa_interaccion)[:n]


def _agrupar_por(analizadas: list[PublicacionAnalizada], clave) -> dict[str, dict]:
    grupos: dict[str, list[PublicacionAnalizada]] = defaultdict(list)
    for p in analizadas:
        grupos[clave(p)].append(p)

    resultado = {}
    for nombre_grupo, items in grupos.items():
        promedio_tasa = sum(p.tasa_interaccion for p in items) / len(items)
        resultado[nombre_grupo] = {
            "cantidad_publicaciones": len(items),
            "alcance_total": sum(p.alcance for p in items),
            "interacciones_total": sum(p.interacciones for p in items),
            "consultas_total": sum(p.consultas for p in items),
            "tasa_interaccion_promedio": round(promedio_tasa, 4),
        }
    return dict(sorted(resultado.items(), key=lambda kv: kv[1]["tasa_interaccion_promedio"], reverse=True))


def rendimiento_por_formato(analizadas: list[PublicacionAnalizada]) -> dict:
    return _agrupar_por(analizadas, lambda p: p.publicacion.formato)


def rendimiento_por_pilar(analizadas: list[PublicacionAnalizada]) -> dict:
    return _agrupar_por(analizadas, lambda p: p.publicacion.pilar or "sin_pilar")


def rendimiento_por_servicio(analizadas: list[PublicacionAnalizada]) -> dict:
    return _agrupar_por(analizadas, lambda p: p.servicio_nombre)


def rendimiento_por_plataforma(analizadas: list[PublicacionAnalizada]) -> dict:
    return _agrupar_por(analizadas, lambda p: p.publicacion.plataforma)


def rendimiento_por_horario(analizadas: list[PublicacionAnalizada]) -> dict:
    return _agrupar_por(analizadas, lambda p: f"{p.publicacion.fecha.hour:02d}:00")


def rendimiento_por_dia_semana(analizadas: list[PublicacionAnalizada]) -> dict:
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return _agrupar_por(analizadas, lambda p: dias[p.publicacion.fecha.weekday()])


def mejor_horario(analizadas: list[PublicacionAnalizada]) -> str | None:
    por_horario = rendimiento_por_horario(analizadas)
    if not por_horario:
        return None
    return max(por_horario.items(), key=lambda kv: kv[1]["tasa_interaccion_promedio"])[0]


def crecimiento_seguidores(sesion: Session) -> dict[str, dict]:
    registros = sesion.query(SeguidorHistorico).order_by(SeguidorHistorico.fecha).all()
    por_plataforma: dict[str, list[SeguidorHistorico]] = defaultdict(list)
    for r in registros:
        por_plataforma[r.plataforma].append(r)

    resultado = {}
    for plataforma, items in por_plataforma.items():
        if len(items) < 2:
            resultado[plataforma] = {"actual": items[-1].cantidad if items else 0, "crecimiento_absoluto": 0, "crecimiento_pct": 0.0}
            continue
        primero, ultimo = items[0].cantidad, items[-1].cantidad
        crecimiento_pct = round((ultimo - primero) / primero * 100, 1) if primero else 0.0
        resultado[plataforma] = {
            "actual": ultimo,
            "crecimiento_absoluto": ultimo - primero,
            "crecimiento_pct": crecimiento_pct,
            "serie": [{"fecha": r.fecha.isoformat(), "cantidad": r.cantidad} for r in items],
        }
    return resultado


def resumen_general(analizadas: list[PublicacionAnalizada]) -> dict:
    if not analizadas:
        return {
            "hay_datos": False,
            "mensaje": "No hay datos suficientes para determinarlo.",
        }
    return {
        "hay_datos": True,
        "alcance_total": sum(p.alcance for p in analizadas),
        "visualizaciones_total": sum(p.visualizaciones for p in analizadas),
        "interacciones_total": sum(p.interacciones for p in analizadas),
        "consultas_total": sum(p.consultas for p in analizadas),
        "cantidad_publicaciones": len(analizadas),
        "tasa_interaccion_promedio": round(sum(p.tasa_interaccion for p in analizadas) / len(analizadas), 4),
    }
