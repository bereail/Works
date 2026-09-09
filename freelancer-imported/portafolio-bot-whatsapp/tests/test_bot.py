"""Pruebas básicas del flujo conversacional del bot."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from flask import Flask

from app.models import Producto, db
from app.services import bot


@pytest.fixture()
def contexto_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.add(Producto(nombre="Empanada de carne", precio=900))
        db.session.add(Producto(nombre="Pollo al spiedo", precio=9800))
        db.session.commit()
        bot._estados_conversacion.clear()
        yield app


def test_saludo_inicial_muestra_menu(contexto_app):
    respuestas = bot.obtener_saludo("+54 9 11 1111-1111")
    assert "Bienvenido" in respuestas[0]["texto"]
    assert "1️⃣" in respuestas[0]["texto"]


def test_ver_catalogo_lista_productos(contexto_app):
    telefono = "+54 9 11 2222-2222"
    bot.obtener_saludo(telefono)
    respuestas = bot.procesar_mensaje(telefono, "1")
    assert "Empanada de carne" in respuestas[0]["texto"]
    assert "Pollo al spiedo" in respuestas[0]["texto"]


def test_flujo_completo_de_pedido_lo_persiste(contexto_app):
    telefono = "+54 9 11 3333-3333"
    bot.obtener_saludo(telefono)

    bot.procesar_mensaje(telefono, "2")
    bot.procesar_mensaje(telefono, "1")
    bot.procesar_mensaje(telefono, "3")
    bot.procesar_mensaje(telefono, "no")
    respuestas = bot.procesar_mensaje(telefono, "confirmar")

    assert "Pedido confirmado" in respuestas[0]["texto"]

    cliente = bot.obtener_o_crear_cliente(telefono)
    from app.models import Pedido

    pedido = Pedido.query.filter_by(cliente_id=cliente.id).first()
    assert pedido is not None
    assert pedido.total == 2700
    assert pedido.items[0].cantidad == 3


def test_mensaje_no_reconocido_reenvia_menu(contexto_app):
    telefono = "+54 9 11 4444-4444"
    bot.obtener_saludo(telefono)
    respuestas = bot.procesar_mensaje(telefono, "asdasd")
    assert "No entendí" in respuestas[0]["texto"]
