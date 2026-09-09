"""Las pantallas tienen que responder y el pipeline de estados tiene que moverse.
La búsqueda se reemplaza por una falsa: los tests no salen a internet."""

from urllib.parse import unquote

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401  -- registra las tablas
from app.database import Base, obtener_sesion
from app.main import app
from app.models import OportunidadFreelance
from app.services.ingesta import ESTADO_BANDEJA


@pytest.fixture
def cliente():
    # StaticPool: una base en memoria vive dentro de su conexion, y TestClient
    # atiende los pedidos en otro hilo. Sin esto, la app no ve las tablas creadas aca.
    motor = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=motor)
    fabrica = sessionmaker(bind=motor)

    def sesion_de_prueba():
        with fabrica() as s:
            yield s

    app.dependency_overrides[obtener_sesion] = sesion_de_prueba
    # `with TestClient` dispararia el ciclo de vida real, que crea la base de verdad
    # y arranca la busqueda periodica: para probar las rutas no hace falta nada de eso.
    yield TestClient(app), fabrica
    app.dependency_overrides.clear()


def guardar(fabrica, **campos):
    with fabrica() as s:
        oferta = OportunidadFreelance(**{"titulo": "Django Developer", **campos})
        s.add(oferta)
        s.commit()
        return oferta.id


class TestPantallas:
    def test_el_inicio_responde(self, cliente):
        api, _ = cliente
        assert api.get("/").status_code == 200

    def test_el_listado_responde_sin_ofertas(self, cliente):
        api, _ = cliente
        respuesta = api.get("/ofertas")
        assert respuesta.status_code == 200
        assert "Todavía no hay ninguna oferta" in respuesta.text

    def test_la_bandeja_vacia_invita_a_buscar(self, cliente):
        api, _ = cliente
        assert "Buscar ahora" in api.get(f"/ofertas?estado={ESTADO_BANDEJA}").text

    def test_muestra_las_cuatro_fuentes_conectadas(self, cliente):
        api, _ = cliente
        texto = api.get("/ofertas").text
        for etiqueta in ("Get on Board", "Remote OK", "Remotive", "We Work Remotely"):
            assert etiqueta in texto

    def test_la_bandeja_ordena_por_afinidad(self, cliente):
        api, fabrica = cliente
        guardar(fabrica, titulo="Menos afin", estado=ESTADO_BANDEJA, puntaje=30, origen="importada")
        guardar(fabrica, titulo="Mas afin", estado=ESTADO_BANDEJA, puntaje=80, origen="importada")

        texto = api.get(f"/ofertas?estado={ESTADO_BANDEJA}").text
        assert texto.index("Mas afin") < texto.index("Menos afin")

    def test_el_inicio_avisa_cuantas_hay_sin_revisar(self, cliente):
        api, fabrica = cliente
        guardar(fabrica, estado=ESTADO_BANDEJA, origen="importada")

        assert "1 sin revisar" in api.get("/").text


class TestPipeline:
    def test_me_interesa_pasa_la_oferta_a_por_postular(self, cliente):
        api, fabrica = cliente
        identificador = guardar(fabrica, estado=ESTADO_BANDEJA, origen="importada")

        api.post(f"/ofertas/{identificador}/estado", data={"estado": "por_postular"}, follow_redirects=False)

        with fabrica() as s:
            assert s.get(OportunidadFreelance, identificador).estado == "por_postular"

    def test_vuelve_a_la_bandeja_despues_de_decidir(self, cliente):
        api, fabrica = cliente
        identificador = guardar(fabrica, estado=ESTADO_BANDEJA, origen="importada")

        respuesta = api.post(
            f"/ofertas/{identificador}/estado",
            data={"estado": "descartada", "volver_a": f"/ofertas?estado={ESTADO_BANDEJA}"},
            follow_redirects=False,
        )
        assert respuesta.headers["location"] == f"/ofertas?estado={ESTADO_BANDEJA}"

    def test_marcar_postulada_registra_la_fecha(self, cliente):
        api, fabrica = cliente
        identificador = guardar(fabrica, estado="por_postular")

        api.post(f"/ofertas/{identificador}/estado", data={"estado": "postulada"}, follow_redirects=False)

        with fabrica() as s:
            assert s.get(OportunidadFreelance, identificador).fecha_postulacion is not None


class TestBusqueda:
    def test_el_boton_de_buscar_deja_el_resultado_a_la_vista(self, cliente, monkeypatch):
        from app.ui.routers import freelancer as router

        monkeypatch.setattr(
            router, "importar_todo",
            lambda sesion, forzar=False: type("R", (), {"texto": "3 ofertas nuevas en la bandeja."})(),
        )
        api, _ = cliente

        respuesta = api.post("/ofertas/buscar", data={}, follow_redirects=False)
        destino = unquote(respuesta.headers["location"])

        assert respuesta.status_code == 303
        assert ESTADO_BANDEJA in destino
        assert "3 ofertas nuevas" in destino


class TestCargaManual:
    def test_la_carga_a_mano_sigue_andando(self, cliente):
        api, fabrica = cliente

        api.post("/ofertas/nueva", data={
            "titulo": "Sistema para un cliente de PC Fix",
            "cliente_o_empresa": "Comercio de Rosario",
            "fuente": "referido",
            "tipo": "proyecto_freelance",
        }, follow_redirects=False)

        with fabrica() as s:
            oferta = s.query(OportunidadFreelance).one()
        assert oferta.origen == "manual"
        assert oferta.estado == "por_postular"
