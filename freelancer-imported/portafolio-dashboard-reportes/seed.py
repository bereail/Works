"""Genera datos de ejemplo realistas para el panel de reportes.

Simula seis meses de ventas de una tienda online ficticia ("NovaShop"),
con estacionalidad semanal, una tendencia de crecimiento y algunos días
de promoción con picos de ventas.

Uso: python seed.py
"""

import random
from datetime import date, timedelta

from app import db
from app.main import app
from app.models.categoria import Categoria
from app.models.cliente import Cliente
from app.models.pedido import DetallePedido, Pedido
from app.models.producto import Producto

random.seed(42)

CATEGORIAS_PRODUCTOS = {
    "Indumentaria": [
        ("Remera básica de algodón", 8500),
        ("Buzo canguro frisado", 18900),
        ("Campera de jean", 32500),
        ("Pantalón jogger", 15200),
        ("Vestido de verano", 21800),
        ("Camisa lisa", 17300),
    ],
    "Calzado": [
        ("Zapatillas urbanas", 45900),
        ("Zapatillas running", 52300),
        ("Botitas de cuero", 38700),
        ("Ojotas de goma", 9800),
        ("Zapatos de vestir", 41200),
    ],
    "Accesorios": [
        ("Mochila urbana", 27600),
        ("Billetera de cuero", 12400),
        ("Cinturón de cuero", 9900),
        ("Gorra bordada", 8200),
        ("Anteojos de sol", 14500),
        ("Reloj analógico", 23800),
    ],
    "Hogar y Deco": [
        ("Set de sábanas", 19500),
        ("Almohada viscoelástica", 16800),
        ("Vela aromática", 6300),
        ("Portarretrato de madera", 5400),
        ("Manta polar", 14900),
        ("Difusor de aromas", 22100),
    ],
    "Tecnología": [
        ("Auriculares bluetooth", 34900),
        ("Cargador rápido USB-C", 9500),
        ("Parlante portátil", 28700),
        ("Mouse inalámbrico", 11200),
        ("Funda para celular", 7800),
        ("Power bank 10.000 mAh", 24300),
    ],
}

NOMBRES = [
    "Sofía", "Mateo", "Valentina", "Lucas", "Martina", "Benjamín", "Emma",
    "Santiago", "Catalina", "Joaquín", "Isabella", "Thiago", "Renata",
    "Bautista", "Julieta", "Agustín", "Delfina", "Franco", "Milagros",
    "Nicolás", "Camila", "Facundo", "Lucía", "Tomás", "Guadalupe", "Ramiro",
    "Victoria", "Ignacio", "Abril", "Simón",
]
APELLIDOS = [
    "González", "Rodríguez", "Fernández", "López", "Martínez", "Díaz",
    "Pérez", "Sánchez", "Romero", "Álvarez", "Torres", "Ruiz", "Flores",
    "Acosta", "Benítez", "Medina", "Suárez", "Herrera", "Vega", "Molina",
]
CIUDADES = [
    "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "La Plata",
    "Mar del Plata", "Salta", "Tucumán", "Neuquén", "Bahía Blanca",
]

DIAS_HISTORIA = 182
FECHA_FIN = date.today()
FECHA_INICIO = FECHA_FIN - timedelta(days=DIAS_HISTORIA - 1)

FACTOR_DIA_SEMANA = {
    0: 0.85,  # lunes
    1: 0.85,  # martes
    2: 0.90,  # miércoles
    3: 1.05,  # jueves
    4: 1.20,  # viernes
    5: 1.30,  # sábado
    6: 1.10,  # domingo
}


def _generar_dias_promocion() -> dict[date, float]:
    dias_promocion = {}
    cantidad_promos = 6
    for _ in range(cantidad_promos):
        offset = random.randint(5, DIAS_HISTORIA - 5)
        fecha_promo = FECHA_INICIO + timedelta(days=offset)
        dias_promocion[fecha_promo] = random.uniform(2.3, 3.2)
    return dias_promocion


def poblar_base_de_datos() -> None:
    with app.app_context():
        db.drop_all()
        db.create_all()

        categorias = {}
        for nombre_categoria in CATEGORIAS_PRODUCTOS:
            categoria = Categoria(nombre=nombre_categoria)
            db.session.add(categoria)
            categorias[nombre_categoria] = categoria
        db.session.flush()

        productos = []
        for nombre_categoria, lista_productos in CATEGORIAS_PRODUCTOS.items():
            for nombre_producto, precio in lista_productos:
                producto = Producto(
                    nombre=nombre_producto,
                    precio=precio,
                    categoria_id=categorias[nombre_categoria].id,
                )
                db.session.add(producto)
                productos.append(producto)
        db.session.flush()

        clientes = []
        for _ in range(160):
            nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
            cliente = Cliente(nombre=nombre, ciudad=random.choice(CIUDADES))
            db.session.add(cliente)
            clientes.append(cliente)
        db.session.flush()

        dias_promocion = _generar_dias_promocion()

        fecha_actual = FECHA_INICIO
        dia_indice = 0
        total_pedidos_generados = 0

        while fecha_actual <= FECHA_FIN:
            factor_crecimiento = 1 + (dia_indice / DIAS_HISTORIA) * 0.5
            factor_dia_semana = FACTOR_DIA_SEMANA[fecha_actual.weekday()]
            factor_promocion = dias_promocion.get(fecha_actual, 1.0)
            ruido = random.uniform(0.75, 1.25)

            cantidad_pedidos_dia = max(
                4,
                round(16 * factor_crecimiento * factor_dia_semana * factor_promocion * ruido),
            )

            for _ in range(cantidad_pedidos_dia):
                cliente = random.choice(clientes)
                pedido = Pedido(fecha=fecha_actual, cliente_id=cliente.id)
                db.session.add(pedido)
                db.session.flush()

                cantidad_items = random.choices([1, 2, 3, 4], weights=[45, 30, 18, 7])[0]
                productos_pedido = random.sample(productos, k=min(cantidad_items, len(productos)))

                for producto in productos_pedido:
                    cantidad = random.choices([1, 2, 3], weights=[70, 22, 8])[0]
                    detalle = DetallePedido(
                        pedido_id=pedido.id,
                        producto_id=producto.id,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                    )
                    db.session.add(detalle)

            total_pedidos_generados += cantidad_pedidos_dia
            fecha_actual += timedelta(days=1)
            dia_indice += 1

        db.session.commit()

        print("Base de datos poblada: datos.db")
        print(f"Categorias: {len(categorias)}")
        print(f"Productos: {len(productos)}")
        print(f"Clientes: {len(clientes)}")
        print(f"Pedidos generados: {total_pedidos_generados}")
        print(f"Periodo: {FECHA_INICIO} a {FECHA_FIN}")


if __name__ == "__main__":
    poblar_base_de_datos()
