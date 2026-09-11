# ESTADO ACTUAL — Works

Leer este archivo primero al empezar cualquier sesión. Después, solo los archivos
puntuales que hagan falta (`memoria/PC_FIX.md` o `memoria/FREELANCE.md` según el
contexto activado).

**Última actualización:** 2026-09-11

## Área activa
PC FIX activo: investigación de Instagram (propio + competencia de Rosario) e
implementación de mejoras al generador de contenido, recién terminada. Ver
`memoria/PC_FIX.md`.

## Estado de PC FIX
Estrategia (etapas 1-4) y diseño de automatizaciones (etapas 6, 9) completos. El
sistema de generación de contenido con aprobación humana **ya está construido**
(`pc-fix/app/agents/agente_negocio.py`) y ahora genera Instagram y Facebook juntas
en cada corrida, con hashtags y CTA adaptados por red. Facebook publica de verdad con
un click; Instagram tiene un kit de publicación manual (copiar texto + descargar
imagen) porque Berenice decidió no conectarlo por API. Detalle: `memoria/PC_FIX.md`.

## Estado de FREELANCE
Perfil, LinkedIn y GitHub ya optimizados (Fases 0-1). Ingesta automática de ofertas
de 4 fuentes públicas ya funcionando (Fase 2b, terminada hoy mismo). Matching Engine
real (Fase 3) todavía no arrancó. Detalle: `memoria/FREELANCE.md`.

## Últimas decisiones (ver `historial/decisiones.md` para el detalle completo)
- **2026-09-11:** investigación de Instagram (propio + 6 competidores de Rosario) →
  el botón único del dashboard generaba publicaciones solo para Instagram, nunca para
  Facebook (el canal ya 100% automatizado) — corregido. Se sumaron hashtags curados
  por pilar (solo Instagram) y CTA adaptado por plataforma. Instagram pasó a tener un
  kit de publicación manual (copiar texto + descargar imagen) en vez de un intento de
  publicación real que nunca iba a poder completarse.
- **2026-09-09:** auditoría completa del repo + reorganización. Se corrigió una
  fuga de credenciales (contraseña del VPS de Glicemia, ya rotada por Berenice) y se
  sacaron del repo dos carpetas con datos reales del Hospital Eva Perón que nunca
  debieron estar ahí. `pc-fix/` y `freelancer/` dejaron de ser repos git separados —
  ahora todo `Works` es un solo repositorio, así que `git pull`/`git push` vuelve a
  sincronizar todo entre las dos computadoras.

## Tareas pendientes / próximos pasos
- Confirmar con Berenice si `freelancer/notas/career-master-memory-2026-09-01.html`
  sigue teniendo valor o se puede dejar de generar (ver nota en
  `historial/decisiones.md`).
- PC FIX: definir con Berenice si vale invertir tiempo en contenido de video/reels —
  es lo que mejor le está funcionando a la competencia local mejor posicionada, pero
  el sistema actual no lo automatiza (solo flyers estáticos).
- FREELANCE: definir con Berenice si se arranca la Fase 3 (Matching Engine).

## Bloqueos
Ninguno.
