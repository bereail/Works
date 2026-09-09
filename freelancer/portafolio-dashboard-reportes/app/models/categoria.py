from app import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)

    productos = db.relationship(
        "Producto", backref="categoria", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Categoria {self.nombre}>"
