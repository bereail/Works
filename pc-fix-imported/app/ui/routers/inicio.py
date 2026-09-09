from fastapi import APIRouter, Request

from app.ui.plantillas import templates

router = APIRouter()


@router.get("/inicio")
def pantalla_inicio(request: Request):
    return templates.TemplateResponse("inicio.html", {"request": request})
