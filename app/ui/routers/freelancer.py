from fastapi import APIRouter, Request

from app.auth.dependencias import requiere_login
from app.ui.plantillas import templates

router = APIRouter()


@router.get("/freelancer")
def pantalla_freelancer(request: Request):
    if (redireccion := requiere_login(request)):
        return redireccion
    return templates.TemplateResponse("freelancer.html", {"request": request})
