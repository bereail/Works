"""Lógica conversacional del bot de atención de la rotisería."""

import unicodedata
from datetime import datetime
from random import randint

from app.models import Cliente, Mensaje, Pedido, PedidoItem, Producto, db

NOMBRE_NEGOCIO = "Rotisería Doña Pepa"

# Estado de la conversación por cliente, en memoria (alcanza para una demo).
_estados_conversacion: dict[int, dict] = {}


def _normalizar(texto: str) -> str:
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(caracter for caracter in texto if not unicodedata.combining(caracter))


def _a_entero(texto: str) -> int | None:
    try:
        return int(texto)
    except ValueError:
        return None


def _formatear_precio(valor: float) -> str:
    return f"${valor:,.0f}".replace(",", ".")


def _empaquetar(texto: str) -> dict:
    return {"texto": texto, "hora": datetime.now().strftime("%H:%M")}


def obtener_o_crear_cliente(telefono: str) -> Cliente:
    cliente = Cliente.query.filter_by(telefono=telefono).first()
    if cliente is None:
        cliente = Cliente(telefono=telefono)
        db.session.add(cliente)
        db.session.commit()
    return cliente


def _estado_de(cliente_id: int) -> dict:
    return _estados_conversacion.setdefault(
        cliente_id, {"paso": "inicio", "carrito": [], "producto_temporal": None}
    )


def _guardar_mensaje(cliente: Cliente, texto: str, es_entrante: bool) -> None:
    mensaje = Mensaje(cliente_id=cliente.id, texto=texto, es_entrante=es_entrante)
    db.session.add(mensaje)
    db.session.commit()


def _texto_menu() -> str:
    return (
        f"¡Hola! 👋 Bienvenido/a a *{NOMBRE_NEGOCIO}*.\n"
        "¿En qué te puedo ayudar?\n\n"
        "1️⃣ Ver catálogo\n"
        "2️⃣ Hacer un pedido\n"
        "3️⃣ Consultar el estado de mi pedido\n"
        "4️⃣ Hablar con una persona"
    )


def _productos_disponibles() -> list[Producto]:
    return Producto.query.filter_by(disponible=True).order_by(Producto.id).all()


def _texto_catalogo() -> str:
    productos = _productos_disponibles()
    lineas = [
        f"{indice}. {producto.nombre} — {_formatear_precio(producto.precio)}"
        for indice, producto in enumerate(productos, start=1)
    ]
    return "📋 *Nuestro catálogo:*\n\n" + "\n".join(lineas)


def _texto_lista_numerada() -> str:
    productos = _productos_disponibles()
    lineas = [
        f"{indice}. {producto.nombre} — {_formatear_precio(producto.precio)}"
        for indice, producto in enumerate(productos, start=1)
    ]
    return "¿Qué producto querés agregar? Escribí el número:\n\n" + "\n".join(lineas)


def _texto_estado_pedido(cliente: Cliente) -> str:
    pedido = (
        Pedido.query.filter_by(cliente_id=cliente.id)
        .order_by(Pedido.creado_en.desc())
        .first()
    )
    if pedido is None:
        return "Todavía no hiciste ningún pedido. Escribí *2* para empezar uno ahora. 🛒"

    minutos_transcurridos = (datetime.utcnow() - pedido.creado_en).total_seconds() / 60
    if minutos_transcurridos < pedido.tiempo_estimado_minutos:
        restante = max(int(pedido.tiempo_estimado_minutos - minutos_transcurridos), 1)
        estado_actual = "🍳 En preparación"
        detalle = f"Tiempo estimado restante: {restante} min."
    else:
        estado_actual = "✅ Listo para retirar"
        detalle = "¡Ya podés pasar a buscarlo!"

    items_texto = "\n".join(
        f"• {item.cantidad}x {item.producto.nombre}" for item in pedido.items
    )
    return (
        f"📦 *Tu último pedido* (#{pedido.id})\n\n"
        f"{items_texto}\n\n"
        f"Total: {_formatear_precio(pedido.total)}\n"
        f"Estado: {estado_actual}\n{detalle}"
    )


def _manejar_menu_principal(texto: str, estado: dict, cliente: Cliente) -> list[str]:
    if texto in {"1", "catalogo", "ver catalogo"}:
        return [
            _texto_catalogo(),
            "¿Necesitás algo más? Escribí *2* para hacer un pedido o *menu* para volver al inicio.",
        ]

    if texto in {"2", "pedido", "hacer pedido", "hacer un pedido"}:
        estado["paso"] = "pedido_eligiendo_producto"
        estado["carrito"] = []
        return [_texto_lista_numerada()]

    if texto in {"3", "estado", "consultar estado", "estado del pedido"}:
        return [_texto_estado_pedido(cliente)]

    if texto in {"4", "humano", "hablar con un humano", "hablar con una persona"}:
        return [
            "Listo, te va a contactar una persona del equipo en breve. 🙋 "
            "Mientras tanto podés escribir *menu* para volver a las opciones."
        ]

    return ["No entendí tu mensaje 🤔. Elegí una de estas opciones:", _texto_menu()]


def _manejar_eleccion_producto(texto: str, estado: dict) -> list[str]:
    productos = _productos_disponibles()
    indice = _a_entero(texto)

    if indice is None or not (1 <= indice <= len(productos)):
        return ["No reconocí ese número 🤔.", _texto_lista_numerada()]

    producto = productos[indice - 1]
    estado["producto_temporal"] = producto.id
    estado["paso"] = "pedido_eligiendo_cantidad"
    return [f"¿Cuántas unidades de *{producto.nombre}* querés?"]


