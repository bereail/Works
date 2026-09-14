# FREELANCE — memoria rápida

Fuente de verdad completa: `freelancer/FREELANCER_MASTER_CONTEXT.md` — no duplicar
acá el detalle, actualizarlo ahí y linkearlo. Este archivo es solo el resumen para
arrancar rápido.

## 🔴 PRIORIDAD ACTIVA: sprint de 48hs para conseguir dinero YA (desde 2026-09-11)

Berenice pausó esta sesión en medio del sprint — **al retomar FREELANCE, empezar
acá, no desde cero.** Objetivo: al menos un cliente pago (ARS 100.000-300.000) lo
antes posible. No es estrategia de marca a largo plazo — es conseguir plata ahora.
Detalle completo del estado y los próximos 4 pasos exactos en la memoria global de
Claude (`freelance_sprint_generar_dinero.md`) y en
`freelancer/clientes-freelance/oportunidades-hoy.md`. Resumen:
- Ya armado y listo: oferta, 3 paquetes con precio, mensajes por canal, y 2
  propuestas concretas para avisos reales de Workana — **verificar primero si ya
  las mandó** antes de buscar algo nuevo.
- Workana y el directorio "Guía Comercial Rosario" ya se revisaron a fondo el
  2026-09-11 — no repetir esas búsquedas de entrada.
- El cuello de botella es ejecución, no investigación. El próximo canal a trabajar
  es su red personal (pedir referidos a 5-10 contactos) — no requiere más
  investigación, solo armar la lista con ella y el mensaje.

## Dos patas distintas dentro de FREELANCE — no mezclar (aclarado 2026-09-11)

Berenice separó explícitamente el objetivo de "conseguir ingresos" en tres negocios
(`memoria/ESTADO_ACTUAL.md` tiene el mapa completo): PC FIX, **buscar trabajo como
programadora** (empleo/part-time — lo que hace `freelancer/app/`, la ingesta
automática de ofertas) y **trabajos freelance** (clientes que pagan por un servicio
puntual — carpeta nueva `freelancer/clientes-freelance/`). Son objetivos y públicos
distintos: uno busca que la contraten, el otro busca clientes que le paguen un
trabajo chico. No mezclar el contenido de uno con el del otro.

**Corrección importante, para siempre (2026-09-11):** PC FIX (reparación de PC y
hardware) y FREELANCE (programación de software) son **dos negocios completamente
distintos**, con público distinto. Nunca sugerir que los clientes de PC FIX son una
fuente de leads para trabajos freelance de software, ni al revés — Berenice lo
corrigió de forma tajante después de que se propusiera justo eso. El
`FREELANCER_MASTER_CONTEXT.md` todavía menciona una "sinergia con PCfix" de una
estrategia anterior (2026-08-20) — quedó desactualizada, corregir ahí la próxima vez
que se edite ese archivo. Detalle en la memoria global de Claude
(`pcfix_y_freelance_no_se_mezclan.md`).

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

## Oferta de servicios freelance (definida con Berenice, 2026-08-20; prioridad de
## clientes corregida el 2026-09-11 — ver nota arriba, PC FIX no es fuente de leads)
5-10 hs/semana disponibles. Prioridad de clientes: PyMEs de Rosario > instituciones >
subcontratos. Mercado local/español, inglés técnico básico — no priorizar
plataformas internacionales todavía. Precio orientativo: USD 15-25/hora para
arrancar. Detalle completo en el master context, sección "Oferta de servicios".

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

## Captación de clientes freelance — sprint de 48hs (arrancado 2026-09-11)
Objetivo puntual de Berenice: conseguir cliente(s) pagos por ARS 100.000-300.000 en
48hs, con trabajos chicos (bugs, mantenimiento, mejoras, deploy) — no construir un
producto nuevo. Estrategia completa (oferta, 3 paquetes con precio, propuesta de
valor, mapeo de qué proyecto mostrar según lo que pida el cliente, y a quién
contactar) en `freelancer/clientes-freelance/ESTRATEGIA-48HS.md`. Textos listos por
canal (WhatsApp, Instagram, LinkedIn, Workana) en
`freelancer/clientes-freelance/mensajes-contacto.md`. Todo basado solo en los 4
proyectos reales y las 3 piezas de portafolio ya existentes — nada inventado.
Ejecución (mandar mensajes de verdad) queda en manos de Berenice; próxima sesión
sobre esto: revisar qué canal tuvo respuesta y ajustar.

## Sección "Postulaciones" (agregada 2026-09-14)
Nueva pantalla en `http://127.0.0.1:8002/postulaciones` (ruta `GET /postulaciones` en
`freelancer/app/ui/routers/freelancer.py`, plantilla
`freelancer_postulaciones.html`): junta todo lo que está en bandeja o marcado
"por postular" (estados `nueva`/`por_postular`), ordenado por puntaje, con un botón
grande **"🚀 Postularme →"** que abre el aviso original en una pestaña nueva —
Berenice se postula ahí, la app no postula sola, solo lleva la cuenta ("Ya me
postulé" marca el estado). Al pie suma **5 accesos directos de búsqueda manual**
(Computrabajo, Bumeran, ZonaJobs, LinkedIn Jobs, Indeed Argentina) con URLs de
búsqueda ya armadas para su perfil (full stack, Django/React, remoto) —
**no son fuentes de ingesta automática**, esos portales no tienen API pública y el
proyecto explícitamente no scrapea lo que los términos de cada plataforma prohíben
(mismo criterio que las 4 fuentes ya conectadas). El home (`freelancer.html`) ahora
enlaza primero a `/postulaciones` y aparte a `/ofertas` (historial completo, todos
los estados). Se corrió la ingesta de las 4 fuentes ese día: 0 ofertas nuevas, pero
quedaron 39 en bandeja sin revisar de corridas previas, visibles ya en
`/postulaciones`.

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
