from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.services import analitica
from app.ui.plantillas import contexto_comun, templates

router = APIRouter()

PERIODOS = {"7": 7, "30": 30, "90": 90, "todo": None}


@router.get("/analiticas")
def pantalla_analiticas(request: Request, periodo: str = "30", sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion

    dias = PERIODOS.get(periodo, 30)
    desde = datetime.now(timezone.utc) - timedelta(days=dias) if dias else None

    analizadas = analitica.obtener_publicaciones_analizadas(sesion, desde=desde)

    return templates.TemplateResponse("analiticas.html", {
        "request": request,
        "periodo_actual": periodo,
        "resumen": analitica.resumen_general(analizadas),
        "por_plataforma": analitica.rendimiento_por_plataforma(analizadas),
        "por_servicio": analitica.rendimiento_por_servicio(analizadas),
        "por_formato": analitica.rendimiento_por_formato(analizadas),
        "por_pilar": analitica.rendimiento_por_pilar(analizadas),
        "por_dia_semana": analitica.rendimiento_por_dia_semana(analizadas),
        "por_horario": analitica.rendimiento_por_horario(analizadas),
        **contexto_comun(sesion),
    })
