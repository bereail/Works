# Especificación de Finanzas

**Objetivo:** caja, ingresos, gastos, rentabilidad y flujo de caja — con datos reales, no estimados de memoria.
**Estado:** Diseño completo. La utilidad real de este módulo depende de resolver la situación fiscal (`DECISIONES-PENDIENTES.md`, punto 5) — se puede construir igual, pero "ingresos" solo va a ser un número confiable si se carga con disciplina desde el día uno.

## Tablas nuevas (extienden el modelo base)

**transacciones**
`id, tipo (ingreso/egreso), monto, fecha, categoria (mano_obra/venta_hardware/abono/insumo/herramienta/otro), ticket_id (opcional, si está ligado a un trabajo puntual), descripcion`

**abonos**
`id, cliente_id, plan (particular/pyme), monto_mensual, fecha_inicio, estado (activo/pausado/cancelado), fecha_ultimo_cobro`

## Cómo se calcula la rentabilidad por ticket

`ingreso_ticket (de transacciones tipo ingreso ligadas al ticket) − costo_insumos (transacciones tipo egreso, categoría insumo, ligadas al ticket) = margen_ticket`

El tiempo propio de Berenice **no** se descuenta como costo en pesos (es autoempleo, no un sueldo a pagar) — pero sí se registra el tiempo insumido por ticket (ya está en `eventos` por las marcas de tiempo de cada cambio de estado) para calcular rentabilidad por hora más adelante, que es la métrica que de verdad importa para decidir qué servicios priorizar con tiempo limitado (Fase 1).

## Flujo de caja

Simplemente `suma(transacciones ingreso) − suma(transacciones egreso)` agrupado por semana/mes. No hace falta nada más sofisticado al tamaño actual del negocio — un sistema de flujo de caja proyectado (con cuentas por cobrar, plazos, etc.) recién tiene sentido cuando haya varios abonos mensuales activos y volumen suficiente para que la proyección aporte algo que no se ve a simple vista.

## Categorías de gasto mínimas para no perder trazabilidad

`insumo (SSD, RAM, repuestos) · herramienta (equipamiento propio) · transporte · marketing/publicidad · hosting/software · otro`

Esto es lo que después permite responder cosas como "¿cuánto gasté en insumos este mes vs. cuánto facturé por venta de hardware?" — la comparación que valida o refuta la regla de rentabilidad de Fase 4 (mano de obra > reventa de insumos).

## Qué mide esto que hoy no se mide

Ganancia por servicio, ticket promedio real (no estimado), y si el negocio de venta de hardware realmente aporta margen o solo mueve plata sin dejar ganancia real — algo que hoy es imposible de saber sin este registro.
