# Modelo de datos base — PC Fix

**Objetivo:** el esqueleto de datos mínimo del que dependen todas las automatizaciones de esta etapa. Se implementa en PostgreSQL cuando se resuelva la decisión de hosting (`DECISIONES-PENDIENTES.md`, punto 3). Hasta entonces es una especificación, no código corriendo.

No es el modelo final del CRM (eso se cierra en Etapa 9 con más volumen real de datos) — es lo mínimo para que las automatizaciones de esta etapa tengan dónde leer y escribir.

## Tablas

**clientes**
`id, nombre, telefono, canal_contacto (whatsapp/instagram/facebook/referido), fecha_alta, notas`

**equipos**
`id, cliente_id, tipo (pc/notebook/otro), marca, modelo, numero_serie (opcional)`

**tickets**
`id, cliente_id, equipo_id, estado, sintoma_reportado, diagnostico, presupuesto_monto, presupuesto_detalle, canal_origen, fecha_creacion, fecha_ultimo_cambio_estado`

Valores posibles de `estado` (coinciden 1 a 1 con el manual de flujo operativo, `14-Procedimientos/MANUAL-FLUJO-OPERATIVO.md`):
`recibido → en_diagnostico → presupuestado → aceptado → en_reparacion → control_calidad → listo → entregado → en_garantia → cerrado`

**eventos**
`id, ticket_id, tipo (mensaje_whatsapp/nota_interna/cambio_estado/llamada), contenido, fecha, origen (cliente/berenice/automatico)`
Es el log completo de todo lo que le pasó a un ticket — de acá sale después cualquier métrica de tiempo de respuesta o tiempo de reparación (Etapa 9).

**garantias**
`id, ticket_id, fecha_inicio, fecha_vencimiento, alcance_texto`

**reseñas**
`id, cliente_id, ticket_id, fecha_pedido, respondida (si/no), resultado (positivo/negativo/sin respuesta)`

## Por qué este diseño y no otro

- Todo cuelga de `ticket_id`, no de `cliente_id` — porque un mismo cliente puede tener varios equipos y varios trabajos, y las métricas de negocio (tiempo de reparación, ticket promedio, servicios más vendidos) se miden por ticket, no por cliente.
- `eventos` es un log de solo-agregar (append-only) — nunca se edita ni se borra un evento pasado. Es lo que permite auditar después "qué pasó realmente" sin depender de la memoria de nadie.
- Nombres de tablas y estados en español y en criollo, no en inglés técnico — el sistema lo va a leer y ajustar la propia Berenice, no un equipo de desarrollo tercero.
