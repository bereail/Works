from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.ui.routers import freelancer

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Freelancer — Berenice")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "ui" / "static")), name="static")

app.include_router(freelancer.router)


@app.on_event("startup")
def al_iniciar() -> None:
    Base.metadata.create_all(bind=engine)
