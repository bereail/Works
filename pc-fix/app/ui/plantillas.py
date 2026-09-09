from pathlib import Path

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

DIR_TEMPLATES = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(DIR_TEMPLATES))


def contexto_comun(sesion: Session) -> dict:
    from app.models import IdentidadNegocio
    return {"identidad": sesion.query(IdentidadNegocio).first()}
