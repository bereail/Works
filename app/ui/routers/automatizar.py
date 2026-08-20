from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.agents.agente_negocio import AgentePCfix
from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.ui.plantillas import contexto_comun, templates

router = APIRouter()


@router.get("/automatizar")
def pantalla_automatizar(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    return templates.TemplateResponse("automatizar.html", {"request": request, "resultado": None, **contexto_comun(sesion)})


@router.post("/automatizar/ejecutar")
def ejecutar_automatizacion(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    agente = AgentePCfix(sesion)
    resultado = agente.ejecutar_automatizacion_integral()
    return templates.TemplateResponse("_automatizar_resultado.html", {"request": request, "resultado": resultado})
