from app import db


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, index=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    detalles = db.relationship(
        "DetallePedido", backref="pedido", cascade="all, delete-orphan"
    )

    @property
    def total(self) -> float:
        return sum(detalle.subtotal for detalle in self.detalles)

    def __repr__(self) -> str:
        return f"<Pedido {self.id} - {self.fecha}>"


class DetallePedido(db.Model):
    __tablename__ = "detalles_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    producto = db.relationship("Producto")

    @property
    def subtotal(self) -> float:
        return self.cantidad * self.precio_unitario

    def __repr__(self) -> str:
        return f"<DetallePedido pedido={self.pedido_id} producto={self.producto_id}>"
