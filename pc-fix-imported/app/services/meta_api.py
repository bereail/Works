"""Integración real con la Graph API de Meta para publicar en Facebook e Instagram.

Facebook permite subir el archivo de imagen directamente (multipart) — no necesita
URL pública. Instagram Content Publishing en cambio SÍ exige una URL pública que Meta
pueda descargar (limitación de la propia API de Meta, no de este código) — por eso
depende de `cuenta.url_base_publica` estar configurada en Configuración.
"""

import httpx

from app.models import CuentaConectada

VERSION_API = "v20.0"
URL_BASE = f"https://graph.facebook.com/{VERSION_API}"


class ErrorPublicacionMeta(Exception):
    """La Graph API de Meta devolvió un error al intentar publicar."""


def _mensaje_error(datos: dict, default: str) -> str:
    return datos.get("error", {}).get("message", default)


def publicar_en_facebook(cuenta: CuentaConectada, texto: str, ruta_imagen_absoluta: str) -> str:
    """Publica una foto con caption en la Página de Facebook. Devuelve el id del post creado."""
    url = f"{URL_BASE}/{cuenta.id_externo}/photos"
    with open(ruta_imagen_absoluta, "rb") as archivo_imagen:
        respuesta = httpx.post(
            url,
            params={"access_token": cuenta.access_token},
            data={"caption": texto},
            files={"source": archivo_imagen},
            timeout=30,
        )
    datos = respuesta.json()
    if respuesta.status_code >= 400 or "error" in datos:
        raise ErrorPublicacionMeta(_mensaje_error(datos, "Error desconocido al publicar en Facebook."))
    return datos.get("post_id") or datos.get("id", "")


def publicar_en_instagram(cuenta: CuentaConectada, texto: str, url_imagen_publica: str) -> str:
    """Publica una imagen en la cuenta de Instagram Business. Devuelve el id del media publicado.

    La API exige un proceso de dos pasos: primero crear el contenedor de media
    (con una URL pública de la imagen), después publicarlo.
    """
    url_crear = f"{URL_BASE}/{cuenta.id_externo}/media"
    respuesta_crear = httpx.post(
        url_crear,
        params={"access_token": cuenta.access_token},
        data={"image_url": url_imagen_publica, "caption": texto},
        timeout=30,
    )
    datos_crear = respuesta_crear.json()
    if respuesta_crear.status_code >= 400 or "error" in datos_crear:
        raise ErrorPublicacionMeta(_mensaje_error(datos_crear, "Error creando el contenedor de media en Instagram."))
    creation_id = datos_crear["id"]

    url_publicar = f"{URL_BASE}/{cuenta.id_externo}/media_publish"
    respuesta_publicar = httpx.post(
        url_publicar,
        params={"access_token": cuenta.access_token},
        data={"creation_id": creation_id},
        timeout=30,
    )
    datos_publicar = respuesta_publicar.json()
    if respuesta_publicar.status_code >= 400 or "error" in datos_publicar:
        raise ErrorPublicacionMeta(_mensaje_error(datos_publicar, "Error publicando el media en Instagram."))
    return datos_publicar.get("id", "")
