"""La ingesta no puede duplicar ofertas, no puede traer ruido y no puede golpear las
APIs más seguido de lo que sus términos permiten. Los tests usan una fuente falsa: no
salen a internet."""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models  # noqa: F401  -- registra las tablas
from app.database import Base
from app.models import EstadoFuente, OportunidadFreelance
from app.services import ingesta
from app.services.fuentes.base import OfertaExterna


@pytest.fixture
def sesion():
    """Base en memoria: cada test arranca limpio y no toca freelancer.db."""
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    fabrica = sessionmaker(bind=engine)
    with fabrica() as s:
        yield s


def fuente_falsa(nombre="fuente_test", ofertas=None, revienta=False):
    def obtener():
        if revienta:
            raise ConnectionError("la API no responde")
        return ofertas or []

    return SimpleNamespace(
        NOMBRE=nombre,
        ETIQUETA="Fuente de prueba",
        SITIO="https://ejemplo.test",
        HORAS_ENTRE_CONSULTAS=6,
        obtener=obtener,
    )


def oferta_buena(id_externo="1", titulo="Desarrollador Django part-time"):
    return OfertaExterna(id_externo=id_externo, titulo=titulo, empresa="Empresa", ubicacion="Argentina")


def correr(sesion, modulos, forzar=False, monkeypatch=None):
    monkeypatch.setattr(ingesta, "FUENTES", modulos)
    return ingesta.importar_todo(sesion, forzar=forzar)


class TestImportacion:
    def test_guarda_la_oferta_en_la_bandeja_no_en_el_pipeline(self, sesion, monkeypatch):
        correr(sesion, [fuente_falsa(ofertas=[oferta_buena()])], monkeypatch=monkeypatch)

        guardada = sesion.query(OportunidadFreelance).one()
        assert guardada.estado == ingesta.ESTADO_BANDEJA
        assert guardada.origen == "importada"
        assert guardada.puntaje > 0

    def test_no_duplica_una_oferta_ya_guardada(self, sesion, monkeypatch):
        fuente = fuente_falsa(ofertas=[oferta_buena(id_externo="42")])

        correr(sesion, [fuente], monkeypatch=monkeypatch)
        resumen = correr(sesion, [fuente], forzar=True, monkeypatch=monkeypatch)

        assert sesion.query(OportunidadFreelance).count() == 1
        assert resumen.resultados[0].repetidas == 1

    def test_una_oferta_descartada_no_vuelve_a_aparecer(self, sesion, monkeypatch):
        """Si volviera a entrar en cada búsqueda, la bandeja sería inusable."""
        fuente = fuente_falsa(ofertas=[oferta_buena(id_externo="42")])
        correr(sesion, [fuente], monkeypatch=monkeypatch)

        sesion.query(OportunidadFreelance).one().estado = "descartada"
        sesion.commit()

        correr(sesion, [fuente], forzar=True, monkeypatch=monkeypatch)
        assert sesion.query(OportunidadFreelance).filter_by(estado=ingesta.ESTADO_BANDEJA).count() == 0

    def test_descarta_lo_que_no_llega_al_puntaje_minimo(self, sesion, monkeypatch):
        ruido = OfertaExterna(id_externo="9", titulo="Community Manager", etiquetas=["marketing"])
        resumen = correr(sesion, [fuente_falsa(ofertas=[ruido])], monkeypatch=monkeypatch)

        assert sesion.query(OportunidadFreelance).count() == 0
        assert resumen.resultados[0].poco_relevantes == 1

    def test_ignora_avisos_sin_identificador(self, sesion, monkeypatch):
        sin_id = OfertaExterna(id_externo="", titulo="Desarrollador Django")
        correr(sesion, [fuente_falsa(ofertas=[sin_id])], monkeypatch=monkeypatch)

        assert sesion.query(OportunidadFreelance).count() == 0


class TestEsperaEntreConsultas:
    def test_saltea_una_fuente_consultada_recien(self, sesion, monkeypatch):
        fuente = fuente_falsa(ofertas=[oferta_buena()])
        correr(sesion, [fuente], monkeypatch=monkeypatch)

        resumen = correr(sesion, [fuente], monkeypatch=monkeypatch)
        assert resumen.resultados[0].salteada is True

    def test_forzar_ignora_la_espera(self, sesion, monkeypatch):
        fuente = fuente_falsa(ofertas=[oferta_buena()])
        correr(sesion, [fuente], monkeypatch=monkeypatch)

        resumen = correr(sesion, [fuente], forzar=True, monkeypatch=monkeypatch)
        assert resumen.resultados[0].salteada is False

    def test_vuelve_a_consultar_pasada_la_espera(self, sesion, monkeypatch):
        fuente = fuente_falsa(ofertas=[oferta_buena()])
        correr(sesion, [fuente], monkeypatch=monkeypatch)

        estado = sesion.get(EstadoFuente, fuente.NOMBRE)
        estado.ultima_consulta = datetime.now(timezone.utc) - timedelta(hours=7)
        sesion.commit()

        resumen = correr(sesion, [fuente], monkeypatch=monkeypatch)
        assert resumen.resultados[0].salteada is False


class TestFuenteCaida:
    def test_una_fuente_caida_no_frena_a_las_demas(self, sesion, monkeypatch):
        modulos = [
            fuente_falsa(nombre="rota", revienta=True),
            fuente_falsa(nombre="sana", ofertas=[oferta_buena()]),
        ]
        resumen = correr(sesion, modulos, monkeypatch=monkeypatch)

        assert resumen.hubo_errores is True
        assert resumen.total_nuevas == 1
        assert "ConnectionError" in resumen.resultados[0].error

    def test_el_error_queda_registrado_para_mostrarlo_en_pantalla(self, sesion, monkeypatch):
        correr(sesion, [fuente_falsa(nombre="rota", revienta=True)], monkeypatch=monkeypatch)

        assert "ConnectionError" in sesion.get(EstadoFuente, "rota").ultimo_error
