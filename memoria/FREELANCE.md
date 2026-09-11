# FREELANCE — memoria rápida

Fuente de verdad completa: `freelancer/FREELANCER_MASTER_CONTEXT.md` — no duplicar
acá el detalle, actualizarlo ahí y linkearlo. Este archivo es solo el resumen para
arrancar rápido.

## Perfil (evidencia real, no inventada)
Full Stack Developer — Django (backend "serio"/institucional) + React/Node/Postgres
(proyectos personales). 4 proyectos reales en producción (Glicemia-Calculadora y
StockFlow en uso en el Hospital Eva Perón; VI y librook con demo pública y CI/CD).
Testing exhaustivo en los 4 — es el diferencial más fuerte del perfil frente al
freelancer promedio.

## Estado por fase
- Fase 0 (Auditoría) — ✅ completa (2026-08-20)
- Fase 1 (Perfil + Employability Score, LinkedIn revivido) — ✅ completa (2026-08-21)
- Fase 2 (Job Discovery manual) — ✅ completa (2026-08-21)
- Fase 2b (Ingesta automática de ofertas: Get on Board, Remote OK, Remotive, We Work
  Remotely — filtro por relevancia, sin scraping) — ✅ completa (2026-09-09)
- Fases 3-9 (Matching Engine, Application Generator, CRM clientes, Client
  Prospecting, Analytics, Autopilot, Learning System) — **no empezadas**, se
  construyen de a una

## Oferta de servicios freelance (definida con Berenice, 2026-08-20)
5-10 hs/semana disponibles. Prioridad de clientes: PyMEs de Rosario (sinergia con PC
FIX) > instituciones > subcontratos. Mercado local/español, inglés técnico básico —
no priorizar plataformas internacionales todavía. Precio orientativo: USD 15-25/hora
para arrancar. Detalle completo en el master context, sección "Oferta de servicios".

**Alcance aclarado el 2026-09-11 — no olvidar:** lo que le sirve no es solo proyecto
freelance puntual — **también empleo part-time remoto** cuenta como oportunidad
válida. Full-time fijo/presencial no. Al filtrar o puntuar ofertas (`relevancia.py`,
futura Fase 3), no descartar algo solo por venir etiquetado
`empleo_relacion_dependencia` — revisar si es part-time/flexible antes de asumir que
no calza. Detalle en la memoria global de Claude (`freelance_alcance_busqueda.md`).

**Ingesta automática mejorada el 2026-09-11:** al revisar la bandeja con Berenice se
detectó que **ninguna de las 46 ofertas ingeridas era freelance/part-time** — no
porque no existieran, sino porque el código no leía el dato. Get on Board expone un
campo `modality` (Full time/Part time/Freelance/Internship) sin usar; Remote OK trae
tags sueltos ("part time", "contract") también sin usar. Se corrigió:
`fuentes/getonbrd.py` y `fuentes/remoteok.py` ahora resuelven ese dato y marcan
`tipo="proyecto_freelance"`; `relevancia.py` suma 20 puntos cuando ese tipo viene
confirmado por la fuente (antes solo detectaba la palabra suelta en el texto libre).
Verificado contra la API real: ~10% de los avisos de programming de Get on Board son
Part time/Freelance. 7 tests nuevos (65 en total). No hizo falta sumar ninguna fuente
externa nueva — el dato ya estaba en las 4 conectadas, solo faltaba leerlo.

## Pendientes / próximos pasos
- Definir y arrancar Fase 3 (Matching Engine) — hoy el filtro de relevancia de la
  Fase 2b es un adelanto mínimo (palabras clave), no el motor completo.
- `freelancer/notas/` tiene notas de búsqueda laboral en plataformas (Workana,
  LinkedIn) más recientes (01-sep) que no están todavía volcadas al master context —
  revisar si hay algo ahí que falte integrar.
- `freelancer/PROYECTO-CARRERA-IT/` (auditoría de GitHub repo-por-repo) quedó
  marcada como histórico — sigue teniendo valor como respaldo de evidencia para el
  CV, no como memoria activa.

## Nota técnica
`freelancer/venv/` hay que recrearlo si no existe (no se versiona) — se recreó el
2026-09-11 porque el acceso directo del escritorio no arrancaba el servidor sin él:
`python -m venv freelancer/venv` y después `freelancer/venv/Scripts/python.exe -m
pip install -r freelancer/requirements.txt`.

## Bloqueos activos
Ninguno crítico. Pendientes menores sin bloquear nada: foto de perfil de Workana (a
la espera de que Berenice la traiga), verificación de identidad de LinkedIn (requiere
el celular).
