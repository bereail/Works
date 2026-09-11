# PC FIX — memoria rápida

Detalle completo: `pc-fix/00-Estrategia/00-ROADMAP.md` (roadmap por etapa) y
`pc-fix/README.md` (mapa de carpetas). Este archivo es solo el resumen para arrancar
rápido — no duplicar acá el detalle, actualizarlo ahí y linkearlo.

## Estado por etapa (ver roadmap para el detalle)

1. Auditoría integral (FODA) — ✅ completo
2. Análisis de mercado Rosario — ✅ completo
3. Posicionamiento de marca — ✅ completo
4. Catálogo de servicios y rentabilidad — ✅ completo
5. Procedimientos operativos — ✅ completo (el roadmap tenía esto desactualizado
   como pendiente; se corrigió el 2026-09-09 — ver `historial/decisiones.md`)
6. Automatizaciones (diseño + infraestructura) — ✅ diseño y decisiones listas,
   **implementación real en curso** (ver más abajo)
7. Web + SEO — ⏸ en pausa por decisión propia
8. Redes sociales (plan de contenidos) — ✅ completo, 1 publicación/semana
9. CRM, finanzas, inventario, dashboard — ✅ diseño completo, listo para implementar
10. Publicidad paga — ⏸ en pausa, presupuesto $0

## Decisiones de infraestructura ya resueltas (5 ago 2026)
1-5 hs/semana disponibles · dominio `ailonline.com.ar/pcfix` · hosting en PC propia ·
WhatsApp con Evolution API self-hosted · sin monotributo todavía (números internos,
no oficiales) · $0 de presupuesto de ads · atención en punto fijo, dirección
confirmada **Olive 1200, Rosario** (no está cargada en Meta Business todavía — en
pausa a pedido de Berenice, ver `pc-fix/17-Backlog/IDEAS-PENDIENTES.md`). Detalle:
`pc-fix/00-Estrategia/DECISIONES-PENDIENTES.md`.

## El sistema de automatización de contenido — YA EXISTE

El objetivo de "Claude genera → Berenice aprueba → se publica" **ya está construido**,
no es un proyecto nuevo a arrancar de cero:
- `pc-fix/app/agents/agente_negocio.py` — genera copy y flyer, deja la publicación en
  estado `previsualizado`, un solo click para confirmar.
- Diseño de 3 agentes (Atención / Contenido / Análisis) en
  `pc-fix/13-IA/AGENTES-DE-IA.md` — el de Contenido nunca publica solo.

### Integración con Meta API — verificada el 2026-09-09

- **Facebook: conectada de verdad y funcionando.** Token de página válido (sin
  expiración, scopes correctos), verificado con una llamada real de solo lectura a la
  Graph API. Ya publicó de verdad al menos una vez: publicación #29, 3-sep-2026,
  `id_publicacion_externa = 725615510632047_122200756442938008`.
- **Instagram: todavía en modo simulado.** Berenice confirmó (2026-09-09) que no
  quiere conectar Instagram por la **API oficial de Meta** (exige verificación de
  negocio + URL pública para la imagen). **Aclarado el 2026-09-11: eso no significa
  que quiera publicar a mano.** El botón "Publicar" de Instagram tiene que terminar
  publicando de verdad, automatizando el navegador (Chrome, sesión ya logueada de
  ella, sin que el sistema maneje su contraseña) en vez de usar la API — ver
  `[[pcfix_boton_publicar_instagram]]` en la memoria global de Claude y el detalle
  completo más abajo. Todavía no está implementado — el kit de copiar/descargar que
  se armó el 2026-09-11 es un paso intermedio, no el diseño final.
- El resto de publicaciones marcadas "publicado" en la base (17 de 18) son datos de
  prueba sembrados el 20-21 de agosto (`origen_datos='simulado'`), sin ID externo
  real — no confundir con actividad real.
- **Tests agregados el 2026-09-09** (`pc-fix/tests/test_meta_api.py`,
  `test_publicar_de_verdad.py`): 14 tests, cubren `publicar_en_facebook`/
  `publicar_en_instagram` (éxito y error de Meta, HTTP mockeado) y toda la lógica de
  bloqueo de `_publicar_de_verdad` (sin cuenta conectada, sin flyer, archivo
  faltante, falta URL pública de Instagram, camino feliz, error de Meta → estado
  `error`). Ninguno sale a internet. Correr con
  `pc-fix/venv/Scripts/python.exe -m pytest tests/` desde `pc-fix/`.

