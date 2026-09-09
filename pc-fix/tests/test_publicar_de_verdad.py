"""_publicar_de_verdad es el punto donde el sistema decide si una publicación sale de
verdad a Facebook/Instagram o queda bloqueada. Estos tests cubren esa lógica de
bloqueo (sin la cual una publicación mal configurada podría intentar salir igual, o
al revés: quedar trabada sin explicación) y el camino feliz, con la llamada real a
Meta simulada — no salen a internet."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  -- registra las tablas en Base.metadata
from app.database import Base
from app.models import CuentaConectada, Flyer, Publicacion
from app.services.meta_api import ErrorPublicacionMeta
from app.ui.routers import publicaciones as router_publicaciones


@pytest.fixture
def sesion():
    motor = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=motor)
    fabrica = sessionmaker(bind=motor)
    with fabrica() as s:
        yield s


def _publicacion(sesion, plataforma="facebook", con_flyer=True, archivo_generado="flyers/x.jpg"):
    publicacion = Publicacion(
        plataforma=plataforma, fecha=datetime.now(timezone.utc), formato="imagen",
        tema="Promo SSD", texto="Repotenciá tu PC", cta="Escribinos", estado="aprobado",
    )
    sesion.add(publicacion)
    sesion.flush()
    if con_flyer:
        sesion.add(Flyer(publicacion_id=publicacion.id, titular="Promo SSD", archivo_generado=archivo_generado))
        sesion.flush()
        sesion.refresh(publicacion)
    return publicacion


def _cuenta_conectada(sesion, plataforma="facebook", **extra):
    datos = dict(
        plataforma=plataforma, nombre_cuenta="PC Fix", estado_conexion="conectada",
        id_externo="725615510632047", access_token="token-real",
    )
    datos.update(extra)
    cuenta = CuentaConectada(**datos)
    sesion.add(cuenta)
    sesion.flush()
    return cuenta


class TestBloqueos:
    def test_bloquea_si_no_hay_cuenta_conectada_para_la_plataforma(self, sesion):
        publicacion = _publicacion(sesion, plataforma="facebook")
        resultado = router_publicaciones._publicar_de_verdad(sesion, publicacion)
        assert "no está conectada de verdad" in resultado
        assert publicacion.estado == "aprobado"  # no se tocó

    def test_bloquea_si_la_cuenta_esta_en_modo_simulado(self, sesion):
        _cuenta_conectada(sesion, plataforma="instagram", estado_conexion="simulado", access_token="", id_externo="")
        publicacion = _publicacion(sesion, plataforma="instagram")
        resultado = router_publicaciones._publicar_de_verdad(sesion, publicacion)
        assert "no está conectada de verdad" in resultado

    def test_bloquea_si_falta_el_flyer(self, sesion):
        _cuenta_conectada(sesion, plataforma="facebook")
        publicacion = _publicacion(sesion, plataforma="facebook", con_flyer=False)
        resultado = router_publicaciones._publicar_de_verdad(sesion, publicacion)
        assert "no tiene un flyer generado" in resultado

    def test_bloquea_si_el_archivo_del_flyer_no_existe_en_disco(self, sesion):
        _cuenta_conectada(sesion, plataforma="facebook")
        publicacion = _publicacion(sesion, plataforma="facebook", archivo_generado="flyers/no-existe-nunca.jpg")
        resultado = router_publicaciones._publicar_de_verdad(sesion, publicacion)
        assert "no se encontró el archivo" in resultado

    def test_instagram_bloquea_si_falta_la_url_publica(self, sesion, monkeypatch, tmp_path):
        _cuenta_conectada(sesion, plataforma="instagram", url_base_publica="")
        ruta = tmp_path / "flyer.jpg"
        ruta.write_bytes(b"x")
        publicacion = _publicacion(sesion, plataforma="instagram", archivo_generado="flyer.jpg")
        monkeypatch.setattr(router_publicaciones, "RUTA_STATIC", str(tmp_path))

        resultado = router_publicaciones._publicar_de_verdad(sesion, publicacion)
        assert "falta configurar la URL pública" in resultado


class TestCaminoFeliz:
    def test_publica_de_verdad_y_actualiza_estado_y_id_externo(self, sesion, monkeypatch, tmp_path):
        _cuenta_conectada(sesion, plataforma="facebook")
        ruta = tmp_path / "flyer.jpg"
        ruta.write_bytes(b"x")
        publicacion = _publicacion(sesion, plataforma="facebook", archivo_generado="flyer.jpg")
        monkeypatch.setattr(router_publicaciones, "RUTA_STATIC", str(tmp_path))
        monkeypatch.setattr(router_publicaciones, "publicar_en_facebook", lambda *a, **k: "id-post-real")

        resultado = router_publicaciones._publicar_de_verdad(sesion, publicacion)

        assert publicacion.estado == "publicado"
        assert publicacion.id_publicacion_externa == "id-post-real"
        assert "id-post-real" in resultado


class TestErrorDeMeta:
    def test_si_meta_devuelve_error_la_publicacion_queda_en_estado_error(self, sesion, monkeypatch, tmp_path):
        _cuenta_conectada(sesion, plataforma="facebook")
        ruta = tmp_path / "flyer.jpg"
        ruta.write_bytes(b"x")
        publicacion = _publicacion(sesion, plataforma="facebook", archivo_generado="flyer.jpg")
        monkeypatch.setattr(router_publicaciones, "RUTA_STATIC", str(tmp_path))

        def falla(*a, **k):
            raise ErrorPublicacionMeta("Token vencido")

        monkeypatch.setattr(router_publicaciones, "publicar_en_facebook", falla)

        resultado = router_publicaciones._publicar_de_verdad(sesion, publicacion)

        assert publicacion.estado == "error"
        assert "Token vencido" in resultado
