# Historial de decisiones — Works

Decisiones que cruzan ambos negocios o que son sobre el repositorio en sí. Las
decisiones específicas de cada negocio viven en su propia memoria
(`freelancer/FREELANCER_MASTER_CONTEXT.md` sección 5, `pc-fix/00-Estrategia/DECISIONES-PENDIENTES.md`).

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
