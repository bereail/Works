# Historial de decisiones — Works

Decisiones que cruzan ambos negocios o que son sobre el repositorio en sí. Las
decisiones específicas de cada negocio viven en su propia memoria
(`freelancer/FREELANCER_MASTER_CONTEXT.md` sección 5, `pc-fix/00-Estrategia/DECISIONES-PENDIENTES.md`).

---

## 2026-09-09 — PC FIX: corregido el roadmap, la Etapa 5 ya estaba completa

`00-Estrategia/00-ROADMAP.md` marcaba la Etapa 5 (procedimientos operativos) como
"próxima fase automática", pero `14-Procedimientos/MANUAL-FLUJO-OPERATIVO.md` ya
existía completo (11 pasos, con nota de automatización futura en cada uno) y de hecho
es la base sobre la que se diseñó la Etapa 6, que sí figuraba completa. El roadmap
nunca se actualizó cuando se cerró la Etapa 5. Se corrigió el estado en el roadmap.
**Lección:** el roadmap puede estar desfasado respecto del contenido real de las
carpetas — antes de dar por "pendiente" una etapa, revisar si ya existe el archivo
resultado esperado.

---

## 2026-09-09 — PC FIX: Instagram no se conecta vía API

Berenice confirmó que **no quiere conectar Instagram a la Graph API de Meta**. El
flujo querido es: el sistema genera el mismo contenido para ambas redes, pero se
publica por separado — Facebook vía la automatización ya conectada (funcionando desde
el 3-sep-2026), Instagram publicado a mano por ella. No volver a proponer conectar
Instagram salvo que lo pida explícitamente. Detalle en `memoria/PC_FIX.md`.

---

## 2026-09-09 — Auditoría y reorganización completa del repositorio

Berenice pidió tratar `Works` como proyecto persistente compartido entre PC FIX y
FREELANCE, con memoria en archivos (no solo en la conversación). Antes de crear la
estructura pedida, se auditó todo el repo existente. Hallazgos y acciones:

- **Seguridad crítica:** `glicemia-deploy-notas.md` tenía en texto plano la
  contraseña root del VPS de Glicemia-Calculadora (sistema en uso en el Hospital Eva
  Perón), y el commit ya estaba pusheado a `bereail/Works`, que es **público**. Se
  redactó el archivo, se reescribió el commit único del repo (`git commit --amend` +
  `push --force-with-lease`) para sacarla del historial, y Berenice **rotó la
  contraseña real en el servidor** el mismo día (confirmado).
