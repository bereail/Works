> ⚠️ **HISTÓRICO — superado por `freelancer/FREELANCER_MASTER_CONTEXT.md` desde el
> 2026-08-20.** Este archivo documenta la auditoría de GitHub (Etapa 1 del plan
> original de 8 etapas). Esa auditoría ya está resumida y absorbida en el master
> context actual. Se conserva como detalle histórico de cómo se llegó a esas
> conclusiones — no leer esto como el estado actual del proyecto.

# MEMORIA DEL PROYECTO — Carrera IT de Berenice

> Este archivo se lee PRIMERO al retomar el proyecto. Contiene el estado exacto para poder
> continuar sin volver a explicar nada. Se actualiza al cierre de cada sesión de trabajo.

## Objetivo general
Preparar el perfil profesional de Berenice para conseguir trabajo como desarrolladora.
Ver `00-CONTEXTO/OBJETIVO-FINAL.md` y `00-CONTEXTO/CONTEXTO-PROYECTO.md`.

## Etapa actual
**Etapa 1 de 8: GitHub.** No avanzar a CV/Portfolio/LinkedIn/búsqueda laboral hasta cerrarla.

## 🎯 FOCO ACTUAL (redefinido 2026-08-11)
Berenice decidió que **los únicos repos que quiere públicos en su GitHub son 4**:
**Glicemia-Calculadora, stockTonerDesktop, VI, librook.** Todo el resto del inventario queda
privado (ya se aplicó: Arbolada y Portfolio-Rodrigo pasados a privado en esta sesión, sumados a
los que ya estaban privados de antes — statuapp, Bebi, DB2, ail, HostingAilonline,
plan-de-escape, Portfolio, y los huérfanos/duplicados).

El objetivo es dejar estos 4 repos "1000% presentables para conseguir trabajo" — máxima
prioridad, dedicarles todo el esfuerzo de pulido (código, README, tests, screenshots, demo).
El resto del roadmap original (Arbolada, dnt-web, Portfolio-Rodrigo, etc.) queda en pausa
indefinida salvo que Berenice pida retomarlo.

**Orden de trabajo de los 4 — TODOS COMPLETOS (2026-08-13):**
1. Glicemia-Calculadora — ✅ hecho (89/100)
2. stockTonerDesktop — ✅ hecho (85/100)
3. VI — ✅ hecho (90/100)
4. librook — ✅ hecho. Pusheado (commits `2fd6e9c` y `81ddbeb`).

🎯 **Los 4 repos objetivo quedaron cerrados.** Falta decidir con Berenice el próximo paso:
retomar el roadmap original en pausa (Arbolada, dnt-web, Portfolio-Rodrigo) o pasar a la
Etapa 2 (CV profesional).

## Etapa siguiente
Etapa 2: CV profesional (no iniciar todavía).

## Repositorios: estado de revisión

| Repo | Estado | Nivel | Notas |
|---|---|---|---|
| Glicemia-Calculadora | 🟢 LISTO PARA PORTFOLIO (89/100) | A | Ver `02-REPOSITORIOS/Glicemia-Calculadora/AUDITORIA.md` |
| statuapp | 🟡 Mejoras pusheadas, pasado a PRIVADO hasta resolver Netlify (74/100) | A | Ver `02-REPOSITORIOS/statuapp/AUDITORIA.md` |
| VI | 🟢 LISTO PARA PORTFOLIO (90/100) | A | Ver `02-REPOSITORIOS/VI/AUDITORIA.md` |
| librook | 🟢 LISTO PARA PORTFOLIO | A | Feature Community + README + capturas. Pusheado |
| dnt-web | ⚪ Pendiente | B | Stack moderno, README básico |
| Portfolio-Rodrigo | ⏸️ Pausado, pasado a PRIVADO | B | Fuera del foco de los 4 repos objetivo |
| Arbolada | ⏸️ Pausado, pasado a PRIVADO | B | Fuera del foco de los 4 repos objetivo |
| stockTonerDesktop | 🟢 LISTO PARA PORTFOLIO (85/100), sigue privado | A | Ver `02-REPOSITORIOS/stockTonerDesktop/AUDITORIA.md` |
| Bebi | ⚪ Pendiente | D→? | 🔴 Bloqueado: `venv/` trackeado (6764 archivos) + sospecha de secretos en historial pasado |
| DB2 | ⚪ Pendiente | C | Contenido de facultad, no destacar |
| ail | ⚪ Pendiente | D | Sin README, estructura confusa |
| HostingAilonline | ⚪ Pendiente | D | README default, un solo commit de 2025 |
| Portfolio | ⚪ Pendiente | D? | Aclarar propósito (¿sitio comercial o portfolio de código?) |
| plan-de-escape | ⚪ Pendiente | D? | Aclarar de qué se trata |

