# Roadmap maestro — PC Fix

Última actualización: 5 de agosto de 2026.

Regla de avance: cada fase se ejecuta sin pedir autorización, salvo que dependa de gastar dinero, crear una cuenta nueva, o comprometer algo legal/fiscal — esos puntos quedan listados en `DECISIONES-PENDIENTES.md` y bloquean solo las fases que dependen de ellos, no el resto.

---

## Etapa 1 — Auditoría integral del negocio
- **Objetivo:** entender el punto de partida real (no el ideal) antes de diseñar nada.
- **Prioridad:** crítica.
- **Tiempo estimado:** 1 sesión.
- **Impacto esperado:** evita construir estrategia sobre supuestos falsos.
- **Checklist:** situación actual ✔ · fortalezas ✔ · debilidades ✔ · oportunidades ✔ · amenazas ✔
- **Dependencias:** ninguna.
- **Estado:** ✅ Completo — ver `FASE-1-AUDITORIA-FODA.md`.
- **Resultado esperado:** FODA profundo y específico de PC Fix, no genérico.

## Etapa 2 — Análisis de mercado (Rosario, Santa Fe)
- **Objetivo:** mapear competencia real, precios, demanda y huecos de mercado.
- **Prioridad:** crítica.
- **Tiempo estimado:** 1 sesión.
- **Impacto esperado:** define en qué nichos competir y en cuáles no.
- **Checklist:** competencia relevada ✔ · precios de referencia ✔ · nichos identificados ✔ · servicios rápidos vs. premium vs. recurrentes ✔
- **Dependencias:** Etapa 1.
- **Estado:** ✅ Completo — ver `FASE-2-ANALISIS-MERCADO-ROSARIO.md`.
- **Resultado esperado:** lista priorizada de oportunidades reales, con evidencia.

## Etapa 3 — Posicionamiento de marca
- **Objetivo:** definir por qué PC Fix gana sin competir por precio.
- **Prioridad:** crítica.
- **Tiempo estimado:** 1 sesión.
- **Impacto esperado:** todo el copy, diseño y ventas futuras se apoyan en esto.
- **Checklist:** pilares de posicionamiento ✔ · tagline ✔ · qué NO se va a hacer ✔
- **Dependencias:** Etapas 1 y 2.
- **Estado:** ✅ Completo — ver `../01-Marca/FASE-3-POSICIONAMIENTO.md`.
- **Resultado esperado:** un párrafo que cualquier persona del equipo (aunque el equipo sea de una sola persona) pueda usar para decidir "¿esto es on-brand o no?".

## Etapa 4 — Catálogo de servicios y rentabilidad
- **Objetivo:** decidir qué se ofrece, en qué orden, y qué tan rentable es cada cosa.
- **Prioridad:** crítica.
- **Tiempo estimado:** 1 sesión.
- **Impacto esperado:** evita construir automatización para servicios que no convienen.
- **Checklist:** catálogo completo evaluado ✔ · margen estimado por servicio ✔ · prioridad de lanzamiento ✔
- **Dependencias:** Etapas 1, 2 y 3.
- **Estado:** ✅ Completo — ver `../01-Marca/FASE-4-CATALOGO-SERVICIOS.md`.
- **Resultado esperado:** catálogo de servicios con semáforo de prioridad.

## Etapa 5 — Procedimientos operativos
- **Objetivo:** documentar el flujo recepción → diagnóstico → presupuesto → reparación → entrega → garantía → reseña, antes de automatizarlo.
- **Prioridad:** alta.
- **Tiempo estimado:** 1–2 sesiones.
- **Impacto esperado:** sin este paso, automatizar es automatizar el caos.
- **Checklist:** manual por etapa del flujo · criterios de calidad · política de garantía.
- **Dependencias:** Etapa 4.
- **Estado:** 🔜 Próxima fase automática.
- **Resultado esperado:** manuales en `14-Procedimientos/`.

