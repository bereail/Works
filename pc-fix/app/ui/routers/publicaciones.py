import os
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.agents.agente_negocio import AgentePCfix
from app.auth.dependencias import requiere_login
from app.database import obtener_sesion
from app.models import CuentaConectada, Flyer, IdentidadNegocio, Publicacion, RegistroAccion, Servicio
from app.services.generador_flyer import generar_flyer
from app.services.meta_api import ErrorPublicacionMeta, publicar_en_facebook, publicar_en_instagram
from app.ui.plantillas import contexto_comun, templates

router = APIRouter(prefix="/publicaciones")

ESTADOS_EDITABLES = ("borrador", "previsualizado", "aprobado")
RUTA_STATIC = os.path.join("app", "ui", "static")


def _publicar_de_verdad(sesion: Session, publicacion: Publicacion) -> str:
    """Publica en la red real correspondiente a `publicacion.plataforma`. Nunca publica
    en más de una plataforma en la misma llamada — eso ya lo garantiza el modelo de datos
    (una Publicacion = una plataforma), respetando el orden Instagram → Facebook por separado."""
    cuenta = sesion.query(CuentaConectada).filter(CuentaConectada.plataforma == publicacion.plataforma).first()
    if cuenta is None or cuenta.estado_conexion != "conectada" or not cuenta.access_token or not cuenta.id_externo:
        return (
            f"Bloqueado: la cuenta de {publicacion.plataforma} todavía no está conectada de verdad "
            "(faltan credenciales en Configuración)."
        )

    if not publicacion.flyers:
        return "Bloqueado: esta publicación todavía no tiene un flyer generado."

    ruta_relativa = publicacion.flyers[-1].archivo_generado
    ruta_absoluta = os.path.join(RUTA_STATIC, ruta_relativa)
    if not os.path.isfile(ruta_absoluta):
        return "Bloqueado: no se encontró el archivo del flyer en el servidor."

    try:
        if publicacion.plataforma == "facebook":
            id_externo = publicar_en_facebook(cuenta, f"{publicacion.texto}\n\n{publicacion.cta}".strip(), ruta_absoluta)
        elif publicacion.plataforma == "instagram":
            if not cuenta.url_base_publica:
                return (
                    "Bloqueado: falta configurar la URL pública desde donde Instagram puede "
                    "descargar el flyer (Instagram no acepta subir el archivo directo, solo una URL)."
                )
            url_imagen_publica = f"{cuenta.url_base_publica.rstrip('/')}/{ruta_relativa}"
            id_externo = publicar_en_instagram(cuenta, f"{publicacion.texto}\n\n{publicacion.cta}".strip(), url_imagen_publica)
        else:
            return f"Bloqueado: plataforma '{publicacion.plataforma}' no soportada todavía."
    except ErrorPublicacionMeta as error:
        publicacion.estado = "error"
        return f"Error al publicar en {publicacion.plataforma}: {error}"

    publicacion.estado = "publicado"
    publicacion.id_publicacion_externa = id_externo
    return f"Publicado de verdad en {publicacion.plataforma} — id {id_externo}."


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
    copy = agente.herramienta_generar_copy(servicio.nombre, objetivo, plataforma=plataforma, pilar=pilar)

    fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    publicacion = Publicacion(
        plataforma=plataforma, fecha=fecha_hora, formato=formato, pilar=pilar, objetivo=objetivo,
        tema=f"{servicio.nombre} — {objetivo.replace('_', ' ')}",
        texto=copy.texto, cta=copy.cta, hashtags=copy.hashtags, estado="borrador", origen_datos="simulado",
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


@router.get("/{publicacion_id}/editar")
def formulario_editar(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    if publicacion.estado not in ESTADOS_EDITABLES:
        return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)
    return templates.TemplateResponse("publicaciones_editar.html", {
        "request": request, "publicacion": publicacion, **contexto_comun(sesion),
    })


@router.post("/{publicacion_id}/editar")
def procesar_editar(
    publicacion_id: int,
    request: Request,
    tema: str = Form(...),
    texto: str = Form(...),
    cta: str = Form(""),
    hashtags: str = Form(""),
    fecha: str = Form(...),
    hora: str = Form(...),
    sesion: Session = Depends(obtener_sesion),
):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    if publicacion.estado not in ESTADOS_EDITABLES:
        return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)

    publicacion.tema = tema
    publicacion.texto = texto
    publicacion.cta = cta
    if publicacion.plataforma == "instagram":
        publicacion.hashtags = hashtags
    publicacion.fecha = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    sesion.add(RegistroAccion(
        herramienta="editar_publicacion", datos_utilizados=f"publicacion_id={publicacion.id}",
        resultado="Texto/tema/fecha editados a mano antes de publicar.",
    ))
    sesion.commit()
    return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)


