from app import db
from app.models.lead import ESTADOS_VALIDOS, Lead
from app.services.notificaciones import notificar_nuevo_lead


def registrar_lead(datos: dict) -> Lead:
    lead = Lead(
        nombre=datos["nombre"].strip(),
        email=datos["email"].strip(),
        telefono=datos.get("telefono", "").strip(),
        empresa=datos.get("empresa", "").strip(),
        mensaje=datos.get("mensaje", "").strip(),
        origen=datos.get("origen") or "Sin especificar",
        estado="Nuevo",
    )
    db.session.add(lead)
    db.session.commit()

    notificar_nuevo_lead(lead)

    return lead


def actualizar_estado_lead(lead_id: int, nuevo_estado: str) -> Lead | None:
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise ValueError(f"Estado inválido: {nuevo_estado}")

    lead = db.session.get(Lead, lead_id)
    if lead is None:
        return None

    lead.estado = nuevo_estado
    db.session.commit()
    return lead


def listar_leads(busqueda: str = "") -> list[Lead]:
    consulta = Lead.query
    if busqueda:
        patron = f"%{busqueda.lower()}%"
        consulta = consulta.filter(
            db.or_(
                db.func.lower(Lead.nombre).like(patron),
                db.func.lower(Lead.email).like(patron),
            )
        )
    return consulta.order_by(Lead.fecha_creacion.desc()).all()
