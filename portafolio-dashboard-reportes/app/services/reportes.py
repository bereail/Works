"""Agregaciones para el panel de reportes de ventas.

Los cálculos se resuelven en Python sobre los objetos ya traídos de la base
(con carga anticipada de relaciones) en lugar de usar funciones de fecha
específicas de un motor de base de datos, para mantener el código portable
entre SQLite y Postgres.
"""

from collections import defaultdict
from datetime import date, timedelta

from sqlalchemy.orm import joinedload

from app import db
from app.models.pedido import Pedido, DetallePedido
from app.models.producto import Producto

PERIODOS_VALIDOS = {
    "30": "Últimos 30 días",
    "90": "Últimos 90 días",
    "todo": "Todo el período",
}


def obtener_fecha_maxima() -> date | None:
    return db.session.query(db.func.max(Pedido.fecha)).scalar()


def calcular_rango(periodo: str, fecha_maxima: date) -> tuple[date | None, date]:
    if periodo == "30":
        return fecha_maxima - timedelta(days=29), fecha_maxima
    if periodo == "90":
        return fecha_maxima - timedelta(days=89), fecha_maxima
    return None, fecha_maxima


def _pedidos_en_rango(fecha_desde: date | None, fecha_hasta: date) -> list[Pedido]:
    consulta = Pedido.query.options(
        joinedload(Pedido.detalles)
        .joinedload(DetallePedido.producto)
        .joinedload(Producto.categoria)
    )
    if fecha_desde is not None:
        consulta = consulta.filter(Pedido.fecha >= fecha_desde)
    consulta = consulta.filter(Pedido.fecha <= fecha_hasta)
    return consulta.all()


def calcular_kpis(pedidos: list[Pedido]) -> dict:
    total_ventas = sum(pedido.total for pedido in pedidos)
    cantidad_pedidos = len(pedidos)
    ticket_promedio = total_ventas / cantidad_pedidos if cantidad_pedidos else 0.0

    unidades_por_producto: dict[str, int] = defaultdict(int)
    for pedido in pedidos:
        for detalle in pedido.detalles:
            unidades_por_producto[detalle.producto.nombre] += detalle.cantidad

    if unidades_por_producto:
        producto_top_nombre, producto_top_unidades = max(
            unidades_por_producto.items(), key=lambda item: item[1]
        )
    else:
        producto_top_nombre, producto_top_unidades = "Sin datos", 0

    return {
        "total_ventas": round(total_ventas, 2),
        "ticket_promedio": round(ticket_promedio, 2),
        "cantidad_pedidos": cantidad_pedidos,
        "producto_top_nombre": producto_top_nombre,
        "producto_top_unidades": producto_top_unidades,
    }


def ventas_por_periodo(pedidos: list[Pedido], agrupar_por_semana: bool) -> list[dict]:
    totales: dict[date, float] = defaultdict(float)
    for pedido in pedidos:
        clave = pedido.fecha
        if agrupar_por_semana:
            clave = pedido.fecha - timedelta(days=pedido.fecha.weekday())
        totales[clave] += pedido.total

    fechas_ordenadas = sorted(totales.keys())
    return [
        {
            "fecha": fecha.strftime("%d/%m"),
            "total": round(totales[fecha], 2),
        }
        for fecha in fechas_ordenadas
    ]


def ventas_por_categoria(pedidos: list[Pedido]) -> list[dict]:
    totales: dict[str, float] = defaultdict(float)
    for pedido in pedidos:
        for detalle in pedido.detalles:
            totales[detalle.producto.categoria.nombre] += detalle.subtotal

    resultado = [
        {"categoria": categoria, "total": round(total, 2)}
        for categoria, total in totales.items()
    ]
    resultado.sort(key=lambda item: item["total"], reverse=True)
    return resultado


def top_productos(pedidos: list[Pedido], cantidad: int = 8) -> list[dict]:
    unidades: dict[str, int] = defaultdict(int)
    montos: dict[str, float] = defaultdict(float)
    categorias: dict[str, str] = {}

    for pedido in pedidos:
        for detalle in pedido.detalles:
            nombre = detalle.producto.nombre
            unidades[nombre] += detalle.cantidad
            montos[nombre] += detalle.subtotal
            categorias[nombre] = detalle.producto.categoria.nombre

    productos = [
        {
            "nombre": nombre,
            "categoria": categorias[nombre],
            "unidades": unidades[nombre],
            "monto": round(montos[nombre], 2),
        }
        for nombre in unidades
    ]
    productos.sort(key=lambda item: item["unidades"], reverse=True)
    return productos[:cantidad]
