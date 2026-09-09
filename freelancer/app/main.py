import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.models  # noqa: F401  -- registra las tablas en Base.metadata antes de crearlas
from app.database import Base, SesionLocal, agregar_columnas_faltantes, engine
from app.services.ingesta import importar_todo
from app.ui.routers import freelancer

BASE_DIR = Path(__file__).resolve().parent
HORAS_ENTRE_REFRESCOS = 6

# Colgado del logger de uvicorn: así los mensajes salen en uvicorn.log como el resto,
# sin tener que configurar handlers propios.
registro = logging.getLogger("uvicorn.error").getChild("ingesta")


async def _refrescar_ofertas_periodicamente() -> None:
    """Busca ofertas sola cada tantas horas, sin que Berenice tenga que apretar nada.

    Cada fuente igual respeta su propio mínimo de espera, así que este ciclo nunca
    consulta una API más seguido de lo que sus términos permiten.
    """
    while True:
        try:
            resumen = await asyncio.to_thread(_correr_ingesta)
            registro.info("Búsqueda automática: %s", resumen)
        except Exception as error:  # una fuente caída no puede tirar abajo la app
            registro.warning("Falló la búsqueda automática: %s", error)
        await asyncio.sleep(HORAS_ENTRE_REFRESCOS * 3600)


def _correr_ingesta() -> str:
    sesion = SesionLocal()
    try:
        return importar_todo(sesion).texto
    finally:
        sesion.close()


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    agregadas = agregar_columnas_faltantes()
    if agregadas:
        registro.info("Columnas nuevas agregadas a la base: %s", ", ".join(agregadas))

    tarea = asyncio.create_task(_refrescar_ofertas_periodicamente())
    yield
    tarea.cancel()


app = FastAPI(title="Freelancer — Berenice", lifespan=ciclo_de_vida)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "ui" / "static")), name="static")

app.include_router(freelancer.router)
