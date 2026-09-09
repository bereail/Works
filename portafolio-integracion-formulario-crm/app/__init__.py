from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def crear_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///crm.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_AS_ASCII"] = False

    db.init_app(app)

    from app.models.lead import Lead, Notificacion  # noqa: F401

    with app.app_context():
        db.create_all()

    from app.rutas import registrar_rutas
    registrar_rutas(app)

    return app
