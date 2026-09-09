from datetime import datetime

from app import db

ESTADOS_VALIDOS = ["Nuevo", "Contactado", "Convertido", "Descartado"]


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(40))
    empresa = db.Column(db.String(120))
    mensaje = db.Column(db.Text)
    origen = db.Column(db.String(60), nullable=False, default="Sin especificar")
    estado = db.Column(db.String(20), nullable=False, default="Nuevo")
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    notificaciones = db.relationship(
        "Notificacion", backref="lead", cascade="all, delete-orphan"
    )

    def a_diccionario(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "empresa": self.empresa,
            "mensaje": self.mensaje,
            "origen": self.origen,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion.strftime("%d/%m/%Y %H:%M"),
        }


class Notificacion(db.Model):
    __tablename__ = "notificaciones"

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def a_diccionario(self) -> dict:
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "mensaje": self.mensaje,
            "fecha_creacion": self.fecha_creacion.strftime("%d/%m/%Y %H:%M"),
        }
