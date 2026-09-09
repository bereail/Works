"""Trae ofertas nuevas desde las fuentes públicas y las guarda en la bandeja.

Cómo funciona una corrida:
1. Se saltean las fuentes consultadas hace menos de `HORAS_ENTRE_CONSULTAS` (a menos
   que se pida forzar), para respetar los límites que piden sus términos.
2. Se le calcula un puntaje de relevancia a cada aviso contra el perfil de Berenice.
3. Los que no llegan al puntaje mínimo se descartan sin guardarse.
4. Los repetidos (misma fuente + mismo id externo) se ignoran, así una oferta que
   ella ya descartó no vuelve a aparecer en cada búsqueda.
5. El resto entra con estado "nueva": la bandeja de entrada a revisar.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import EstadoFuente, OportunidadFreelance
from app.models.oportunidad import ORIGEN_IMPORTADA
from app.services import relevancia
from app.services.fuentes import FUENTES

ESTADO_BANDEJA = "nueva"


@dataclass
class ResultadoFuente:
    nombre: str
    etiqueta: str
    nuevas: int = 0
    repetidas: int = 0
    poco_relevantes: int = 0
    salteada: bool = False
    error: str = ""

    @property
    def resumen(self) -> str:
        if self.error:
            return f"error: {self.error}"
        if self.salteada:
            return "consultada hace poco, se salteó"
        return f"{self.nuevas} nuevas, {self.repetidas} ya conocidas, {self.poco_relevantes} poco relevantes"


@dataclass
class ResumenIngesta:
    resultados: list[ResultadoFuente] = field(default_factory=list)

    @property
    def total_nuevas(self) -> int:
        return sum(r.nuevas for r in self.resultados)

    @property
    def hubo_errores(self) -> bool:
        return any(r.error for r in self.resultados)

    @property
    def texto(self) -> str:
        if self.total_nuevas:
            return f"{self.total_nuevas} oferta{'s' if self.total_nuevas != 1 else ''} nueva{'s' if self.total_nuevas != 1 else ''} en la bandeja."
        if all(r.salteada for r in self.resultados):
            return "Todas las fuentes se consultaron hace menos de 6 horas. Se vuelven a consultar solas más tarde."
        return "No apareció nada nuevo que coincida con tu perfil."


def importar_todo(sesion: Session, forzar: bool = False) -> ResumenIngesta:
    resumen = ResumenIngesta()
    for modulo in FUENTES:
        resumen.resultados.append(_importar_fuente(sesion, modulo, forzar))
    sesion.commit()
    return resumen


def _importar_fuente(sesion: Session, modulo, forzar: bool) -> ResultadoFuente:
    resultado = ResultadoFuente(nombre=modulo.NOMBRE, etiqueta=modulo.ETIQUETA)
    estado = _estado_de(sesion, modulo.NOMBRE)

    if not forzar and _consultada_hace_poco(estado, modulo.HORAS_ENTRE_CONSULTAS):
        resultado.salteada = True
        return resultado

    try:
        ofertas = modulo.obtener()
    except Exception as error:
        resultado.error = f"{type(error).__name__}: {error}"[:200]
        estado.ultimo_error = resultado.error
        estado.ultima_consulta = datetime.now(timezone.utc)
        return resultado

    conocidos = _ids_ya_guardados(sesion, modulo.NOMBRE)

    for oferta in ofertas:
        if not oferta.id_externo or oferta.id_externo in conocidos:
            resultado.repetidas += 1
            continue

        puntaje = relevancia.calcular_puntaje(oferta, modulo.NOMBRE)
        if puntaje < relevancia.PUNTAJE_MINIMO:
            resultado.poco_relevantes += 1
            continue

        sesion.add(_a_oportunidad(oferta, modulo.NOMBRE, puntaje))
        conocidos.add(oferta.id_externo)
        resultado.nuevas += 1

    estado.ultima_consulta = datetime.now(timezone.utc)
    estado.ultimo_resultado = resultado.resumen
    estado.ultimo_error = ""
    return resultado


def _a_oportunidad(oferta, fuente: str, puntaje: int) -> OportunidadFreelance:
    return OportunidadFreelance(
        titulo=oferta.titulo[:255],
        cliente_o_empresa=oferta.empresa[:255],
        fuente=fuente,
        url=oferta.url[:500],
        tipo=oferta.tipo,
        estado=ESTADO_BANDEJA,
        origen=ORIGEN_IMPORTADA,
        id_externo=oferta.id_externo[:200],
        descripcion=oferta.descripcion,
        ubicacion=oferta.ubicacion[:200],
        salario=oferta.salario[:120],
        etiquetas=", ".join(oferta.etiquetas)[:400],
        puntaje=puntaje,
        fecha_publicacion=oferta.fecha_publicacion,
    )


def _estado_de(sesion: Session, nombre: str) -> EstadoFuente:
    estado = sesion.get(EstadoFuente, nombre)
    if estado is None:
        estado = EstadoFuente(nombre=nombre)
        sesion.add(estado)
    return estado


def _consultada_hace_poco(estado: EstadoFuente, horas: int) -> bool:
    if estado.ultima_consulta is None:
        return False
    ultima = estado.ultima_consulta
    if ultima.tzinfo is None:
        ultima = ultima.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - ultima < timedelta(hours=horas)


def _ids_ya_guardados(sesion: Session, fuente: str) -> set[str]:
    filas = sesion.query(OportunidadFreelance.id_externo).filter(OportunidadFreelance.fuente == fuente).all()
    return {fila[0] for fila in filas if fila[0]}
