from datetime import datetime, timezone

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


@router.post("/configuracion/cuentas/{cuenta_id}")
def actualizar_cuenta(
    cuenta_id: int,
    request: Request,
    id_externo: str = Form(""),
    access_token: str = Form(""),
    url_base_publica: str = Form(""),
    sesion: Session = Depends(obtener_sesion),
):
    """Guarda las credenciales reales de una cuenta (generadas a mano en developers.facebook.com).
    Se marca 'conectada' solo cuando hay id_externo + token cargados — nunca se publica de verdad
    con una cuenta a medio configurar."""
    if (redireccion := requiere_login(request)):
        return redireccion
    cuenta = sesion.get(CuentaConectada, cuenta_id)
    cuenta.id_externo = id_externo.strip()
    cuenta.access_token = access_token.strip()
    cuenta.url_base_publica = url_base_publica.strip()
    tiene_lo_minimo = bool(cuenta.id_externo and cuenta.access_token)
    cuenta.estado_conexion = "conectada" if tiene_lo_minimo else "simulado"
    if cuenta.access_token:
        cuenta.token_actualizado_en = datetime.now(timezone.utc)
    sesion.commit()

    identidad = sesion.query(IdentidadNegocio).first()
    cuentas = sesion.query(CuentaConectada).all()
    return templates.TemplateResponse("configuracion.html", {"request": request, "identidad": identidad, "cuentas": cuentas, "guardado": True})


@router.post("/configuracion/modo-operacion")
def cambiar_modo_operacion(request: Request, modo: str = Form(...), sesion: Session = Depends(obtener_sesion)):
    """Pasar a modo Real exige al menos una cuenta ya conectada de verdad — evita activarlo
    por error y que el primer click de 'Confirmar y publicar' falle sin explicación."""
    if (redireccion := requiere_login(request)):
        return redireccion
    identidad = sesion.query(IdentidadNegocio).first()
    hay_cuenta_conectada = sesion.query(CuentaConectada).filter(CuentaConectada.estado_conexion == "conectada").count() > 0
    if modo == "real" and not hay_cuenta_conectada:
        cuentas = sesion.query(CuentaConectada).all()
        return templates.TemplateResponse("configuracion.html", {
            "request": request, "identidad": identidad, "cuentas": cuentas, "guardado": False,
            "error_modo": "Conectá al menos una cuenta (Instagram o Facebook) antes de pasar a modo Real.",
        })
    identidad.modo_operacion = modo
    sesion.commit()
    cuentas = sesion.query(CuentaConectada).all()
    return templates.TemplateResponse("configuracion.html", {"request": request, "identidad": identidad, "cuentas": cuentas, "guardado": True})
