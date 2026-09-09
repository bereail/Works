# Panel de Reportes de Ventas — NovaShop

Dashboard web de reportes de ventas para una tienda online ficticia, construido como
pieza de portafolio para demostrar habilidades de scripting, automatización de
reportes y visualización de datos con Python.

## Qué hace

- Muestra KPIs clave: total de ventas, ticket promedio, cantidad de pedidos y
  producto más vendido del período.
- Grafica la evolución de ventas en el tiempo (por día o por semana, según el
  período elegido) y la participación de cada categoría de producto.
- Lista el top de productos más vendidos, con unidades y monto facturado.
- Permite filtrar todo el panel por período (últimos 30 días, últimos 90 días o
  todo el histórico) sin recargar manualmente: el filtro recalcula KPIs, gráficos
  y tabla contra los mismos datos.
- Incluye modo claro/oscuro con paleta validada para contraste y daltonismo,
  tooltips interactivos en los gráficos y una vista en tabla alternativa para
  accesibilidad.
- Los datos surgen de una base SQLite real (no están hardcodeados en el HTML):
  ~6 meses de historial simulado, con estacionalidad semanal, tendencia de
  crecimiento y días de promoción con picos de ventas.

## Stack

- **Backend:** Python + Flask
- **Base de datos:** SQLite, con SQLAlchemy (Flask-SQLAlchemy) como ORM —
  pensado para poder migrar a PostgreSQL sin reescribir consultas
- **Frontend:** HTML + CSS propio (sin frameworks JS pesados) y Chart.js vía CDN
  para los gráficos
- **Datos de ejemplo:** script de seed propio (`seed.py`) que genera el histórico

## Estructura del proyecto

```
portafolio-dashboard-reportes/
├── app/
│   ├── models/       # Categoria, Producto, Cliente, Pedido, DetallePedido
│   ├── services/     # reportes.py: KPIs, series y agregaciones
│   ├── ui/           # templates y estáticos (CSS/JS) del dashboard
│   └── main.py       # rutas Flask
├── seed.py           # genera la base de datos con datos de ejemplo
├── requirements.txt
└── capturas/         # screenshots del dashboard funcionando
```

## Cómo correrlo

```bash
pip install -r requirements.txt
python seed.py              # genera datos.db con ~6 meses de ventas simuladas
python -m app.main          # levanta el servidor en http://localhost:5002
```

El servidor corre con `app.run(port=5002)`. Para volver a generar los datos
desde cero (por ejemplo, para simular otro período) simplemente se vuelve a
correr `python seed.py`: recrea las tablas y las puebla de nuevo.

## Para el portafolio de Workana

> Dashboard de reportes de ventas desarrollado en Python (Flask + SQLAlchemy),
> conectado a una base de datos real con seis meses de historial. Incluye KPIs
> del período, gráficos de evolución de ventas y de participación por categoría,
> un ranking de productos más vendidos y filtros por rango de fechas que
> recalculan todos los indicadores al instante. Pensado para automatizar la
> lectura de métricas de un negocio online sin depender de planillas manuales.
