"""Registro de fuentes de ofertas.

Para sumar una fuente nueva alcanza con crear un módulo con `NOMBRE`, `ETIQUETA`,
`SITIO`, `HORAS_ENTRE_CONSULTAS` y una función `obtener()` que devuelva una lista
de `OfertaExterna`, e importarlo acá.
"""

from app.services.fuentes import getonbrd, remoteok, remotive, weworkremotely

FUENTES = [getonbrd, remoteok, remotive, weworkremotely]

FUENTES_POR_NOMBRE = {modulo.NOMBRE: modulo for modulo in FUENTES}


def etiqueta_de(nombre: str) -> str:
    modulo = FUENTES_POR_NOMBRE.get(nombre)
    return modulo.ETIQUETA if modulo else nombre


__all__ = ["FUENTES", "FUENTES_POR_NOMBRE", "etiqueta_de"]
