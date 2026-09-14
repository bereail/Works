from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import obtener_sesion
from app.models import EstadoFuente, OportunidadFreelance
from app.services import relevancia
from app.services.fuentes import FUENTES, etiqueta_de
from app.services.ingesta import ESTADO_BANDEJA, importar_todo
from app.ui.plantillas import templates

router = APIRouter()

ESTADOS_ACTIVOS = ["por_postular", "postulada", "en_conversacion"]
ESTADOS_CERRADOS = ["ganada", "rechazada", "descartada"]
ESTADOS_PARA_POSTULARSE = ["nueva", "por_postular"]

# Accesos directos a búsquedas ya armadas en portales que no tienen API pública
# (por eso no se ingieren automático, coherente con no scrapear lo que lo prohíbe
# en sus términos) — Berenice hace un click y revisa/postula a mano ahí mismo.
PORTALES_BUSQUEDA_MANUAL = [
    {
        "nombre": "Computrabajo",
        "url": "https://ar.computrabajo.com/trabajo-de-desarrollador-full-stack-remoto",
        "descripcion": "El más grande en Argentina — conviene revisarlo seguido.",
    },
    {
        "nombre": "Bumeran",
        "url": "https://www.bumeran.com.ar/busquedas.html?q=desarrollador+full+stack+remoto",
        "descripcion": "Fuerte en PyMEs e instituciones locales.",
    },
    {
        "nombre": "ZonaJobs",
        "url": "https://www.zonajobs.com.ar/empleos-busqueda-desarrollador-full-stack-remoto.html",
        "descripcion": "Mismo grupo que Bumeran, avisos distintos igual.",
    },
    {
        "nombre": "LinkedIn Jobs",
        "url": "https://www.linkedin.com/jobs/search/?keywords=full%20stack%20django%20react&location=Argentina&f_WT=2",
        "descripcion": "Filtrado por remoto — buscá también \"contract\"/\"freelance\".",
    },
    {
        "nombre": "Indeed Argentina",
        "url": "https://ar.indeed.com/jobs?q=desarrollador+full+stack+remoto&l=Argentina",
        "descripcion": "Agrega avisos que no están en los otros cuatro.",
    },
]


@router.get("/")
def pantalla_freelancer(request: Request, sesion: Session = Depends(obtener_sesion)):
    total_activas = sesion.query(OportunidadFreelance).filter(OportunidadFreelance.estado.in_(ESTADOS_ACTIVOS)).count()
    total_bandeja = _contar_bandeja(sesion)
    return templates.TemplateResponse(request, "freelancer.html", {
        "total_ofertas_activas": total_activas,
        "total_bandeja": total_bandeja,
    })


@router.get("/ofertas")
def listado_ofertas(request: Request, estado: str = "", aviso: str = "", sesion: Session = Depends(obtener_sesion)):
    consulta = sesion.query(OportunidadFreelance)
    if estado:
        consulta = consulta.filter(OportunidadFreelance.estado == estado)

    # En la bandeja importa lo más parecido a su perfil; en el resto del pipeline,
    # lo más reciente.
    if estado == ESTADO_BANDEJA:
        consulta = consulta.order_by(OportunidadFreelance.puntaje.desc(), OportunidadFreelance.fecha_encontrada.desc())
    else:
        consulta = consulta.order_by(OportunidadFreelance.fecha_encontrada.desc())

    return templates.TemplateResponse(request, "freelancer_ofertas.html", {
        "ofertas": consulta.all(),
        "filtro_estado": estado,
        "estados_activos": ESTADOS_ACTIVOS,
        "estados_cerrados": ESTADOS_CERRADOS,
        "estado_bandeja": ESTADO_BANDEJA,
        "total_bandeja": _contar_bandeja(sesion),
        "aviso": aviso,
        "fuentes": _estado_de_fuentes(sesion),
        "puntaje_minimo": relevancia.PUNTAJE_MINIMO,
    })


