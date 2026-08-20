# Especificación de Dashboard

**Objetivo:** un panel único con las métricas que importan, calculadas sobre datos reales de `clientes`, `tickets`, `eventos`, `transacciones`, `abonos` y `productos`.
**Herramienta propuesta:** Grafana leyendo directo de PostgreSQL — es open source, ya está en el stack elegido, y evita construir un dashboard a medida desde cero.
**Estado:** Diseño completo.

## Métricas agrupadas por bloque

**Adquisición**
- Cantidad de consultas (por semana/mes) — de `tickets` con `fecha_creacion`.
- Origen de clientes — de `canal_origen`.
- Conversión (consulta → ticket aceptado) — `tickets aceptados / tickets creados`.
- Tiempo de respuesta — de `eventos`, diferencia entre mensaje entrante y primera respuesta.

**Operación**
- Tiempo promedio de reparación — de `eventos`, diferencia entre `en_reparacion` y `listo`.
- Tiempo promedio de cierre — de `eventos`, diferencia entre `recibido` y `entregado`.
- Servicios más vendidos — de `transacciones`, agrupado por `categoria`.

**Plata**
- Ingresos diarios / mensuales — de `transacciones` tipo ingreso.
- Ganancia mensual y ganancia por servicio — de `transacciones` (ver fórmula en `11-Finanzas/ESPECIFICACION-FINANZAS.md`).
- Servicios recurrentes activos (MRR) — de `abonos` con `estado = activo`.

**Clientes**
- Clientes nuevos vs. frecuentes vs. inactivos vs. recuperados — de las reglas de `07-CRM/ESPECIFICACION-CRM.md`.
- Valor de vida del cliente (LTV) — suma histórica de ingresos por `cliente_id`.

## Qué es medible desde el día uno y qué necesita tiempo

**Desde el primer ticket cargado:** consultas, conversión, tiempo de respuesta, tiempo de reparación, ingresos, servicios más vendidos.

**Recién con varios meses de datos:** clientes inactivos/recuperados (necesita historial), LTV real (necesita ver el comportamiento repetido), y cualquier comparación mes a mes o de tendencia.

**Bloqueado hasta la Etapa 10 (publicidad paga):** costo por cliente (CAC) y ROI/publicidad más efectiva — no se puede calcular el retorno de una inversión que todavía no existe. El dashboard deja el lugar preparado para esos indicadores, pero van a estar vacíos hasta que haya gasto de pauta real que medir.

## Por qué Grafana y no un dashboard hecho a medida

Construir un dashboard propio desde cero es reinventar algo que Grafana ya resuelve bien, y suma una pieza más de software para mantener sin necesidad. Grafana conectado directo a Postgres muestra estos números con paneles ya probados, y deja lugar para sumar Prometheus/Uptime Kuma más adelante si hace falta monitorear la salud del propio sistema de automatización (que las automatizaciones de la Etapa 6 sigan funcionando), no solo las métricas del negocio.
