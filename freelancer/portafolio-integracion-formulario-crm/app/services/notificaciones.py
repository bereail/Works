"""
Simula el paso de "notificación" en el flujo de automatización
formulario -> CRM -> notificación.

En un caso real acá se integraría un servicio externo (email, Slack,
WhatsApp Business API, etc). Para esta demo se registra la notificación
en la base de datos y se deja constancia en la consola del servidor,
manteniendo el mismo patrón que tendría una integración real.
"""

from app import db
from app.models.lead import Lead, Notificacion


def notificar_nuevo_lead(lead: Lead) -> Notificacion:
    mensaje = (
        f"Nuevo lead recibido: {lead.nombre} ({lead.email}) "
        f"vía {lead.origen}. Empresa: {lead.empresa or 'no informada'}."
    )

    print(f"[NOTIFICACIÓN SIMULADA] {mensaje}")

    notificacion = Notificacion(lead_id=lead.id, mensaje=mensaje)
    db.session.add(notificacion)
    db.session.commit()

    return notificacion