@router.post("/{publicacion_id}/eliminar")
def eliminar_publicacion(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    if publicacion is None:
        return RedirectResponse(url="/publicaciones/pendientes", status_code=303)
    if publicacion.estado not in ESTADOS_EDITABLES + ("simulado",):
        # Nunca se borra algo que ya salió de verdad a una red — solo se descartan borradores/simulados.
        return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)

    for flyer in list(publicacion.flyers):
        ruta_archivo = os.path.join("app", "ui", "static", flyer.archivo_generado) if flyer.archivo_generado else None
        if ruta_archivo and os.path.isfile(ruta_archivo):
            try:
                os.remove(ruta_archivo)
            except OSError:
                pass
        sesion.delete(flyer)

    sesion.add(RegistroAccion(
        herramienta="eliminar_publicacion", datos_utilizados=f"publicacion_id={publicacion.id}",
        resultado=f"Publicación descartada (estaba en estado '{publicacion.estado}').",
    ))
    sesion.delete(publicacion)
    sesion.commit()
    return RedirectResponse(url="/publicaciones/pendientes", status_code=303)


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


@router.post("/{publicacion_id}/confirmar-y-publicar")
def confirmar_y_publicar(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    """Un solo click aprueba y publica — Berenice ya vio el texto y el flyer en la previsualización
    antes de llegar acá, así que no hace falta un paso de aprobación separado.

    Cada Publicacion es siempre de una sola plataforma (instagram o facebook), así que
    publicar en ambas redes ya son, por diseño, dos clicks separados — nunca uno solo
    que dispare las dos a la vez."""
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    if publicacion.estado not in ("previsualizado", "aprobado", "error"):
        return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)

    identidad = sesion.query(IdentidadNegocio).first()
    if identidad.modo_operacion != "real":
        publicacion.estado = "simulado"
        resultado = "Publicación simulada: no se envió a ninguna red social real (modo Simulación activo)."
    else:
        resultado = _publicar_de_verdad(sesion, publicacion)

    sesion.add(RegistroAccion(
        herramienta="confirmar_y_publicar", datos_utilizados=f"publicacion_id={publicacion.id}",
        resultado=resultado, requirio_aprobacion=True, aprobado=True,
    ))
    sesion.commit()
    return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)


@router.post("/generar-automatico")
def generar_automatico(request: Request, sesion: Session = Depends(obtener_sesion)):
    """El botón único: analiza, elige qué publicar, arma texto e imagen para Instagram
    y Facebook, y deja las dos listas para que Berenice las vea y confirme cada una
    con un solo click más."""
    if (redireccion := requiere_login(request)):
        return redireccion
    agente = AgentePCfix(sesion)
    agente.generar_publicacion_automatica()
    return RedirectResponse(url="/publicaciones/pendientes", status_code=303)


@router.post("/{publicacion_id}/marcar-publicada-manual")
def marcar_publicada_manual(publicacion_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    """Instagram no se conecta vía API (decisión de Berenice, ver memoria/PC_FIX.md) —
    el kit de texto+hashtags+imagen ya sale listo para copiar/descargar en la
    previsualización; este botón solo confirma que ella ya la publicó a mano en la app."""
    if (redireccion := requiere_login(request)):
        return redireccion
    publicacion = sesion.get(Publicacion, publicacion_id)
    if publicacion is None or publicacion.plataforma != "instagram":
        return RedirectResponse(url="/publicaciones/pendientes", status_code=303)
    if publicacion.estado not in ("previsualizado", "aprobado", "error"):
        return RedirectResponse(url=f"/publicaciones/{publicacion.id}/previsualizar", status_code=303)

    publicacion.estado = "publicado"
    sesion.add(RegistroAccion(
        herramienta="marcar_publicada_manual", datos_utilizados=f"publicacion_id={publicacion.id}",
        resultado="Marcada como publicada en Instagram — publicación manual (sin conexión API, decisión de Berenice).",
        requirio_aprobacion=True, aprobado=True,
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
