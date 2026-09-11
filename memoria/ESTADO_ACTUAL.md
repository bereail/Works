# ESTADO ACTUAL — Works

Leer este archivo primero al empezar cualquier sesión. Después, solo los archivos
puntuales que hagan falta (`memoria/PC_FIX.md` o `memoria/FREELANCE.md` según el
contexto activado).

**Última actualización:** 2026-09-11

## Área activa
PC FIX: investigación de Instagram + mejoras al generador de contenido, revisadas en
vivo con Berenice (ajuste de voz de marca, iteración de publicaciones de prueba).
Pendiente de arrancar: publicación real de Instagram vía automatización de
navegador (prioridad alta, ver `memoria/PC_FIX.md`). De paso, se arreglaron los
accesos directos del escritorio de PC FIX y Freelancer (apuntaban a una ruta vieja
desde la reorganización del 09-sep).

## Estado de PC FIX
Estrategia (etapas 1-4) y diseño de automatizaciones (etapas 6, 9) completos. El
sistema de generación de contenido con aprobación humana **ya está construido**
(`pc-fix/app/agents/agente_negocio.py`) y genera Instagram y Facebook juntas en cada
corrida, con hashtags y CTA adaptados por red, sin la frase "en criollo" y con tips
reales para el pilar técnico. Facebook publica de verdad con un click. Instagram
**todavía no** — tiene un kit de publicación manual como paso intermedio, pero
Berenice pidió que el botón "Publicar" termine publicando de verdad vía
automatización de navegador (un solo click real de su lado) — es el próximo paso a
construir. Detalle: `memoria/PC_FIX.md`.

## Estado de FREELANCE
Perfil, LinkedIn y GitHub ya optimizados (Fases 0-1). Ingesta automática de ofertas
de 4 fuentes públicas ya funcionando (Fase 2b, terminada hoy mismo). Matching Engine
real (Fase 3) todavía no arrancó. Detalle: `memoria/FREELANCE.md`.

## Últimas decisiones (ver `historial/decisiones.md` para el detalle completo)
- **2026-09-11 (más reciente):** revisando publicaciones generadas en vivo, Berenice
  aclaró que el botón "Publicar" de Instagram tiene que publicar de verdad
  automatizando el navegador con su sesión ya logueada — el kit manual (copiar/
  descargar) fue un paso intermedio, no el diseño final. Corrigió también la voz de
  marca ("no digas 'en criollo'") y pidió contenido con tips reales, no solo copy
  promocional. Se arreglaron además los accesos directos del escritorio de PC FIX y
  Freelancer, rotos desde la reorganización del repo del 09-sep.
- **2026-09-11:** investigación de Instagram (propio + 6 competidores de Rosario) →
  el botón único del dashboard generaba publicaciones solo para Instagram, nunca para
  Facebook (el canal ya 100% automatizado) — corregido. Se sumaron hashtags curados
  por pilar (solo Instagram) y CTA adaptado por plataforma.
- **2026-09-09:** auditoría completa del repo + reorganización. Se corrigió una
  fuga de credenciales (contraseña del VPS de Glicemia, ya rotada por Berenice) y se
  sacaron del repo dos carpetas con datos reales del Hospital Eva Perón que nunca
  debieron estar ahí. `pc-fix/` y `freelancer/` dejaron de ser repos git separados —
  ahora todo `Works` es un solo repositorio, así que `git pull`/`git push` vuelve a
  sincronizar todo entre las dos computadoras.

## Tareas pendientes / próximos pasos
- **PC FIX, prioridad alta:** construir la publicación real de Instagram vía
  automatización de navegador para el botón "Publicar" — decisión ya tomada, hacerlo
  con Berenice presente (primer login/posteo real). Ver `memoria/PC_FIX.md` y memoria
  global de Claude (`pcfix_boton_publicar_instagram`).
- Confirmar con Berenice si `freelancer/notas/career-master-memory-2026-09-01.html`
  sigue teniendo valor o se puede dejar de generar (ver nota en
  `historial/decisiones.md`).
- PC FIX: definir con Berenice si vale invertir tiempo en contenido de video/reels —
  es lo que mejor le está funcionando a la competencia local mejor posicionada, pero
  el sistema actual no lo automatiza (solo flyers estáticos).
- FREELANCE: definir con Berenice si se arranca la Fase 3 (Matching Engine).

## Bloqueos
Ninguno.
