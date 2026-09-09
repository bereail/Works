import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from app import crear_app, db
from app.models.lead import Notificacion
from app.services.leads import actualizar_estado_lead, registrar_lead


@pytest.fixture()
def app():
    aplicacion = crear_app()
    aplicacion.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with aplicacion.app_context():
        db.create_all()
        yield aplicacion
        db.drop_all()


def test_registrar_lead_crea_lead_y_notificacion(app):
    with app.app_context():
        lead = registrar_lead({
            "nombre": "Ana Torres",
            "email": "ana@ejemplo.com",
            "telefono": "11 5555-1234",
            "empresa": "Ejemplo SRL",
            "mensaje": "Quiero automatizar mi facturación",
            "origen": "Google",
        })

        assert lead.id is not None
        assert lead.estado == "Nuevo"

        notificaciones = Notificacion.query.filter_by(lead_id=lead.id).all()
        assert len(notificaciones) == 1
        assert "Ana Torres" in notificaciones[0].mensaje


def test_actualizar_estado_lead_cambia_estado(app):
    with app.app_context():
        lead = registrar_lead({"nombre": "Luis Pérez", "email": "luis@ejemplo.com"})

        actualizado = actualizar_estado_lead(lead.id, "Contactado")

        assert actualizado.estado == "Contactado"


def test_actualizar_estado_invalido_lanza_error(app):
    with app.app_context():
        lead = registrar_lead({"nombre": "Sofía Ruiz", "email": "sofia@ejemplo.com"})

        with pytest.raises(ValueError):
            actualizar_estado_lead(lead.id, "Estado que no existe")