## Etapa 6 — Diseño de automatizaciones (especificación)
- **Objetivo:** diseñar en papel cada automatización (CRM, WhatsApp, seguimiento, presupuestos) antes de tocar infraestructura.
- **Prioridad:** alta.
- **Tiempo estimado:** 2–3 sesiones.
- **Impacto esperado:** especificación lista para implementar apenas se resuelvan las decisiones pendientes de infraestructura.
- **Checklist:** diagrama de flujo por automatización ✔ · datos que mueve ✔ · disparadores ✔ · herramienta propuesta ✔
- **Dependencias:** Etapa 5 + decisión de stack (ver `DECISIONES-PENDIENTES.md`).
- **Estado:** ✅ Diseño completo, ✅ decisiones de infraestructura resueltas (5 ago 2026: PC propia + Evolution API). **Listo para implementación real** — ver `08-Automatizaciones/00-MODELO-DE-DATOS.md`, `01-AUTOMATIZACIONES-CORE.md` y `13-IA/AGENTES-DE-IA.md`. Con 1-5 hs/semana disponibles (decisión #1), la Automatización 1 (triage de WhatsApp) es la de mayor prioridad real.

## Etapa 7 — Web + SEO (especificación y contenidos)
- **Objetivo:** arquitectura del sitio, estructura SEO, textos de páginas de servicio.
- **Prioridad:** media (bajada por Berenice el 5 ago 2026 — no es foco de corto plazo).
- **Tiempo estimado:** 2–3 sesiones.
- **Dependencias:** Etapa 4 (catálogo). Dominio ya definido: `ailonline.com.ar/pcfix` (ver `DECISIONES-PENDIENTES.md`, punto 2).
- **Estado:** ⏸ En espera — se retoma cuando Berenice lo indique. Mientras tanto se avanza con Etapa 8.

## Etapa 8 — Redes sociales (plan de contenidos)
- **Objetivo:** calendario, pilares de contenido, formatos por red.
- **Prioridad:** media-alta.
- **Tiempo estimado:** 1–2 sesiones.
- **Checklist:** pilares de contenido ✔ · formatos por red ✔ · cadencia ajustada al tiempo real disponible (decisión #1) ✔ · calendario del primer mes ✔
- **Dependencias:** Etapa 3.
- **Estado:** ✅ Completo — ver `../05-Redes/PLAN-DE-CONTENIDOS.md`. Cadencia bajada a 1 publicación/semana (7 ago 2026) tras resolverse la decisión #1. Dos ideas de contenido quedaron en `17-Backlog/IDEAS-PENDIENTES.md` hasta que la Etapa 6 esté desplegada.

## Etapa 9 — CRM, finanzas, inventario y dashboard (especificación)
- **Objetivo:** modelo de datos y métricas antes de elegir herramienta.
- **Prioridad:** media.
- **Tiempo estimado:** 2 sesiones.
- **Checklist:** segmentación de clientes ✔ · tablas de finanzas y fórmula de rentabilidad ✔ · tablas de inventario y alertas ✔ · métricas de dashboard mapeadas a Grafana ✔
- **Dependencias:** Etapa 6.
- **Estado:** ✅ Diseño completo, ✅ decisiones resueltas. Listo para implementación real — ver `07-CRM/ESPECIFICACION-CRM.md`, `11-Finanzas/ESPECIFICACION-FINANZAS.md`, `10-Inventario/ESPECIFICACION-INVENTARIO.md`, `12-Dashboard/ESPECIFICACION-DASHBOARD.md`. Nota: sin monotributo (decisión #5), los números de Finanzas son de uso interno/estimativo, no oficiales.

## Etapa 10 — Publicidad paga
- **Objetivo:** campañas Google/Meta Ads.
- **Prioridad:** media (no crítica al inicio — primero orgánico y boca en boca profesionalizado).
- **Dependencias:** presupuesto de pauta + cuenta comercial de Meta verificada (hoy restringida, ver memoria del proyecto de Instagram).
- **Estado:** ⏸ En pausa por decisión propia (5 ago 2026: presupuesto definido en $0, foco 100% orgánico). No es un bloqueo externo — se retoma si en algún momento aparece presupuesto real.

---

### Convenciones de estado
✅ Completo · 🔜 Próxima automática · ⏸ Diseñable ya, ejecución condicionada · 🚫 Bloqueada por decisión externa