### Generación de contenido — mejorada el 2026-09-11 (investigación de Instagram)

Investigación breve de `@pcfix.informatica` y 6 competidores de Rosario (detalle en
`historial/decisiones.md`): la cuenta propia no usaba hashtags y el botón único del
dashboard solo generaba publicaciones para Instagram, nunca para Facebook (el canal
que sí está 100% automatizado). Cambios ya implementados:
- `generar_publicacion_automatica` ahora crea **Instagram y Facebook juntas** en cada
  corrida (mismo servicio, mismo flyer, copy adaptado por red).
- Hashtags curados por pilar, solo en Instagram (campo nuevo `Publicacion.hashtags`).
- CTA distinto por plataforma (Facebook más formal/PyME, Instagram más directo).
- Instagram ya no intenta publicar por API en la previsualización — en su lugar hay
  un **kit de publicación manual**: botón "copiar texto + hashtags" y botón
  "descargar imagen", más un botón "Ya la publiqué en Instagram" que solo confirma el
  estado. Esto es un paso intermedio, no el diseño final — ver "Pendientes" más abajo.
- Facebook sigue publicando de verdad con un solo click, sin cambios.
- Ajuste de voz de marca (mismo día, al revisar publicaciones generadas con
  Berenice): sacada la frase "en criollo" del copy (quedaba mal, corregido a pedido
  de ella) y agregado `PLANTILLAS_TIP_CRITERIO_TECNICO` — tips reales (SSD vs.
  procesador, mito del formateo) en vez de copy promocional genérico para el pilar
  "criterio_tecnico". Guardado en memoria global de Claude
  (`pcfix_voz_de_marca_copy`).

### Acceso directo del escritorio — arreglado el 2026-09-11

`PCfix Automation Center.lnk` ya existía en el escritorio pero apuntaba a la ruta
vieja de antes del aplanamiento del repo (09-sep) y ya no abría nada. Se corrigió
para apuntar a `Works\pc-fix\iniciar_silencioso.vbs` (nuevo, mismo patrón que ya
tenía Freelancer: si el servidor no está corriendo lo levanta oculto y recién
entonces abre el navegador en `/inicio` — un solo click). Probado de verdad, funciona.
Detalle completo (incluye el mismo arreglo para el ícono de Freelancer) en
`historial/decisiones.md`.

## Pendientes / próximos pasos
- **Prioridad alta:** implementar la publicación real de Instagram vía automatización
  de navegador — el botón "Publicar" debe ser el único click manual de Berenice; todo
  lo demás (subir imagen a Instagram, pegar texto, click en "Compartir" ahí) lo hace
  la automatización disparada por ese click. Decisión tomada el 2026-09-11, detalle
  completo en `historial/decisiones.md` y en la memoria global de Claude
  (`pcfix_boton_publicar_instagram`). Riesgo conocido a documentarle a Berenice antes
  de la primera publicación real por esta vía: Instagram puede detectar y restringir
  cuentas que publican por automatización de navegador en vez de la app/web oficial.
- Contenido/borradores sueltos que vivían en la raíz de `Works` ahora están en
  `pc-fix/contenido/` — revisar si siguen vigentes o ya se publicaron.
- Fuera de alcance de este avance: contenido en video/reels. El sistema solo compone
  flyers estáticos (plantilla HTML + Playwright); video sería una automatización
  nueva, no una mejora del generador actual. La competencia local de mejor desempeño
  en Rosario (`@rosarioblackam`, ~3.000 seguidores) crece justamente con video corto
  de reparaciones reales — quedaría como próxima oportunidad si Berenice quiere
  invertir tiempo en grabar.
- Cuenta de Instagram con ratio de seguidos invertido (57 seguidores / sigue a 332)
  — no es algo que se resuelva por código, queda anotado para que Berenice lo revise
  cuando tenga un rato.

## Nota técnica
`pc-fix/venv/` hay que recrearlo si no existe (no se versiona): `python -m venv
pc-fix/venv` y después `pc-fix/venv/Scripts/python.exe -m pip install -r
pc-fix/requirements.txt pytest`.

## Bloqueos activos
Ninguno crítico.
