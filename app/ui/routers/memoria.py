from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.models import Aprendizaje, Decision, IdentidadNegocio, Publicacion, RegistroAccion, Servicio
from app.ui.plantillas import templates

router = APIRouter()


@router.get("/memoria")
def pantalla_memoria(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion

    identidad = sesion.query(IdentidadNegocio).first()
    servicios = sesion.query(Servicio).order_by(Servicio.prioridad, Servicio.nombre).all()
    aprendizajes = sesion.query(Aprendizaje).order_by(Aprendizaje.creado_en.desc()).limit(30).all()
    decisiones = sesion.query(Decision).order_by(Decision.fecha.desc()).limit(20).all()
    registro_acciones = sesion.query(RegistroAccion).order_by(RegistroAccion.fecha.desc()).limit(40).all()
    total_publicaciones = sesion.query(Publicacion).count()

    return templates.TemplateResponse("memoria.html", {
        "request": request,
        "identidad": identidad,
        "servicios": servicios,
        "aprendizajes": aprendizajes,
        "decisiones": decisiones,
        "registro_acciones": registro_acciones,
        "total_publicaciones": total_publicaciones,
    })