@router.get("/postulaciones")
def pantalla_postulaciones(request: Request, sesion: Session = Depends(obtener_sesion)):
    """Todo lo que tiene sentido postular ya, en un solo lugar: un click abre el
    aviso original en su sitio para que Berenice se postule ahí (no lo hace esta
    app), y otro click acá lo marca como ya postulado."""
    consulta = (
        sesion.query(OportunidadFreelance)
        .filter(OportunidadFreelance.estado.in_(ESTADOS_PARA_POSTULARSE))
        .order_by(OportunidadFreelance.puntaje.desc(), OportunidadFreelance.fecha_encontrada.desc())
    )
    return templates.TemplateResponse(request, "freelancer_postulaciones.html", {
        "ofertas": consulta.all(),
        "portales": PORTALES_BUSQUEDA_MANUAL,
        "puntaje_minimo": relevancia.PUNTAJE_MINIMO,
    })


@router.post("/ofertas/buscar")
def buscar_ofertas(request: Request, forzar: str = Form(""), sesion: Session = Depends(obtener_sesion)):
    resumen = importar_todo(sesion, forzar=bool(forzar))
    destino = f"/ofertas?estado={ESTADO_BANDEJA}&aviso={resumen.texto}"
    return RedirectResponse(url=destino, status_code=303)


@router.get("/ofertas/nueva")
def formulario_nueva_oferta(request: Request):
    return templates.TemplateResponse(request, "freelancer_oferta_formulario.html", {"oferta": None})


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
    return templates.TemplateResponse(request, "freelancer_oferta_formulario.html", {"oferta": oferta})


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
def cambiar_estado_oferta(
    oferta_id: int,
    request: Request,
    estado: str = Form(...),
    volver_a: str = Form(""),
    sesion: Session = Depends(obtener_sesion),
):
    oferta = sesion.get(OportunidadFreelance, oferta_id)
    if oferta:
        oferta.estado = estado
        if estado == "postulada" and oferta.fecha_postulacion is None:
            oferta.fecha_postulacion = datetime.now(timezone.utc)
        sesion.commit()
    return RedirectResponse(url=volver_a or "/ofertas", status_code=303)


@router.post("/ofertas/{oferta_id}/eliminar")
def eliminar_oferta(oferta_id: int, request: Request, sesion: Session = Depends(obtener_sesion)):
    oferta = sesion.get(OportunidadFreelance, oferta_id)
    if oferta:
        sesion.delete(oferta)
        sesion.commit()
    return RedirectResponse(url="/ofertas", status_code=303)


def _contar_bandeja(sesion: Session) -> int:
    return sesion.query(OportunidadFreelance).filter(OportunidadFreelance.estado == ESTADO_BANDEJA).count()


def _estado_de_fuentes(sesion: Session) -> list[dict]:
    guardados = {e.nombre: e for e in sesion.query(EstadoFuente).all()}
    fuentes = []
    for modulo in FUENTES:
        estado = guardados.get(modulo.NOMBRE)
        fuentes.append({
            "nombre": modulo.NOMBRE,
            "etiqueta": modulo.ETIQUETA,
            "sitio": modulo.SITIO,
            "ultima_consulta": _hace_cuanto(estado.ultima_consulta if estado else None),
            "resultado": estado.ultimo_resultado if estado else "",
            "error": estado.ultimo_error if estado else "",
        })
    return fuentes


def _hace_cuanto(momento: datetime | None) -> str:
    if momento is None:
        return "nunca"
    if momento.tzinfo is None:
        momento = momento.replace(tzinfo=timezone.utc)
    minutos = int((datetime.now(timezone.utc) - momento).total_seconds() // 60)
    if minutos < 1:
        return "recien"
    if minutos < 60:
        return f"hace {minutos} min"
    horas = minutos // 60
    if horas < 24:
        return f"hace {horas} h"
    return f"hace {horas // 24} d"
