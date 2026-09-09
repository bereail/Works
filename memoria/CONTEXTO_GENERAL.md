# Contexto general — Works

## Qué es este repositorio

`Works` es el repositorio único de Berenice Solohaga que contiene **dos negocios
independientes** más la memoria compartida entre ambos. Vive en
`C:\Users\bsolohaga\Desktop\bere\GIT\Works`, se sincroniza con
`github.com/bereail/Works` (repo **público**), y es la fuente de verdad que permite
retomar el trabajo desde cualquiera de sus dos computadoras sin volver a explicar
contexto.

## Los dos negocios

### PC FIX (`pc-fix/`)
Servicio técnico de PCs en Rosario, Santa Fe: reparación, mantenimiento, diagnóstico,
venta de insumos, marketing, contenido para Instagram/Facebook. Objetivo actual:
automatizar al máximo la generación de contenido de redes (Claude genera → Berenice
aprueba → se publica), sin sacrificar el criterio técnico que diferencia a la marca.
Mapa completo de carpetas en `pc-fix/README.md`. Memoria rápida: `memoria/PC_FIX.md`.

### FREELANCE (`freelancer/`)
La carrera de Berenice como desarrolladora Full Stack (Django + React/Node):
perfil de GitHub/LinkedIn, portfolio, oferta de servicios freelance, búsqueda laboral
activa y sistema propio de ingesta de ofertas. Fuente de verdad:
`freelancer/FREELANCER_MASTER_CONTEXT.md`. Memoria rápida: `memoria/FREELANCE.md`.

## Cómo se activa cada contexto

Si el mensaje empieza con o es exactamente **"PC FIX"** → activar contexto PC FIX,
leer `memoria/PC_FIX.md` y responder con estado, última actividad, pendientes y
próximo paso. Igual con **"FREELANCE"**. Nunca mezclar ambos en la misma respuesta.

## Estructura del repo

```
Works/
├── CLAUDE.md                  ← reglas de comportamiento de este repo
├── .gitignore                 ← venv/, *.db, *.log, .clave_sesion, etc.
├── memoria/
│   ├── CONTEXTO_GENERAL.md    ← este archivo
│   ├── ESTADO_ACTUAL.md       ← memoria rápida, leer siempre primero
│   ├── PC_FIX.md
│   └── FREELANCE.md
├── historial/
│   └── decisiones.md          ← decisiones que cruzan ambos negocios o el repo en sí
├── pc-fix/                    ← negocio 1 (antes repo git independiente, aplanado
│                                  el 2026-09-09 — conserva su historial de 15 commits)
│   ├── 00-Estrategia/ … 18-Reportes/   ← roadmap, FODA, especificaciones
│   ├── app/                   ← sistema real: FastAPI + agentes de generación de contenido
│   └── contenido/             ← borradores y flyers sueltos (movidos acá el 2026-09-09)
└── freelancer/                ← negocio 2 (antes repo git independiente, aplanado
                                   el 2026-09-09 — conserva su historial)
    ├── FREELANCER_MASTER_CONTEXT.md   ← fuente de verdad activa
    ├── PROYECTO-CARRERA-IT/           ← auditoría detallada de GitHub (histórico)
    ├── portafolio-*/                  ← 3 proyectos de portfolio (bot WhatsApp,
    │                                     dashboard, integración CRM)
    ├── app/                           ← sistema real: ingesta automática de ofertas
    └── notas/                         ← notas sueltas (movidas acá el 2026-09-09)
```

## Cosas importantes que no son obvias leyendo el código

- `pc-fix/` y `freelancer/` corren como apps FastAPI locales, cada una con su propia
  base de datos SQLite y clave de sesión — esos archivos están gitignorados a
  propósito (son estado, no código) y siguen viviendo físicamente en esas carpetas.
- Dos carpetas con **datos reales de infraestructura hospitalaria** (backup de git
  pre-limpieza de stockTonerDesktop + capturas viejas) se sacaron por completo del
  repo el 2026-09-09 y quedaron en
  `C:\Users\bsolohaga\Desktop\bere\_respaldos-locales-fuera-de-git\` — **nunca deben
  volver a entrar a este repo ni a ningún repo público**. Ver `historial/decisiones.md`.
- Antes del 2026-09-09 este repo tenía `freelancer/` y `pc-fix/` como repos git
  independientes sin remoto propio — el `git pull`/`git push` no los traía. Eso ya
  está resuelto (ver `historial/decisiones.md`), pero si en algún momento aparece de
  nuevo una carpeta con `.git` adentro de `pc-fix/` o `freelancer/`, es una señal de
  que algo se rompió.
