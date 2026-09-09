from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_BASE_DATOS = BASE_DIR / "freelancer.db"

engine = create_engine(f"sqlite:///{RUTA_BASE_DATOS}", connect_args={"check_same_thread": False})
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def obtener_sesion():
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()


def agregar_columnas_faltantes(motor=None) -> list[str]:
    """Suma a las tablas ya creadas las columnas nuevas del modelo.

    `create_all` solo crea tablas que no existen: nunca toca una tabla vieja.
    Como el proyecto no usa Alembic, esta función cubre el caso simple de sumar
    columnas (ALTER TABLE ADD COLUMN es SQL estándar, así que también va a
    funcionar el día que se migre a PostgreSQL). No renombra ni borra nada.
    """
    motor = motor or engine
    inspector = inspect(motor)
    agregadas: list[str] = []

    with motor.begin() as conexion:
        for tabla in Base.metadata.sorted_tables:
            if tabla.name not in inspector.get_table_names():
                continue
            existentes = {c["name"] for c in inspector.get_columns(tabla.name)}
            for columna in tabla.columns:
                if columna.name in existentes:
                    continue
                tipo = columna.type.compile(motor.dialect)
                sentencia = f"ALTER TABLE {tabla.name} ADD COLUMN {columna.name} {tipo}"
                if columna.default is not None and columna.default.is_scalar:
                    valor = columna.default.arg
                    literal = f"'{valor}'" if isinstance(valor, str) else valor
                    sentencia += f" DEFAULT {literal}"
                conexion.execute(text(sentencia))
                agregadas.append(f"{tabla.name}.{columna.name}")

    return agregadas
