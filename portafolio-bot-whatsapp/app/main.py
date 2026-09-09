"""Servidor Flask del bot de atención simulado por WhatsApp."""

from pathlib import Path

from flask import Flask, jsonify, render_template, request

from app.models import Producto, db
from app.services import bot

BASE_DIR = Path(__file__).resolve().parent
RUTA_BASE_DATOS = BASE_DIR / "bot_whatsapp.db"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "ui" / "templates"),
    static_folder=str(BASE_DIR / "ui" / "static"),
)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{RUTA_BASE_DATOS}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

PRODUCTOS_INICIALES = [
    {
        "nombre": "Empanada de carne (unidad)",
        "descripcion": "Cortada a cuchillo, horneada",
        "precio": 900,
    },
    {
        "nombre": "Empanada de jamón y queso (unidad)",
        "descripcion": "Horneada",
        "precio": 900,
    },
    {
        "nombre": "Pollo al spiedo entero",
        "descripcion": "Con papas españolas",
        "precio": 9800,
    },
    {
        "nombre": "Milanesa napolitana con papas fritas",
        "descripcion": "Milanesa de carne, jamón, queso y salsa",
        "precio": 7200,
    },
    {
        "nombre": "Ensalada mixta",
        "descripcion": "Lechuga, tomate y cebolla",
        "precio": 3200,
    },
]


def _sembrar_productos() -> None:
    if Producto.query.first() is not None:
        return
    for datos in PRODUCTOS_INICIALES:
        db.session.add(Producto(**datos))
    db.session.commit()


with app.app_context():
    db.create_all()
    _sembrar_productos()


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/historial/<telefono>")
def historial(telefono: str):
    return jsonify(bot.obtener_historial(telefono))


@app.route("/saludo/<telefono>")
def saludo(telefono: str):
    return jsonify(bot.obtener_saludo(telefono))


@app.route("/mensaje", methods=["POST"])
def mensaje():
    datos = request.get_json(force=True)
    telefono = datos.get("telefono", "")
    texto = datos.get("texto", "")
    respuestas = bot.procesar_mensaje(telefono, texto)
    return jsonify(respuestas)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
