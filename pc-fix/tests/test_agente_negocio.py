"""generar_publicacion_automatica es el botón único del dashboard: tiene que dejar
lista una publicación por red (Instagram y Facebook), con el mismo servicio e imagen,
pero copy adaptado por plataforma (hashtags solo en Instagram, CTA distinto) — así
Facebook queda a un click real de publicar y Instagram queda con su kit manual listo."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  -- registra las tablas en Base.metadata
from app.agents import agente_negocio as modulo_agente
from app.agents.agente_negocio import AgentePCfix
from app.database import Base
from app.models import IdentidadNegocio, Servicio


@pytest.fixture
def sesion():
    motor = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=motor)
    fabrica = sessionmaker(bind=motor)
    with fabrica() as s:
        yield s


@pytest.fixture(autouse=True)
def sin_playwright(monkeypatch):
    """Evita renderizar de verdad con Playwright en el test — solo interesa la lógica
    de generación de contenido, no el motor de flyers (ya cubierto en otro lado)."""
    monkeypatch.setattr(modulo_agente, "generar_flyer", lambda **kwargs: "generados/flyer_fake.png")


def _sembrar(sesion):
    sesion.add(IdentidadNegocio(
        nombre_comercial="PCfix", actividad="Servicio técnico", zona="Rosario",
        tagline="Se entiende lo que te arreglan.",
    ))
    sesion.add(Servicio(nombre="Cambio a SSD", categoria="mantenimiento", prioridad="verde", activo=True))
    sesion.commit()


class TestGenerarPublicacionAutomatica:
    def test_genera_una_publicacion_por_red_con_el_mismo_servicio(self, sesion):
        _sembrar(sesion)
        agente = AgentePCfix(sesion)

        publicaciones = agente.generar_publicacion_automatica()

        assert len(publicaciones) == 2
        plataformas = {p.plataforma for p in publicaciones}
        assert plataformas == {"instagram", "facebook"}
        assert all(p.servicio.nombre == "Cambio a SSD" for p in publicaciones)
        assert all(p.estado == "previsualizado" for p in publicaciones)

    def test_solo_instagram_lleva_hashtags(self, sesion):
        _sembrar(sesion)
        agente = AgentePCfix(sesion)

        publicaciones = agente.generar_publicacion_automatica()

        por_plataforma = {p.plataforma: p for p in publicaciones}
        assert por_plataforma["instagram"].hashtags != ""
        assert por_plataforma["facebook"].hashtags == ""

    def test_el_cta_es_distinto_por_plataforma(self, sesion):
        _sembrar(sesion)
        agente = AgentePCfix(sesion)

        publicaciones = agente.generar_publicacion_automatica()

        por_plataforma = {p.plataforma: p for p in publicaciones}
        assert por_plataforma["instagram"].cta != por_plataforma["facebook"].cta

    def test_ambas_reutilizan_el_mismo_archivo_de_flyer(self, sesion):
        _sembrar(sesion)
        agente = AgentePCfix(sesion)

        publicaciones = agente.generar_publicacion_automatica()

        rutas = {p.flyers[-1].archivo_generado for p in publicaciones}
        assert len(rutas) == 1

    def test_sin_servicios_activos_lanza_error_claro(self, sesion):
        sesion.add(IdentidadNegocio(nombre_comercial="PCfix", actividad="Servicio técnico", zona="Rosario"))
        sesion.commit()
        agente = AgentePCfix(sesion)

        with pytest.raises(ValueError):
            agente.generar_publicacion_automatica()
