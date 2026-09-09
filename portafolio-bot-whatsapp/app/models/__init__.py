"""Modelos SQLAlchemy del bot de atención por WhatsApp."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(100))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos = db.relationship("Pedido", back_populates="cliente")
    mensajes = db.relationship("Mensaje", back_populates="cliente")


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True)


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    estado = db.Column(db.String(30), default="confirmado")
    total = db.Column(db.Float, nullable=False)
    tiempo_estimado_minutos = db.Column(db.Integer, default=30)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    items = db.relationship(
        "PedidoItem", back_populates="pedido", cascade="all, delete-orphan"
    )


class PedidoItem(db.Model):
    __tablename__ = "pedido_items"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    pedido = db.relationship("Pedido", back_populates="items")
    producto = db.relationship("Producto")

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio_unitario


class Mensaje(db.Model):
    __tablename__ = "mensajes"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    es_entrante = db.Column(db.Boolean, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    cliente = db.relationship("Cliente", back_populates="mensajes")
