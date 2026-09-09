from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import obtener_sesion
from app.models import OportunidadFreelance
from app.ui.plantillas import templates

router = APIRouter()

ESTADOS_ACTIVOS = ["por_postular", "postulada", "en_conversacion"]
ESTADOS_CERRADOS = ["ganada", "rechazada", "descartada"]


@router.get("/")
def pantalla_freelancer(request: Request, sesion: Session = Depends(obtener_sesion)):
    total_activas = sesion.query(OportunidadFreelance).filter(OportunidadFreelance.estado.in_(ESTADOS_ACTIVOS)).count()
    return templates.TemplateResponse("freelancer.html", {"request": request, "total_ofertas_activas": total_activas})


@router.get("/ofertas")
def listado_ofertas(request: Request, estado: str = "", sesion: Session = Depends(obtener_sesion)):
    consulta = sesion.query(OportunidadFreelance)
    if estado:
        consulta = consulta.filter(OportunidadFreelance.estado == estado)
    ofertas = consulta.order_by(OportunidadFreelance.fecha_encontrada.desc()).all()
    return templates.TemplateResponse("freelancer_ofertas.html", {
        "request": request, "ofertas": ofertas, "filtro_estado": estado,
        "estados_activos": ESTADOS_ACTIVOS, "estados_cerrados": ESTADOS_CERRADOS,
    })


@router.get("/ofertas/nueva")
def formulario_nueva_oferta(request: Request):
    return templates.TemplateResponse("freelancer_oferta_formulario.html", {"request": request, "oferta": None})


@router.post("/ofertas/nueva")
def crear_oferta(
    request: Request,
    titulo: str = Form(...),
    cliente_o_empresa: str = Form(""),
    fuente: str = Form("otro"),
    url: str = Form(""),
    tipo: str = Form("proyecto_freelance"),
    notas: str = Form(""),
    sesion: Session = Depends(obtener_sesion),
):
    oferta = OportunidadFreelance(
        titulo=titulo, cliente_o_empresa=cliente_o_empresa, fuente=fuente,
        url=url, tipo=tipo, notas=notas,
    )
    sesion.add(oferta)
    sesion.commit()
    return RedirectResponse(url="/ofertas", status_code=303)


@router.get("/ofertas/{oferta_id}/editar")
def formulario_editar_oferta(oferta_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    oferta = sesion.get(OportunidadFreelance, oferta_id)
    return templates.TemplateResponse("freelancer_oferta_formulario.html", {"request": request, "oferta": oferta})


@router.post("/ofertas/{oferta_id}/editar")
def guardar_edicion_oferta(
    oferta_id: int,
    request: Request,
    titulo: str = Form(...),
    cliente_o_empresa: str = Form(""),
    fuente: str = Form("otro"),
    url: str = Form(""),
    tipo: str = Form("proyecto_freelance"),
    notas: str = Form(""),
    sesion: Session = Depends(obtener_sesion),
):
    oferta = sesion.get(OportunidadFreelance, oferta_id)
    if oferta:
        oferta.titulo = titulo
        oferta.cliente_o_empresa = cliente_o_empresa
        oferta.fuente = fuente
        oferta.url = url
        oferta.tipo = tipo
        oferta.notas = notas
        sesion.commit()
    return RedirectResponse(url="/ofertas", status_code=303)


@router.post("/ofertas/{oferta_id}/estado")
def cambiar_estado_oferta(oferta_id: int, request: Request, estado: str = Form(...), sesion: Session = Depends(obtener_sesion)):
    oferta = sesion.get(OportunidadFreelance, oferta_id)
    if oferta:
        oferta.estado = estado
        if estado == "postulada" and oferta.fecha_postulacion is None:
            oferta.fecha_postulacion = datetime.now(timezone.utc)
        sesion.commit()
    return RedirectResponse(url="/ofertas", status_code=303)


@router.post("/ofertas/{oferta_id}/eliminar")
def eliminar_oferta(oferta_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    oferta = sesion.get(OportunidadFreelance, oferta_id)
    if oferta:
        sesion.delete(oferta)
        sesion.commit()
    return RedirectResponse(url="/ofertas", status_code=303)
