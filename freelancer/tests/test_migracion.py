"""La base de Berenice ya existía antes de la ingesta automática, con la tabla vieja de
ofertas. `create_all` no toca una tabla que ya está creada, así que las columnas nuevas
tienen que sumarse aparte — y si eso falla, la app arranca y explota al primer guardado."""

from sqlalchemy import create_engine, inspect, text

import app.models  # noqa: F401  -- registra las tablas
from app.database import Base, agregar_columnas_faltantes

COLUMNAS_VIEJAS = """
    CREATE TABLE oportunidades_freelance (
        id INTEGER NOT NULL PRIMARY KEY,
        titulo VARCHAR(255),
        cliente_o_empresa VARCHAR(255),
        fuente VARCHAR(50),
        url VARCHAR(500),
        tipo VARCHAR(30),
        estado VARCHAR(30),
        notas TEXT,
        fecha_encontrada DATETIME,
        fecha_postulacion DATETIME,
        creado_en DATETIME
    )
"""


def base_con_esquema_viejo():
    motor = create_engine("sqlite://", connect_args={"check_same_thread": False})
    with motor.begin() as conexion:
        conexion.execute(text(COLUMNAS_VIEJAS))
    return motor


def test_suma_las_columnas_nuevas_a_una_tabla_que_ya_existia():
    motor = base_con_esquema_viejo()

    agregadas = agregar_columnas_faltantes(motor)

    columnas = {c["name"] for c in inspect(motor).get_columns("oportunidades_freelance")}
    assert {"origen", "id_externo", "descripcion", "puntaje", "fecha_publicacion"} <= columnas
    assert len(agregadas) == 8


def test_no_pisa_los_datos_que_ya_estaban():
    motor = base_con_esquema_viejo()
    with motor.begin() as conexion:
        conexion.execute(text("INSERT INTO oportunidades_freelance (titulo, estado) VALUES ('Cargada a mano', 'postulada')"))

    agregar_columnas_faltantes(motor)

    with motor.begin() as conexion:
        fila = conexion.execute(text("SELECT titulo, estado FROM oportunidades_freelance")).one()
    assert fila == ("Cargada a mano", "postulada")


def test_correrla_dos_veces_no_rompe():
    """Se ejecuta en cada arranque de la app."""
    motor = base_con_esquema_viejo()

    agregar_columnas_faltantes(motor)
    assert agregar_columnas_faltantes(motor) == []


def test_crea_la_tabla_de_estado_de_fuentes_desde_cero():
    motor = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=motor)

    assert "estado_fuentes" in inspect(motor).get_table_names()
