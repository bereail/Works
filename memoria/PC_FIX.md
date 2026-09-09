# PC FIX — memoria rápida

Detalle completo: `pc-fix/00-Estrategia/00-ROADMAP.md` (roadmap por etapa) y
`pc-fix/README.md` (mapa de carpetas). Este archivo es solo el resumen para arrancar
rápido — no duplicar acá el detalle, actualizarlo ahí y linkearlo.

## Estado por etapa (ver roadmap para el detalle)

1. Auditoría integral (FODA) — ✅ completo
2. Análisis de mercado Rosario — ✅ completo
3. Posicionamiento de marca — ✅ completo
4. Catálogo de servicios y rentabilidad — ✅ completo
5. Procedimientos operativos — 🔜 próxima etapa a ejecutar
6. Automatizaciones (diseño + infraestructura) — ✅ diseño y decisiones listas,
   **implementación real en curso** (ver más abajo)
7. Web + SEO — ⏸ en pausa por decisión propia
8. Redes sociales (plan de contenidos) — ✅ completo, 1 publicación/semana
9. CRM, finanzas, inventario, dashboard — ✅ diseño completo, listo para implementar
10. Publicidad paga — ⏸ en pausa, presupuesto $0

## Decisiones de infraestructura ya resueltas (5 ago 2026)
1-5 hs/semana disponibles · dominio `ailonline.com.ar/pcfix` · hosting en PC propia ·
WhatsApp con Evolution API self-hosted · sin monotributo todavía (números internos,
no oficiales) · $0 de presupuesto de ads · atención en punto fijo (Olive 1200,
Rosario — *pendiente confirmar si coincide con Meta Business*). Detalle:
`pc-fix/00-Estrategia/DECISIONES-PENDIENTES.md`.

## El sistema de automatización de contenido — YA EXISTE

El objetivo de "Claude genera → Berenice aprueba → se publica" **ya está construido**,
no es un proyecto nuevo a arrancar de cero:
- `pc-fix/app/agents/agente_negocio.py` — genera copy y flyer, deja la publicación en
  estado `previsualizado`, un solo click para confirmar.
- Diseño de 3 agentes (Atención / Contenido / Análisis) en
  `pc-fix/13-IA/AGENTES-DE-IA.md` — el de Contenido nunca publica solo.
- **En curso al 2026-09-09** (trabajo sin commitear rescatado en la reorganización del
  repo): integración con Meta API (`app/services/meta_api.py`, migraciones alembic
  para credenciales de cuentas) — falta confirmar si ya está conectada de verdad o
  solo el scaffolding.

## Pendientes / próximos pasos
- Etapa 5 (procedimientos operativos): documentar el flujo recepción → entrega antes
  de automatizarlo del todo.
- Confirmar dirección de atención al público (Olive 1200 vs 1300 en Meta Business) —
  pendiente menor en `pc-fix/17-Backlog/IDEAS-PENDIENTES.md`.
- Confirmar estado real de la integración Meta API (recién rescatada del trabajo sin
  commitear, no verificada en esta sesión).
- Contenido/borradores sueltos que vivían en la raíz de `Works` ahora están en
  `pc-fix/contenido/` — revisar si siguen vigentes o ya se publicaron.

## Bloqueos activos
Ninguno crítico.