- **Segundo hallazgo de seguridad:** dentro de `freelancer/PROYECTO-CARRERA-IT/`
  (nunca antes commiteada en ningún repo) había dos carpetas con **datos reales de
  infraestructura del Hospital Eva Perón** — `git-backup-pre-filter-repo/` (backup de
  54MB del historial de stockTonerDesktop de antes de limpiarlo, con
  `inventario_data.json` real) y `screenshots-con-datos-reales-hospital/` (14
  capturas). Se sacaron del todo del repo, movidas a
  `C:\Users\bsolohaga\Desktop\bere\_respaldos-locales-fuera-de-git\` — nunca llegaron
  a subirse a GitHub.
- **Estructura rota de sincronización:** `freelancer/` y `pc-fix/` eran repos git
  independientes sin remoto propio en GitHub (llegaron a esa forma por una serie de
  renombres desde submódulos originales sin `.gitmodules`). Consecuencia: un
  `git pull` de `Works` en otra computadora no traía nada de esos dos negocios. Se
  decidió (con Berenice, confirmando "un solo repositorio") **aplanar ambos como
  carpetas normales** dentro de `Works`, preservando su historial de commits real vía
  `git subtree` (15 commits de pc-fix, 1 de freelancer) en vez de perderlo.
- Al aplanar, se rescató también **trabajo en curso sin commitear** que tenían ambos
  repos: integración con Meta API y tarjeta de presentación en pc-fix; y en
  freelancer, el código de ingesta de ofertas y — lo más importante — **todo
  `PROYECTO-CARRERA-IT/` y los tres `portafolio-*`**, que hasta ese día nunca habían
  estado respaldados en git en ningún repositorio.
- Se sacó el gitlink huérfano `turnero` del índice (carpeta ya inexistente en disco,
  sin `.gitmodules`) a pedido de Berenice — no se investigó más su origen.
- Se agregó `.gitignore` en la raíz de `Works` (venv/, `*.db`, `*.log`,
  `.clave_sesion`, `__pycache__/`) para que las apps de ambos negocios sigan
  corriendo local sin versionar su estado.
- Archivos sueltos de contenido/notas que vivían en la raíz del repo se movieron a
  `pc-fix/contenido/` y `freelancer/notas/` respectivamente, para no mezclar los dos
  negocios fuera de sus carpetas.
- `freelancer/PROYECTO-CARRERA-IT/00-CONTEXTO/*.md` y `MEMORIA-PROYECTO.md` (memoria
  de la auditoría de GitHub, plan de "8 etapas") se marcaron como histórico —
  superados por `freelancer/FREELANCER_MASTER_CONTEXT.md`, que ya absorbió y superó
  esa etapa.
- Se creó la estructura de memoria pedida: `CLAUDE.md` (raíz), `memoria/` con
  `CONTEXTO_GENERAL.md`, `ESTADO_ACTUAL.md`, `PC_FIX.md`, `FREELANCE.md`, y este
  archivo (`historial/decisiones.md`).

**Pendiente de esta reorganización:** decidir qué hacer con
`freelancer/notas/career-master-memory-2026-09-01.html` (dashboard visual, contenido
solapado con `busqueda-laboral.md` en la misma carpeta) — se conservó como snapshot
histórico sin resolver del todo si sigue teniendo valor seguir generándolo.

---

## 2026-09-11 — PC FIX: investigación de Instagram (propio + competencia de Rosario) y mejoras al generador de contenido

**Investigación:** cuenta propia `@pcfix.informatica` (57 seguidores, sigue a 332 —
ratio invertido) publica solo posts estáticos de promociones, sin hashtags. Se
relevaron 6 cuentas de servicio técnico de Rosario; la de mejor desempeño local
(`@rosarioblackam`, ~3.000 seguidores, verificada) crece con video corto mostrando
reparación real (reballing, componentes, "laboratorio"), organizado en categorías de
destacados — ninguna usa hashtags de forma visible tampoco, así que ahí sigue habiendo
oportunidad real si PC Fix los suma bien. Ninguna cuenta relevada juega en
transparencia de precios ni proceso — confirma que esos dos pilares (ya elegidos en
`05-Redes/PLAN-DE-CONTENIDOS.md`) siguen siendo el diferencial correcto.

**Hallazgo de código:** `generar_publicacion_automatica` (el botón único del
dashboard) generaba **una sola publicación, siempre en Instagram**, nunca en
Facebook — o sea que el único canal ya automatizado de punta a punta (Facebook, con
API real conectada) no se estaba alimentando desde el flujo automático. Corregido:
ahora genera las dos publicaciones (mismo servicio, misma imagen, copy adaptado por
red) en cada corrida.

**Implementado:**
- Campo `hashtags` en `Publicacion` (migración `a1c2e3f4b5d6`) + generador de
  hashtags curados por pilar de contenido, **solo para Instagram** (en Facebook no
  aportan alcance real y ensucian el texto).
- CTA distinto por plataforma en `generador_copy.py`: Facebook más formal, orientado
  a dueños de comercio (coincide con el público más adulto que señala Fase 2);
  Instagram más directo/casual.
- `generar_publicacion_automatica` ahora crea Instagram **y** Facebook juntas,
  compartiendo el mismo flyer generado (no se renderiza dos veces).
- Como Berenice decidió no conectar Instagram por API (ver nota en `PC_FIX.md`), se
  reemplazó el intento de publicación real de Instagram en la previsualización por un
  **kit de publicación manual**: texto + CTA + hashtags listos para copiar con un
  click, e imagen lista para descargar con un click — y un botón "Ya la publiqué en
  Instagram" que solo confirma el estado. Facebook sigue con su publicación real de
  un click, sin cambios.
- 5 tests nuevos (`tests/test_agente_negocio.py`) cubriendo la generación de a pares
  y la diferenciación por plataforma. Los 14 tests existentes siguen pasando (19
  en total).

**No implementado (fuera del alcance de código):** contenido en video (reels) — el
sistema solo compone flyers estáticos vía plantilla HTML/Playwright, no genera video;
quedaría como una automatización nueva y más cara de construir, no una mejora al
generador actual.
