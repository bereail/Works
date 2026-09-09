from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.models import CuentaConectada, IdentidadNegocio
from app.ui.plantillas import templates

router = APIRouter()


@router.get("/configuracion")
def pantalla_configuracion(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    identidad = sesion.query(IdentidadNegocio).first()
    cuentas = sesion.query(CuentaConectada).all()
    return templates.TemplateResponse("configuracion.html", {"request": request, "identidad": identidad, "cuentas": cuentas, "guardado": False})


@router.post("/configuracion")
def actualizar_configuracion(
    request: Request,
    tagline: str = Form(...),
    color_primario: str = Form(...),
    color_acento: str = Form(...),
    sesion: Session = Depends(obtener_sesion),
):
    if (redireccion := requiere_login(request)):
        return redireccion
    identidad = sesion.query(IdentidadNegocio).first()
    identidad.tagline = tagline
    identidad.color_primario = color_primario
    identidad.color_acento = color_acento
    sesion.commit()
    cuentas = sesion.query(CuentaConectada).all()
    return templates.TemplateResponse("configuracion.html", {"request": request, "identidad": identidad, "cuentas": cuentas, "guardado": True})
