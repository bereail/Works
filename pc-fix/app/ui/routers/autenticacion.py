from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth.seguridad import verificar_password
from app.database import obtener_sesion
from app.models import Usuario
from app.ui.plantillas import templates

router = APIRouter()


@router.get("/login")
def formulario_login(request: Request):
    if request.session.get("usuario_id"):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
def procesar_login(request: Request, email: str = Form(...), password: str = Form(...), sesion: Session = Depends(obtener_sesion)):
    usuario = sesion.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verificar_password(password, usuario.hash_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email o contraseña incorrectos."}, status_code=401)
    request.session["usuario_id"] = usuario.id
    request.session["usuario_nombre"] = usuario.nombre
    return RedirectResponse(url="/", status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
