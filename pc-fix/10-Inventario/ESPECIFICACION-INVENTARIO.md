# Especificación de Inventario

**Objetivo:** stock, alertas, proveedores y costos — acotado a lo que hoy realmente se vende (SSD, RAM, accesorios), sin sobre-diseñar para un catálogo de hardware que todavía no existe.
**Estado:** Diseño completo.

## Tablas nuevas

**productos**
`id, nombre, categoria (ssd/ram/accesorio/otro), costo_unitario, precio_venta, stock_actual, stock_minimo`

**movimientos_stock**
`id, producto_id, tipo (compra/venta/ajuste), cantidad, fecha, ticket_id (opcional, si la venta fue parte de un trabajo)`

**proveedores**
`id, nombre, contacto, productos_que_provee, tiempo_entrega_estimado`

## Alertas automáticas

- `stock_actual <= stock_minimo` → aviso a Berenice para reponer, antes de quedarse sin stock en medio de un trabajo aceptado.
- Sin movimiento de un producto en X meses → aviso de revisión (puede ser un producto que conviene dejar de tener inmovilizado).

## Rentabilidad por producto

`(precio_venta − costo_unitario) / precio_venta` por producto — permite ver rápido qué conviene mantener en stock y qué conviene vender solo por pedido puntual (sin inmovilizar plata en algo de rotación baja).

## Por qué acotado y no un inventario completo de "hardware store"

El catálogo de Fase 4 marcó la venta de hardware como **complemento, no foco** (margen bajo-medio, sensible al dólar). Un sistema de inventario grande, con múltiples depósitos o control de series, sería una automatización sin negocio real detrás — se diseña lo justo para no perder plata por falta de control, no más que eso. Si en el futuro la venta de hardware crece como línea de negocio propia, este módulo se extiende recién ahí.