Detalle completo de la clasificación y el porqué: `01-GITHUB/AUDITORIA-GITHUB.md`.

## Repositorios NO auditados aún (fuera de la carpeta GIT/ con git)
`chatBot`, `PropuestaFichaArcade`, `Test` (sin `.git`, a definir qué son).

## Repos huérfanos en GitHub (sin carpeta local)
`zkteco-f22`, `gameRos`, `Glicemia-Version-Estable`, `alboradaClaude`, `CasinoFlor`,
`Glicemia-CalculadoraNew`, `movieApp`, `ReadMe-Fullstack-App-Django-REST-React-`, `e-commerce`.
✅ Todos pasados a privado (2026-08-11) junto con el resto de la limpieza de visibilidad.

## Visibilidad de GitHub — RESUELTO (2026-08-11)
`gh` CLI autenticado como `bereail` (scope `repo`). Se aplicó el criterio "público solo lo que
suma como carta de presentación". **Públicos: Arbolada, Glicemia-Calculadora, librook,
Portfolio-Rodrigo, statuapp, VI.** Todo el resto (40 repos) quedó privado. Se descubrieron 23
repos privados adicionales sin carpeta local, varios con nombres de proyectos hospitalarios
(`HospitalComputos`, `PatrimonioHEEP`, `NEW_API_HEEP`, `HOLOS`, `MET-SIST1`, etc.) — quedan
fuera del alcance de esta etapa salvo que Berenice pida evaluarlos. Detalle completo en
`01-GITHUB/AUDITORIA-GITHUB.md` sección 6.

## Decisiones tomadas
Ver `00-CONTEXTO/DECISIONES.md`. Resumen: carpeta del proyecto vive en `Desktop/bere/PROYECTO-CARRERA-IT/`,
separada de `GIT/`. Se trabaja repo por repo, sin saltar etapas.

## Problemas detectados (sin resolver aún)
1. ✅ RESUELTO — Glicemia-Calculadora tiene documentación institucional del Hospital Eva Perón
   pública en GitHub (protocolo oficial en PDF). Berenice confirmó (2026-08-11) que tiene
   autorización del hospital para publicarlo. Se mantiene tal cual, no se toca.
2. 🔴 `Bebi` y `stockTonerDesktop` tienen el entorno virtual de Python completo versionado en git
   (miles de archivos). Requiere reescribir historial — se pedirá confirmación antes de tocarlo.
3. 🔴 `Bebi` tiene un commit ("prevenir que se vuelvan a commitear secretos") que sugiere secretos
   expuestos en commits anteriores. Pendiente auditar el historial completo antes de decidir estrategia.
4. 🟠 8 de 14 repos no tienen README real.
5. 🟠 3 repos distintos de Glicemia en GitHub (confuso para quien visita el perfil).
6. 🟡 Perfil de GitHub — EN CURSO (2026-08-13): README de perfil creado (repo `bereail/bereail`,
   pusheado) y descripciones cortas agregadas a `librook` y `VI` (Glicemia-Calculadora ya tenía).
   Pendiente: bio + nombre completo ("Berenice Solohaga") en el perfil — requiere que Berenice
   corra `gh auth refresh -h github.com -s user` (scope `user`, login interactivo, el asistente
   no lo puede disparar) para que `gh` pueda editar el perfil vía API. Foto de perfil también
   pendiente — requiere que ella suba una imagen propia, el asistente no tiene ninguna.
   stockTonerDesktop se mantiene privado a pedido explícito de Berenice (2026-08-13), aunque ya
   está limpio de datos sensibles.

## Problemas solucionados
1. Glicemia-Calculadora: README profesional, 5 screenshots reales, requirements.txt regenerado
   en UTF-8, eliminado código muerto (`pacientes/`, `_inspeccionar_pdf.py`), IPs de red interna
   sacadas de `settings.py`, rama `metricas` obsoleta borrada. Pusheado a GitHub
   (commits `2af89998` y `cabd451e`). Puntaje: 57 → 89/100.
