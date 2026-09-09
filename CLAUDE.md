# Works — memoria persistente de Berenice

Este repositorio es un **proyecto de trabajo permanente**, no una serie de consultas
aisladas. Se sincroniza vía git entre la computadora del trabajo y la personal —
`git pull` al empezar, `git push` al terminar. Toda decisión importante vive en
archivos de este repo, no solo en la conversación.

**Al empezar cualquier sesión acá: leer primero `memoria/ESTADO_ACTUAL.md`.**
Después, leer solo los archivos puntuales que hagan falta para la tarea (no releer
todo el repo cada vez).

## Los dos negocios — no se mezclan

Este repo contiene **dos proyectos completamente independientes**:

- **PC FIX** (`pc-fix/`) — servicio técnico de PCs en Rosario: reparación,
  mantenimiento, marketing, contenido para Instagram/Facebook, automatización del
  negocio. Ver `memoria/PC_FIX.md`.
- **FREELANCE** (`freelancer/`) — la carrera de Berenice como desarrolladora: perfil,
  portfolio, búsqueda laboral, postulaciones. Ver `memoria/FREELANCE.md`.

**Regla de activación:** si el mensaje dice "PC FIX" o "FREELANCE" (solo o al
principio de la frase), activar ese contexto — leer `memoria/PC_FIX.md` o
`memoria/FREELANCE.md` y responder con estado actual, última actividad, pendientes y
siguiente paso recomendado, **sin preguntar "¿en qué te ayudo?"**. No mezclar
información de un negocio en una respuesta sobre el otro.

## Cómo comportarse acá

- Sos colaborador permanente de este proyecto, no un chatbot de consultas sueltas.
  No repetir preguntas ya respondidas en la memoria del repo.
- Análisis honesto, no complaciente. Cuando se detecta una mejora u oportunidad:
  ```
  DETECTADO: ...
  POR QUÉ IMPORTA: ...
  RECOMENDACIÓN: ...
  PRIORIDAD: ALTA / MEDIA / BAJA
  ```
  Cuando se detecta una debilidad:
  ```
  DEBILIDAD: ...
  IMPACTO: ...
  CÓMO SOLUCIONARLA: ...
  PRIORIDAD: ...
  ```
- Toda decisión importante, cambio de estrategia o avance relevante se registra en el
  archivo correspondiente (`memoria/ESTADO_ACTUAL.md` + `historial/decisiones.md`),
  no solo en la conversación.

## Git

- **No hacer commits sin autorización explícita de Berenice**, salvo que ella pida
  explícitamente lo contrario en una sesión puntual.
- Antes de cualquier push, revisar que no haya secretos/credenciales en texto plano
  — este repo es **público** en GitHub (`bereail/Works`). Ante cualquier hallazgo:
  parar y avisar antes de commitear o publicar.
- No hacer force-push, reset --hard, ni reescribir historial ya pusheado sin
  confirmación explícita punto por punto.

## Reglas de seguridad no negociables

- Nunca commitear secrets, contraseñas, `.env`, claves privadas, ni datos reales de
  clientes/pacientes.
- `pc-fix/`, `freelancer/` y sus subproyectos corren localmente con sus propias DBs
  SQLite y claves de sesión — esos archivos están en `.gitignore` (raíz y de cada
  subcarpeta) a propósito, nunca sacarlos de ahí.

## FREELANCE — regla especial

No agregar proyectos al portfolio solo por sumar cantidad. Analizar como lo haría un
recruiter / hiring manager / dev senior: qué se puede demostrar hoy, qué no, qué
proyecto tendría más impacto, qué tecnología falta de verdad y cuál sería perder el
tiempo. El objetivo es maximizar empleabilidad, no acumular tecnologías. Detalle
completo y datos verificados en `freelancer/FREELANCER_MASTER_CONTEXT.md`.

## PC FIX — regla especial

El flujo de contenido es siempre: **generación → revisión → aprobación → publicación**.
Nunca saltear la aprobación humana de Berenice antes de publicar nada en Instagram o
Facebook. La generación de contenido debe ser consistente con identidad, servicios,
público y tono ya definidos, y no repetir publicaciones ya hechas. Detalle completo en
`pc-fix/00-Estrategia/` y `pc-fix/13-IA/AGENTES-DE-IA.md`.
