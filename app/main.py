import secrets
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, SesionLocal, engine
from app.seed.datos_simulados import sembrar
from app.ui.routers import analiticas, automatizar, autenticacion, configuracion, dashboard, memoria, oportunidades, publicaciones

BASE_DIR = Path(__file__).resolve().parent
CLAVE_SESION_PATH = BASE_DIR.parent / ".clave_sesion"


def _obtener_o_crear_clave_sesion() -> str:
    if CLAVE_SESION_PATH.exists():
        return CLAVE_SESION_PATH.read_text().strip()
    clave = secrets.token_hex(32)
    CLAVE_SESION_PATH.write_text(clave)
    return clave


app = FastAPI(title="PCfix Automation Center")
app.add_middleware(SessionMiddleware, secret_key=_obtener_o_crear_clave_sesion())
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "ui" / "static")), name="static")

app.include_router(autenticacion.router)
app.include_router(dashboard.router)
app.include_router(automatizar.router)
app.include_router(oportunidades.router)
app.include_router(publicaciones.router)
app.include_router(analiticas.router)
app.include_router(memoria.router)
app.include_router(configuracion.router)


@app.on_event("startup")
def al_iniciar() -> None:
    Base.metadata.create_all(bind=engine)
    sesion = SesionLocal()
    try:
        sembrar(sesion)
    finally:
        sesion.close()
