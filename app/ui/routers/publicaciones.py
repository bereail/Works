from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.agents.agente_negocio import AgentePCfix
from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.models import CuentaConectada, Flyer, IdentidadNegocio, Publicacion, RegistroAccion, Servicio
from app.services.generador_flyer import generar_flyer
from app.ui.plantillas import contexto_comun, templates

router = APIRouter(prefix="/publicaciones")


@router.get("")
def redireccion_index(request: Request):
    return RedirectResponse(url="/publicaciones/pendientes", status_code=303)


@router.get("/crear")
def formulario_crear(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    agente = AgentePCfix(sesion)
    propuesta = agente.herramienta_proponer_publicacion()
    servicios = sesion.query(Servicio).filter(Servicio.activo.is_(True)).order_by(Servicio.nombre).all()
    return templates.TemplateResponse("publicaciones_crear.html", {
        "request": request, "propuesta": propuesta, "servicios": servicios, "ahora": datetime.now(), **contexto_comun(sesion),
    })


@router.post("/crear")
def procesar_crear(
    request: Request,
    servicio_id: int = Form(...),
    plataforma: str = Form(...),
    formato: str = Form(...),
    pilar: str = Form(...),
    objetivo: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(...),
    sesion: Session = Depends(obtener_sesion),
):
    if (redireccion := requiere_login(request)):
        return redireccion

    servicio = sesion.get(Servicio, servicio_id)
    agente = AgentePCfix(sesion)
    copy = agente.herramienta_generar_copy(servicio.nombre, objetivo)

    fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    publicacion = Publicacion(
        plataforma=plataforma, fecha=fecha_hora, formato=formato, pilar=pilar, objetivo=objetivo,
        tema=f"{servicio.nombre} — {objetivo.replace('_', ' ')}",
        texto=copy.texto, cta=copy.cta, estado="borrador", origen_datos="simulado",
        servicio_id=servicio.id,
    )
    sesion.add(publicacion)
    sesion.commit()
    return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)


@router.get("/{publicacion_id}/previsualizar")
def previsualizar(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    if publicacion.estado == "borrador":
        publicacion.estado = "previsualizado"
        sesion.commit()
    identidad = sesion.query(IdentidadNegocio).first()
    cuenta = sesion.query(CuentaConectada).filter(CuentaConectada.plataforma == publicacion.plataforma).first()
    return templates.TemplateResponse("publicaciones_previsualizar.html", {
        "request": request, "publicacion": publicacion, "identidad": identidad, "cuenta": cuenta,
    })


@router.post("/{publicacion_id}/generar-flyer")
def generar_flyer_publicacion(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    identidad = sesion.query(IdentidadNegocio).first()

    ruta = generar_flyer(
        titular=publicacion.servicio.nombre if publicacion.servicio else publicacion.tema,
        subtitulo=publicacion.texto,
        cta=publicacion.cta,
        nombre_comercial=identidad.nombre_comercial,
        tagline=identidad.tagline,
        color_primario=identidad.color_primario,
        color_acento=identidad.color_acento,
    )
    flyer = Flyer(
        publicacion_id=publicacion.id, titular=publicacion.tema, subtitulo=publicacion.texto,
        cta=publicacion.cta, archivo_generado=ruta,
    )
    sesion.add(flyer)
    sesion.add(RegistroAccion(herramienta="herramienta_generar_flyer", datos_utilizados=f"publicacion_id={publicacion.id}", resultado=ruta))
    sesion.commit()
    return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)


@router.post("/{publicacion_id}/aprobar")
def aprobar(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    publicacion.estado = "aprobado"
    sesion.add(RegistroAccion(
        herramienta="aprobar_publicacion", datos_utilizados=f"publicacion_id={publicacion.id}",
        resultado="aprobado por Berenice", requirio_aprobacion=True, aprobado=True,
    ))
    sesion.commit()
    return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)


@router.post("/{publicacion_id}/publicar")
def publicar(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    identidad = sesion.query(IdentidadNegocio).first()

    if identidad.modo_operacion != "real":
        publicacion.estado = "simulado"
        resultado = "Publicación simulada: no se envió a ninguna red social real (modo Simulación activo)."
    else:
        # Modo Real: sin integraciones conectadas todavía en esta fase — se bloquea explícitamente.
        resultado = "Bloqueado: no hay ninguna cuenta real conectada todavía."

    sesion.add(RegistroAccion(
        herramienta="publicar_publicacion", datos_utilizados=f"publicacion_id={publicacion.id}",
        resultado=resultado, requirio_aprobacion=True, aprobado=True,
    ))
    sesion.commit()
    return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)


@router.get("/flyers")
def listado_flyers(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    flyers = sesion.query(Flyer).order_by(Flyer.creado_en.desc()).all()
    return templates.TemplateResponse("publicaciones_flyers.html", {"request": request, "flyers": flyers, **contexto_comun(sesion)})


@router.get("/calendario")
def calendario(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicaciones = sesion.query(Publicacion).order_by(Publicacion.fecha).all()
    return templates.TemplateResponse("publicaciones_calendario.html", {"request": request, "publicaciones": publicaciones, **contexto_comun(sesion)})


@router.get("/pendientes")
def pendientes(request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicaciones = (
        sesion.query(Publicacion)
        .filter(Publicacion.estado.in_(["borrador", "previsualizado", "aprobado"]))
        .order_by(Publicacion.fecha)
        .all()
    )
    return templates.TemplateResponse("publicaciones_pendientes.html", {"request": request, "publicaciones": publicaciones, **contexto_comun(sesion)})
