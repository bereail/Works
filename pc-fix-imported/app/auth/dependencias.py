from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.models import Usuario


class RedireccionLogin(Exception):
    pass


def obtener_usuario_actual(request: Request, sesion: Session) -> Usuario | None:
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return None
    return sesion.get(Usuario, usuario_id)


def requiere_login(request: Request) -> RedirectResponse | None:
    """Devuelve una RedirectResponse a /login si no hay sesión activa, o None si está todo bien."""
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/login", status_code=303)
    return None
