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
    """Login desactivado: la app corre solo en localhost para uso personal de Berenice,
    así que nunca redirige a /login. Se deja la función (en vez de borrar sus usos en
    cada router) para poder reactivarla fácil si el día de mañana se expone la app afuera."""
    return None
