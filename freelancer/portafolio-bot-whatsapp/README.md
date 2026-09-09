# Bot de atención por WhatsApp (simulado) — Rotisería Doña Pepa

Proyecto de portafolio que simula un bot de atención al cliente por WhatsApp para un
negocio de ejemplo (una rotisería). La interfaz imita visualmente WhatsApp Web
(colores, burbujas de chat, hora en cada mensaje, indicador de "escribiendo…"),
pero **no usa la API real de WhatsApp**: es una demo funcional con backend en Flask.

## Qué hace

- Simula una conversación de atención al cliente con un flujo de toma de pedidos:
  - Saludo inicial con menú (ver catálogo / hacer pedido / consultar estado / hablar con un humano).
  - Catálogo de productos leído desde la base de datos (no hardcodeado en el texto).
  - Armado de pedido paso a paso: elegís producto, cantidad, podés agregar más
    productos, y al final confirmás con un resumen (ítems, total y tiempo estimado).
  - Consulta de estado del último pedido (en preparación / listo para retirar).
  - Historial de conversación persistido, así que si recargás la página seguís
    donde quedaste.
- Todo el intercambio de mensajes (entrantes y salientes) y los pedidos se guardan
  en una base de datos SQLite.
- La lógica de intents es simple (matching por número de opción o palabra clave),
  sin IA ni NLP — pensado como demo de automatización con reglas claras.

## Stack

- **Backend:** Python + Flask
- **Base de datos:** SQLite + SQLAlchemy (ORM, portable a PostgreSQL a futuro)
- **Frontend:** HTML + CSS + JavaScript simple (sin frameworks), fetch a la API Flask
- **Tests:** pytest sobre la lógica del bot

## Estructura del proyecto

```
portafolio-bot-whatsapp/
├── app/
│   ├── models/       # Modelos SQLAlchemy: Cliente, Producto, Pedido, PedidoItem, Mensaje
│   ├── services/      # Lógica conversacional del bot (bot.py)
│   ├── ui/            # Templates y estáticos (HTML/CSS/JS de la interfaz tipo WhatsApp)
│   └── main.py        # App Flask, rutas y seed de productos
├── tests/
│   └── test_bot.py    # Pruebas del flujo conversacional
├── capturas/           # Capturas de pantalla del chat funcionando
├── requirements.txt
└── README.md
```

## Cómo correrlo

```bash
cd portafolio-bot-whatsapp
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

python -m app.main
```

El servidor queda escuchando en **http://localhost:5001**. Al abrir la página se
genera un número de teléfono simulado (guardado en el navegador) y el bot saluda
automáticamente, como si fuera el primer contacto por WhatsApp.

Para correr los tests:

```bash
pytest
```

## Capturas

Ver carpeta `capturas/`: saludo + catálogo, armado y resumen del pedido, y
confirmación final con número de pedido y tiempo estimado.

## Descripción para el portafolio de Workana

> Demo de bot de atención automatizada vía WhatsApp, con interfaz que replica la
> experiencia de WhatsApp Web y backend real en Python (Flask + SQLAlchemy). El bot
> gestiona un flujo completo de atención: saludo, catálogo de productos, toma de
> pedidos paso a paso con carrito y confirmación, y consulta de estado — todo con
> persistencia en base de datos. Ideal como base para automatizar la atención al
> cliente de comercios (rotiserías, kioscos, y otros rubros con pedidos simples).
