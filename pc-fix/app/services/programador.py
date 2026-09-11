"""Programador interno: cada cierta cantidad de días, genera solo un borrador
de publicación nuevo (mismo flujo que el botón 🚀 Automatizar y publicar) para
que Berenice nunca tenga que acordarse de arrancarlo a mano.

Nunca publica nada por sí solo — solo deja el borrador listo en Pendientes,
esperando el click final de confirmación (misma regla de siempre).
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone

from app.agents.agente_negocio import AgentePCfix
from app.database import SesionLocal
from app.models import Publicacion

logger = logging.getLogger("programador")

DIAS_ENTRE_BORRADORES_AUTOMATICOS = 7
INTERVALO_CHEQUEO_SEGUNDOS = 60 * 60 * 6  # revisa cada 6 horas si toca generar


def _hay_que_generar_borrador(sesion) -> bool:
    ultima_publicacion = sesion.query(Publicacion).order_by(Publicacion.creado_en.desc()).first()
    if ultima_publicacion is None:
        return True
    limite = datetime.now(timezone.utc) - timedelta(days=DIAS_ENTRE_BORRADORES_AUTOMATICOS)
    creado_en = ultima_publicacion.creado_en
    if creado_en.tzinfo is None:
        creado_en = creado_en.replace(tzinfo=timezone.utc)
    return creado_en < limite


def generar_borrador_si_corresponde() -> None:
    sesion = SesionLocal()
    try:
        if not _hay_que_generar_borrador(sesion):
            return
        agente = AgentePCfix(sesion)
        agente.ejecutar_automatizacion_integral()
        publicaciones = agente.generar_publicacion_automatica()
        ids = [p.id for p in publicaciones]
        logger.info("Borradores semanales automáticos generados: publicacion_ids=%s", ids)
    except Exception:
        logger.exception("No se pudo generar el borrador semanal automático")
    finally:
        sesion.close()


async def correr_programador_en_segundo_plano() -> None:
    while True:
        generar_borrador_si_corresponde()
        await asyncio.sleep(INTERVALO_CHEQUEO_SEGUNDOS)
