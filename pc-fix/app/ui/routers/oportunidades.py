from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.models import Campania, Decision, Oportunidad
from app.ui.plantillas import contexto_comun, templates

router = APIRouter()


@router.get("/oportunidades")
def pantalla_oportunidades(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    oportunidades = sesion.query(Oportunidad).order_by(Oportunidad.estado, Oportunidad.creado_en.desc()).all()
    return templates.TemplateResponse("oportunidades.html", {"request": request, "oportunidades": oportunidades, **contexto_comun(sesion)})


@router.post("/oportunidades/{oportunidad_id}/crear-campania")
def crear_campania_desde_oportunidad(oportunidad_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    oportunidad = sesion.get(Oportunidad, oportunidad_id)
    if oportunidad and oportunidad.estado == "nueva":
        campania = Campania(
            nombre=oportunidad.titulo,
            objetivo=oportunidad.accion_recomendada,
            fecha_inicio=datetime.now(timezone.utc),
        )
        sesion.add(campania)
        oportunidad.estado = "convertida_en_campania"
        sesion.add(Decision(
            texto=f"Se convirtió la oportunidad '{oportunidad.titulo}' en campaña.",
            contexto=oportunidad.explicacion,
        ))
        sesion.commit()
    return RedirectResponse(url="/oportunidades", status_code=303)


@router.post("/oportunidades/{oportunidad_id}/descartar")
def descartar_oportunidad(oportunidad_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    oportunidad = sesion.get(Oportunidad, oportunidad_id)
    if oportunidad and oportunidad.estado == "nueva":
        oportunidad.estado = "descartada"
        sesion.commit()
    return RedirectResponse(url="/oportunidades", status_code=303)
