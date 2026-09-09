# ESTADO ACTUAL — Works

Leer este archivo primero al empezar cualquier sesión. Después, solo los archivos
puntuales que hagan falta (`memoria/PC_FIX.md` o `memoria/FREELANCE.md` según el
contexto activado).

**Última actualización:** 2026-09-09

## Área activa
Reorganización del repositorio recién terminada. Sin negocio específico activado —
esperando que Berenice diga "PC FIX" o "FREELANCE" para continuar el trabajo de fondo
de cada uno.

## Estado de PC FIX
Estrategia (etapas 1-4) y diseño de automatizaciones (etapas 6, 9) completos. El
sistema de generación de contenido con aprobación humana **ya está construido**
(`pc-fix/app/agents/agente_negocio.py`). Integración con Meta API en curso. Detalle:
`memoria/PC_FIX.md`.

## Estado de FREELANCE
Perfil, LinkedIn y GitHub ya optimizados (Fases 0-1). Ingesta automática de ofertas
de 4 fuentes públicas ya funcionando (Fase 2b, terminada hoy mismo). Matching Engine
real (Fase 3) todavía no arrancó. Detalle: `memoria/FREELANCE.md`.

## Últimas decisiones (ver `historial/decisiones.md` para el detalle completo)
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
- PC FIX: arrancar Etapa 5 (procedimientos operativos) cuando Berenice lo indique.
- FREELANCE: definir con Berenice si se arranca la Fase 3 (Matching Engine).

## Bloqueos
Ninguno.