def _manejar_cantidad(texto: str, estado: dict) -> list[str]:
    cantidad = _a_entero(texto)
    if cantidad is None or cantidad <= 0:
        return ["Decime un número válido de unidades, por favor (ej: 1, 2, 3)."]

    producto = db.session.get(Producto, estado["producto_temporal"])
    estado["carrito"].append({"producto_id": producto.id, "cantidad": cantidad})
    estado["producto_temporal"] = None
    estado["paso"] = "pedido_agregar_mas"
    return [
        f"Agregado: {cantidad}x {producto.nombre} ✅\n\n"
        "¿Querés agregar otro producto? Respondé *si* o *no*."
    ]


def _manejar_agregar_mas(texto: str, estado: dict) -> list[str]:
    if texto in {"si", "sí", "s", "1"}:
        estado["paso"] = "pedido_eligiendo_producto"
        return [_texto_lista_numerada()]

    if texto in {"no", "n", "2"}:
        estado["paso"] = "pedido_confirmando"
        return [_texto_resumen_carrito(estado["carrito"])]

    return ["Respondé *si* para agregar otro producto o *no* para continuar."]


def _texto_resumen_carrito(carrito: list[dict]) -> str:
    lineas = []
    total = 0.0
    for item in carrito:
        producto = db.session.get(Producto, item["producto_id"])
        subtotal = producto.precio * item["cantidad"]
        total += subtotal
        lineas.append(
            f"• {item['cantidad']}x {producto.nombre} — {_formatear_precio(subtotal)}"
        )

    return (
        "🧾 *Resumen de tu pedido:*\n\n"
        + "\n".join(lineas)
        + f"\n\nTotal: {_formatear_precio(total)}\n\n"
        "¿Confirmás el pedido? Respondé *confirmar* o *cancelar*."
    )


def _crear_pedido(cliente: Cliente, carrito: list[dict]) -> Pedido:
    total = 0.0
    items = []
    for entrada in carrito:
        producto = db.session.get(Producto, entrada["producto_id"])
        total += producto.precio * entrada["cantidad"]
        items.append(
            PedidoItem(
                producto_id=producto.id,
                cantidad=entrada["cantidad"],
                precio_unitario=producto.precio,
            )
        )

    pedido = Pedido(
        cliente_id=cliente.id,
        total=total,
        tiempo_estimado_minutos=randint(20, 40),
        items=items,
    )
    db.session.add(pedido)
    db.session.commit()
    return pedido


def _manejar_confirmacion(texto: str, estado: dict, cliente: Cliente) -> list[str]:
    if texto in {"confirmar", "si", "sí", "ok", "dale"}:
        pedido = _crear_pedido(cliente, estado["carrito"])
        estado["carrito"] = []
        estado["paso"] = "inicio"
        return [
            f"¡Pedido confirmado! 🎉 Número de pedido: #{pedido.id}\n"
            f"Tiempo estimado de entrega: {pedido.tiempo_estimado_minutos} minutos.\n\n"
            "Gracias por tu compra. Escribí *menu* si querés algo más."
        ]

    if texto in {"cancelar", "no"}:
        estado["carrito"] = []
        estado["paso"] = "inicio"
        return ["Pedido cancelado. Escribí *menu* para ver las opciones de nuevo."]

    return ["Respondé *confirmar* para finalizar el pedido o *cancelar* para descartarlo."]


def obtener_saludo(telefono: str) -> list[dict]:
    cliente = obtener_o_crear_cliente(telefono)
    estado = _estado_de(cliente.id)
    estado["paso"] = "inicio"
    texto = _texto_menu()
    _guardar_mensaje(cliente, texto, es_entrante=False)
    return [_empaquetar(texto)]


def obtener_historial(telefono: str) -> list[dict]:
    cliente = Cliente.query.filter_by(telefono=telefono).first()
    if cliente is None:
        return []

    mensajes = (
        Mensaje.query.filter_by(cliente_id=cliente.id).order_by(Mensaje.creado_en).all()
    )
    return [
        {
            "texto": mensaje.texto,
            "hora": mensaje.creado_en.strftime("%H:%M"),
            "es_entrante": mensaje.es_entrante,
        }
        for mensaje in mensajes
    ]


def procesar_mensaje(telefono: str, texto_usuario: str) -> list[dict]:
    cliente = obtener_o_crear_cliente(telefono)
    _guardar_mensaje(cliente, texto_usuario, es_entrante=True)

    estado = _estado_de(cliente.id)
    texto_normalizado = _normalizar(texto_usuario)

    if texto_normalizado in {"hola", "buenas", "menu", "inicio", "volver"}:
        estado["paso"] = "inicio"
        estado["carrito"] = []
        respuestas = [_texto_menu()]
    elif estado["paso"] == "pedido_eligiendo_producto":
        respuestas = _manejar_eleccion_producto(texto_normalizado, estado)
    elif estado["paso"] == "pedido_eligiendo_cantidad":
        respuestas = _manejar_cantidad(texto_normalizado, estado)
    elif estado["paso"] == "pedido_agregar_mas":
        respuestas = _manejar_agregar_mas(texto_normalizado, estado)
    elif estado["paso"] == "pedido_confirmando":
        respuestas = _manejar_confirmacion(texto_normalizado, estado, cliente)
    else:
        respuestas = _manejar_menu_principal(texto_normalizado, estado, cliente)

    for respuesta in respuestas:
        _guardar_mensaje(cliente, respuesta, es_entrante=False)

    return [_empaquetar(respuesta) for respuesta in respuestas]
