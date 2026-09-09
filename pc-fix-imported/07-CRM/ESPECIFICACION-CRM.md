# Especificación de CRM

**Objetivo:** cómo se segmenta y se le hace seguimiento a la cartera de clientes.
**Estado:** Diseño completo. Se apoya directo en `08-Automatizaciones/00-MODELO-DE-DATOS.md` (tablas `clientes`, `tickets`, `eventos`).

## Segmentación automática (reglas, no opinión)

- **Cliente nuevo:** 1 ticket cerrado, sin historial previo.
- **Cliente frecuente:** 2 o más tickets en los últimos 12 meses.
- **Cliente recurrente (abono):** tiene un registro activo en la tabla `abonos` (ver `11-Finanzas/ESPECIFICACION-FINANZAS.md`).
- **Cliente inactivo:** su último ticket cerrado tiene más de 6 meses (ajustable con datos reales) y no tiene abono activo.
- **Cliente PyME/comercio:** marcado a mano al cargarlo (no todos los datos para inferirlo automático van a estar disponibles al principio).

Estas reglas se calculan con una consulta sobre `tickets` y `abonos` — no hace falta un campo manual de "segmento" que alguien tenga que actualizar y se desactualiza.

## Historial visible por cliente

Todo cliente tiene una vista única que junta: sus equipos (`equipos`), todos sus tickets con estado y fecha, y el log completo de `eventos`. Esto reemplaza tener que "acordarse" de qué se le hizo la última vez — hoy ese conocimiento vive solo en la memoria de Berenice.

## Recordatorios automáticos

- **Clientes inactivos con equipo de más de 12 meses sin mantenimiento:** disparo de un mensaje de recordatorio de mantenimiento preventivo (conecta directo con el servicio de Fase 4 marcado como diferenciador).
- **Abonos:** recordatorio antes del vencimiento del cobro mensual.
- **Garantías por vencer:** aviso interno a Berenice (no al cliente) unos días antes de que venza una garantía activa, por si conviene un contacto proactivo.

## Qué NO hace el CRM al principio

No intenta predecir nada (próxima compra, riesgo de fuga) hasta tener suficiente volumen histórico — con pocos meses de datos, un modelo predictivo daría resultados poco confiables. Se arranca con reglas simples y confiables, no con algo sofisticado y poco preciso.
