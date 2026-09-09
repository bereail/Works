from datetime import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.models import CuentaConectada, IdentidadNegocio, Oportunidad, Publicacion
from app.services import analitica
from app.ui.plantillas import templates

router = APIRouter()


@router.get("/")
def dashboard(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion

    identidad = sesion.query(IdentidadNegocio).first()
    cuentas = sesion.query(CuentaConectada).all()

    analizadas = analitica.obtener_publicaciones_analizadas(sesion)
    resumen = analitica.resumen_general(analizadas)
    mejores = analitica.mejores_publicaciones(analizadas, n=3)
    peores = analitica.peores_publicaciones(analizadas, n=3)
    por_servicio = analitica.rendimiento_por_servicio(analizadas)
    mejor_horario = analitica.mejor_horario(analizadas)
    crecimiento = analitica.crecimiento_seguidores(sesion)
    oportunidades_recientes = sesion.query(Oportunidad).filter(Oportunidad.estado == "nueva").order_by(Oportunidad.creado_en.desc()).limit(4).all()
    publicacion_pendiente = (
        sesion.query(Publicacion)
        .filter(Publicacion.estado.in_(["previsualizado", "aprobado"]))
        .order_by(Publicacion.creado_en.desc())
        .first()
    )

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "identidad": identidad,
        "cuentas": cuentas,
        "resumen": resumen,
        "mejores": mejores,
        "peores": peores,
        "por_servicio": list(por_servicio.items())[:5],
        "mejor_horario": mejor_horario,
        "crecimiento": crecimiento,
        "oportunidades_recientes": oportunidades_recientes,
        "publicacion_pendiente": publicacion_pendiente,
        "ahora": datetime.now(),
    })
