from app import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    ciudad = db.Column(db.String(80))

    pedidos = db.relationship(
        "Pedido", backref="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cliente {self.nombre}>"