2. statuapp: README reescrito con arquitectura real (Next.js full-stack + Netlify Blobs, sin
   backend Django separado), imagen de screenshots falsa (generada por IA) reemplazada por 3
   capturas reales, `package.json` corregido, PDFs internos sacados del repo, 2 commits locales
   pendientes pusheados. Además se corrigió la config global de git (autor genérico → Berenice
   Solohaga). Pusheado (commits `7c1da61` y `6481688`). Puntaje: ~74/100 — falta que Berenice
   dispare un redeploy en Netlify para que la demo muestre el mapa interactivo ya implementado.
   Pasado a PRIVADO a pedido de Berenice (fuera del foco de los 4 repos objetivo).
3. VI: README completo agregado, 9 capturas de pantalla completamente desactualizadas
   (mostraban un diseño anterior al rediseño visual de julio) reemplazadas por 2 capturas
   reales tomadas de la demo en producción, `package.json` corregido. 128 tests confirmados
   pasando. Pusheado (commit `3a47998`). Puntaje: 90/100.
4. stockTonerDesktop: historial de git completamente reescrito (54MB → 6.6MB) para sacar
   `.venv/` (9934 archivos), ejecutables de PyInstaller, `db.sqlite3`, y un archivo
   `inventario_data.json` con datos operativos reales del hospital (sectores, PCs, impresoras)
   que también estaban en 13 capturas de pantalla viejas. Todo lo sensible se preservó fuera
   del repo, no se perdió. README agregado, 2 capturas nuevas con datos ficticios, 2 fixtures
   rotos corregidos. Pusheado con `--force` tras confirmación explícita (commit `cf98ff0`).
   Puntaje: 85/100. Sigue privado.
5. Glicemia-Calculadora: a pedido de Berenice, se agregó al README un link a la demo real en
   producción (`138.36.238.175:8001/login`) — se verificó primero que el servidor no expone
   trazas de debug. Commit `82caea92`.

## Cosas que NO hay que cambiar
- No usar `git push --force` ni reescribir historial sin avisar y pedir confirmación explícita.
- No eliminar ni archivar repos sin confirmación de Berenice.
- No inventar experiencia laboral ni proyectos para el futuro CV — todo debe salir de lo que
  realmente existe en el código.

## librook — CERRADO (2026-08-13)

Lo que se hizo en las dos sesiones de trabajo sobre este repo:
- Feature "Community" (posts, comentarios, likes, alias público) verificada, testeada y
  commiteada — no era basura, era trabajo real a medio commitear (942 líneas).
- Restos vestigiales de Supabase eliminados (`src/lib/supabase.ts`, `supabase/schema.sql`,
  variables de entorno) tras confirmar que no se usaban — el backend real es Node/Express propio.
- `server.tar.gz` (artefacto de deploy redundante) eliminado del repo.
- Email personal real de Berenice sacado de `server/.env.example` (estaba hardcodeado).
- Vulnerabilidades de npm resueltas (frontend 5→0, backend 4→0), incluyendo bump de nodemailer
  6→9 (breaking, tests siguen pasando).
- README completo escrito desde cero (arquitectura real verificada en el código), con 5 capturas
  reales generadas en un entorno **local** aislado (Docker + Postgres temporal), sin tocar la
  producción de Berenice. Ver nota de seguridad abajo.
- Pusheado a GitHub: commits `2fd6e9c` (Community + limpieza Supabase) y `81ddbeb` (README +
  capturas).

⚠️ **Nota de seguridad relevante para futuras sesiones**: al intentar tomar las capturas usando
la demo de producción (`ailonline.com.ar/librook`), el token de sesión del navegador había
expirado, y al ir a re-loguear, Chrome autocompletó el email y la contraseña reales de Berenice
desde el gestor de contraseñas — no se usaron. Crear una cuenta de prueba (incluso con datos
ficticios) en el servidor de producción tampoco es algo que el asistente puede hacer. Por eso se
optó por levantar todo en local (Docker) para generar datos de demo. **Para futuros repos que
necesiten capturas con datos de prueba, preferir siempre un entorno local aislado en vez de la
demo de producción**, salvo que Berenice loguee ella misma.
