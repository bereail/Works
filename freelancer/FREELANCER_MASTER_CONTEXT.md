# FREELANCER — Fuente de verdad

Este archivo es la única fuente de verdad del proyecto "Freelancer" de Berenice (carrera como Desarrolladora Full Stack, independiente de PCfix Informática). Cualquier conversación nueva sobre este tema debe empezar leyendo este archivo — no volver a pedirle que explique de nuevo su perfil, proyectos o estrategia.

**Regla de este archivo:** no duplicar información. Si un dato cambia, se actualiza acá mismo, no se crea una versión nueva.

Última actualización: 2026-09-09 (Fase 2b — ingesta automática de ofertas desde APIs/RSS públicas — construida).

---

## 1. PERFIL BASE (DATO — verificado en github.com/bereail el 2026-08-20)

- GitHub: [github.com/bereail](https://github.com/bereail) — cuenta creada 2021-12-11, con actividad real reciente (todos los repos actualizados el 2026-08-18).
- Ubicación (perfil de GitHub): Rosario, Santa Fe, Argentina.
- 5 repositorios públicos: 4 proyectos reales + 1 README de perfil (`bereail/bereail`).
- Campo "hireable" de GitHub: **no activado**. Bio de usuario: **vacía**. Sin link a LinkedIn/portfolio en el perfil de usuario (solo dentro del README).
- Rol actual (de `00-Estrategia/FASE-1-AUDITORIA-FODA.md` del proyecto PCfix): Analista de Sistemas, full-time en una institución + PCfix como segundo trabajo/freelance propio. Dos de sus proyectos de GitHub están en uso real en esa institución: el **Hospital Eva Perón** (dato tomado del propio README de perfil de Berenice, no inventado).

### Los 4 proyectos reales

| Proyecto | Stack | Testing | Estado |
|---|---|---|---|
| **Glicemia-Calculadora** (METANUTRIC) | Django 5.2, SQLite→Postgres, Chart.js, openpyxl, reportlab | 108 tests | En uso real en UCI del Hospital Eva Perón. [Demo](http://138.36.238.175:8001/login) (credenciales a pedido) |
| **StockFlow** | Django 5.2 embebido + pywebview + waitress, PyInstaller (.exe) | 70 tests | En uso real en el mismo hospital (inventario de insumos IT) |
| **librook** | React 19 + TypeScript + Vite (PWA), Node/Express + PostgreSQL, JWT+bcrypt | Vitest + Testing Library + Jest + Supertest | Deploy real (VPS propio, `deploy.sh`). [Demo pública](https://ailonline.com.ar/librook/) — botón "Ver sin cuenta" |
| **VI** | React 19 + Vite, Node/Express + PostgreSQL, JWT+bcrypt | 128 tests (Vitest + Testing Library) + Playwright E2E | CI/CD real con GitHub Actions (rsync/SSH, secrets en GitHub Actions). [Demo pública](https://ailonline.com.ar/vi/) — botón "Ver sin cuenta" |

Las 3 demos públicas verificadas activas (HTTP 200) el 2026-08-20.

### Patrón técnico real demostrado (DATO)

- Combo dominante: **Django (backend monolítico)** en los proyectos "serios"/institucionales, y **React + Node/Express + PostgreSQL (API separada)** en los proyectos personales full-stack.
- **Testing exhaustivo y consistente en los 4 proyectos** — esto es inusual y es el diferencial más fuerte del perfil (Django TestCase, Vitest, Jest+Supertest, Playwright E2E).
- Buenas prácticas de seguridad repetidas: secrets nunca hardcodeados, variables de entorno documentadas, `DEBUG` desactivado en producción, credenciales de deploy en GitHub Secrets.
- Arquitectura en capas explícita en Glicemia (`views → services → lógica pura → adaptadores UI → reportes`), documentación de estructura de carpetas en los 4 READMEs.
- Deploy real: VPS propio con `rsync`/`ssh`/`systemctl`, CI/CD con GitHub Actions, empaquetado de escritorio con PyInstaller.
- Integraciones con APIs externas reales: OpenLibrary, TMDB.

---

## 2. ESTRATEGIA RECOMENDADA (Fase 0 — auditoría del 2026-08-20)

### Posicionamiento recomendado (RECOMENDACIÓN)

No venderse como "junior buscando su primera oportunidad de programación". La calidad de ingeniería (testing, arquitectura, seguridad, deploy real) está por encima de lo típico de un perfil junior. El ángulo real y más fuerte es:

> **"Full Stack Developer (Django + React/Node) que ya construye y mantiene sistemas en producción real — no proyectos de práctica."**

Esto conecta directo con lo que PCfix también quiere vender (sistemas/automatización para PyMEs) — hay sinergia real entre ambos negocios: mismo público objetivo potencial (organizaciones/PyMEs que necesitan un sistema interno, no un sitio de marketing).

### Top skills (evidencia real, no inventada)

1. Django — backend, ORM, admin, auth por grupos, arquitectura en capas (2 sistemas en producción real).
2. React 19 + hooks propios + testing de componentes.
3. Node.js/Express + APIs REST propias.
4. PostgreSQL y SQLite.
5. **Testing automatizado en profundidad** — diferencial más fuerte del perfil frente al freelancer promedio.
6. Autenticación propia (JWT + bcrypt), sin depender de servicios de terceros.
7. Deploy real (VPS propio, CI/CD, empaquetado desktop).
8. Integración de APIs externas.
9. Generación de reportes (Excel, PDF).
10. Diseño de UI propio, sin librerías de componentes prearmadas.

### Debilidades detectadas (INTERPRETACIÓN honesta)

- El perfil de GitHub (la página de usuario, no los repos) no vende: sin bio, sin "hireable", sin contacto visible fuera del README.
- Sin badge de CI visible en README de VI (ya tiene el pipeline armado, solo falta mostrarlo).
- TypeScript solo en librook, no en VI — inconsistencia menor pero visible.
- Sin proyectos con Next.js — hoy muy pedido en ofertas de React.
- Sin case studies narrativos (los README son técnicos/funcionales, no cuentan la historia en términos que entienda un cliente no técnico).
- Presencia en LinkedIn: **no verificada** — no tengo acceso, no se puede confirmar ni descartar. No inventar.
- Inglés técnico: **no verificado** — preguntar directamente antes de asumir nada, es alto impacto para plataformas internacionales.

### Quick wins (impacto alto, esfuerzo bajo)

1. ✅ Hecho (2026-08-20) — "Hireable" activado + bio: "Full Stack Developer · Django + React/Node · sistemas en producción real, no solo proyectos de práctica".
2. ✅ Hecho (2026-08-20) — URL del perfil: `https://ailonline.com.ar` (agrupa las demos de VI y librook).
3. ✅ Hecho (2026-08-20) — badge de GitHub Actions ("Tests") agregado al README de VI, [commit](https://github.com/bereail/VI/commit/4e057fd8d1c6a8db9ac09856b0a26a5c6aecc2ae).
4. ✅ Ya estaba — los 4 proyectos ya están fijados en el perfil, con Glicemia primero (orden exacto de los otros 3 no se tocó para no arriesgar el drag & drop automatizado).
5. ✅ Hecho (2026-08-20) — GIF de demo agregado a los README de VI ([commit](https://github.com/bereail/VI/commit/6879a9a6906557a727b39a29dd0a735a13c776f6)) y librook ([commit](https://github.com/bereail/librook/commit/bc276f57df83110331d8f24c46f4ce6d544a50c9)). El de librook quedó casi estático (1 frame) — se puede regrabar más adelante con un recorrido más largo si se quiere más movimiento.

**Los 5 quick wins de GitHub: completos.**

### Clasificación de proyectos

- **Glicemia-Calculadora** — ⭐ STAR + 🚀 candidato a CASE STUDY (dominio complejo real, en producción, mejor testing).
- **StockFlow** — ⭐ STAR (caso de uso real, arquitectura de escritorio poco común como diferenciador).
- **VI** — 🟢 KEEP (demuestra CI/CD real, diferenciador que los otros dos no muestran).
- **librook** — 🟢 KEEP (demo pública navegable, full-stack JS moderno con TypeScript).
- **Perfil `bereail/bereail`** — 🟡 IMPROVE (contenido sólido, falta contacto directo y optimización como "landing" de reclutamiento).

Ningún proyecto para ocultar/archivar — los 4 aportan un ángulo distinto.

### Employability Score (estimación cualitativa mía, basada en evidencia visible — no una medición externa objetiva)

| Área | Score | Nota |
|---|---|---|
| GitHub (código, README, estructura) | 82/100 | Muy por encima del promedio |
| Portfolio / Demos | 75/100 | 3 de 4 con demo viva, faltan case studies narrativos |
| Technical Proof (testing, arquitectura, deploy) | 88/100 | El punto más fuerte del perfil |
| LinkedIn / contacto externo | No evaluable | No hay datos suficientes para determinarlo |
| Freelance Positioning (oferta de servicios clara) | 70/100 | Oferta ya definida internamente (2026-08-20) — sube cuando esté publicada/comunicada |

### Top job types a priorizar (RECOMENDACIÓN)

1. **Django Developer / Django + React Developer** — el combo real y demostrado.
2. Sistemas de gestión/dashboards para PyMEs — sinergia directa con PCfix.
3. Full Stack Node + React (librook/VI habilitan esto) para MVPs/SaaS chicos.

No priorizar por ahora: frontend puro sin backend (no aprovecha el diferencial real), ofertas genéricas sin filtro.

### Oferta de servicios freelance (definida con Berenice el 2026-08-20)

- **Capacidad real:** 5-10 hs/semana (además de su trabajo full-time y PCfix).
- **Clientes objetivo, en orden de prioridad:**
  1. PyMEs / comercios de Rosario — mismo público que PCfix, sinergia real de venta cruzada ("te arreglo la PC + te hago el sistema").
  2. Instituciones/organizaciones más grandes (tipo el hospital) — proyectos de mayor valor, venta más lenta y formal.
  3. Subcontratos para otros desarrolladores/agencias — pago probablemente menor por hora pero más constante, útil para llenar huecos de tiempo.
- **Idioma de mercado:** español / mercado local-LatAm por ahora — inglés técnico básico, no priorizar plataformas internacionales (Upwork, remoto en USD) hasta que mejore.
- **LinkedIn:** existe pero está abandonado — revivirlo es tarea del plan de 30 días, no crear uno nuevo.

**Servicios concretos a ofrecer** (based en el stack real demostrado, no genérico):
- Sistemas de gestión/backoffice a medida (inventario, turnos, clientes, reportes) — exactamente lo que ya demuestran stockToner y Glicemia.
- Desarrollo de dashboards con reportes exportables (Excel/PDF).
- APIs REST + integración de servicios externos.
- Mantenimiento/mejora de sistemas Django o React/Node existentes.

**Precio orientativo** (investigado en el mercado argentino 2026, no inventado — ver fuentes):
- Freelancers Django/React en Argentina cobran entre USD 20-45/hora según experiencia (semi-senior: USD 30-45/hora) — [fuente](https://cristiantait.com/blog/programador-web-freelance-argentina-2026), [fuente](https://julitaenremoto.com/cuanto-cobrar-freelancer-dolares-2026/).
- Un sistema de gestión a medida completo cuesta entre USD 2.500 (módulo básico) y USD 8.000 (ERP completo) — [fuente](https://studiox.com.ar/novedades/cuanto-cuesta-desarrollar-un-software-a-medida-en-argentina-en-2026).
- **Recomendación para arrancar (primeros 2-3 clientes, mientras arma su track record freelance formal):** por debajo del piso de mercado semi-senior pero sin subvalorar la evidencia técnica real —
  - Por hora (consultoría/subcontratos): **USD 15-25/hora**.
  - Sistema de gestión chico a medida (login + 1-2 módulos + reportes básicos, sin roles múltiples ni integraciones complejas): **USD 600-1.500** por proyecto, según alcance.
  - Subir estos números apenas tenga 2-3 testimonios/casos reales como freelance (no solo como empleada).

### Sobre automatizar la búsqueda en plataformas externas (nota crítica y honesta)

LinkedIn, Upwork, Workana, Indeed y Glassdoor **no tienen APIs públicas gratuitas de búsqueda de empleo y prohíben explícitamente el scraping en sus Términos de Servicio**. Construir un scraper para ellas violaría esos términos — no se va a hacer, coherente con la propia regla de Berenice de no saltarse restricciones de plataformas. Sí es viable, para más adelante: un motor de matching/scoring y un CRM freelance alimentado por ofertas que ella misma cargue manualmente, más investigar en su momento qué bolsas (RemoteOK, GetOnBoard, etc.) sí tienen RSS/JSON público.

---

## 3. PLAN

**30 días:**
- Semana 1: quick wins de perfil (arriba).
- Semana 1-2: definir con Berenice la oferta de servicios freelance explícita (qué vende, a quién, precio orientativo) — decisión que le corresponde a ella, no se inventa.
- Semana 2-3: publicar 1 case study narrativo (Glicemia) en LinkedIn u otro canal.
- Semana 3-4: empezar postulaciones activas a ofertas Django/Django+React (manual, hasta que exista el sistema de matching).

**90 días:**
- Sumar Docker documentado a al menos un proyecto.
- Sumar TypeScript a VI.
- Revisar resultados reales de postulaciones y ajustar posicionamiento según tasa de respuesta (Fase 9 del plan largo — aprendizaje).

---

## 4. ESTADO ACTUAL DEL PROYECTO

- **Fase 0 (Auditoría):** ✅ completa — 2026-08-20.
- **Fase 1 (Perfil profesional + Employability Score):** ✅ completa — 2026-08-21. LinkedIn revivido (título, bio, experiencia con los 4 proyectos reales incl. Vi, idiomas, destacados); inglés confirmado como intermedio; oferta de servicios ya estaba definida. Ver detalle en "LinkedIn revivido" más abajo.
- **Fase 2 (Job Discovery manual):** ✅ construida — 2026-08-21. Sección `/ofertas`: carga manual de ofertas/proyectos (sin scraping), con pipeline de estados (por postular → postulada → en conversación → ganada/rechazada/descartada).
- **Fase 2b (Ingesta automática de ofertas):** ✅ construida — 2026-09-09. Cierra el pendiente que había quedado abierto en la Fase 2 (las fuentes con API/RSS pública real). Detalle completo en "Ingesta automática" más abajo.
- **Fases 3-9** (Matching Engine, Application Generator, CRM de clientes, Client Prospecting, Analytics, Autopilot, Learning System): **no empezadas** — se construyen de a una. No construir todo de una vez (regla explícita del proyecto: evitar sobreingeniería). Ojo: el filtro de relevancia de la Fase 2b es un adelanto mínimo del Matching Engine (palabras clave, no un modelo), no la Fase 3 completa.

**IMPORTANTE — proyecto separado de PC Fix (2026-08-21):** este proyecto vive en su propia carpeta `GIT/work/Freelancer/`, con su propio código, su propia base de datos SQLite (`freelancer.db`) y su propio repo git — **no** dentro de `PCFIX/app/`. Al principio la Fase 2 se había construido por error adentro de la app de PC Fix (reusando su FastAPI, sus modelos y su base de datos); Berenice corrigió: "lo de pcfix va separado de freelancer son dos cosas distintas". Corre en `http://127.0.0.1:8002/` (PC Fix corre en el 8001). Sin login (herramienta personal de un solo usuario, corre solo en localhost).

**Arranque de un solo clic (2026-08-31):** en el Escritorio hay un acceso directo
`Buscador de Trabajo (Freelancer).lnk` que apunta a `iniciar_silencioso.vbs` (en esta
carpeta). Al hacer doble clic: si el servidor ya está corriendo en :8002 solo abre el
navegador; si no, lo levanta oculto (sin ventana de consola, vía `iniciar_oculto.bat`,
log en `uvicorn.log`) y recién ahí abre el navegador — nunca duplica el proceso. El
proceso queda corriendo independiente del acceso directo (no se cae si se cierra
Explorador ni nada relacionado al clic), solo se corta si se cierra manualmente desde
el Administrador de tareas o se reinicia la PC. `iniciar.bat` (con ventana visible)
sigue existiendo como alternativa manual para debug directo.

## 4bis. LINKEDIN REVIVIDO (2026-08-21)

Perfil: `linkedin.com/in/berenice-solohaga`. Cambios reales aplicados:
- Título: "Full Stack Developer · Django + React/Node · Sistemas en producción real — no solo proyectos de práctica".
- Bio ("Acerca de") reescrita con el posicionamiento y los 4 proyectos.
- Aptitudes: Programación, Desarrollo web, React.js, Django, Python (tope de 5 en destacadas).
- Idiomas agregados: Español (nativo), Inglés (básico limitado / intermedio).
- Experiencia: sacado YPF SA (dato viejo); "ReadMe App" renombrado a Librook con su stack real; agregado el puesto de Vi (jun. 2026, fecha real del primer commit en GitHub); sumada descripción de Glicemia + gestión de inventario y stock al puesto del Hospital Eva Perón.
- Educación corregida: "Tecnicatura Universitaria en Programación" (antes mezclaba español/inglés).
- Banner "En busca de empleo" (Europa) eliminado a pedido de Berenice.
- Destacados: publicado y fijado un case study narrativo sobre Glicemia (METANUTRIC), más un link a ailonline.com.ar.
- **Pendiente, en manos de Berenice:** el perfil tenía 1 solo contacto/seguidor — máximo problema de credibilidad actual. LinkedIn sugirió 4 compañeros reales de UTN (Belen Venturini, Valentino Appo, Daniza Paz, Lucas Rossi) para conectar. Berenice prefirió elegir ella misma a quién agregar, no automatizarlo.

---

## 4ter. INGESTA AUTOMÁTICA DE OFERTAS (2026-09-09)

Las ofertas ya no dependen de que Berenice las cargue a mano una por una: la app las
trae sola desde fuentes públicas. La carga manual sigue existiendo y no cambió (sirve
para lo que llega por LinkedIn, por un referido o por PC Fix).

### Fuentes conectadas (las 4 verificadas funcionando el 2026-09-09)

| Fuente | Canal | Por qué |
|---|---|---|
| **Get on Board** | API JSON `/api/v0/categories/programming/jobs` (con `expand[]=company`) | La más relevante: LatAm, muchos avisos en español, Chile/Argentina/Perú/Colombia. Es la que más aporta (35 de 42 en la primera corrida) |
| **Remote OK** | API JSON `/api` | Remoto internacional. El primer elemento del array es el aviso legal, no una oferta |
| **Remotive** | API JSON `/api/remote-jobs` | Remoto internacional. Catálogo chico (17 avisos totales al 2026-09-09) |
| **We Work Remotely** | Feed RSS de `remote-programming-jobs` | El título viene como "Empresa: Puesto" y hay que separarlo |

**Descartada: Arbeitnow** — su API pública funciona, pero es casi todo mercado alemán
y presencial en Alemania: aportaba ruido, no ofertas.

### Cumplimiento de los términos de cada plataforma (decisión, no detalle técnico)

Se mantiene la regla del proyecto de no scrapear. Todo lo conectado es API o RSS
**oficial y pública**, el canal que cada plataforma publica justamente para que
terceros redistribuyan sus avisos. Además:

- **Link de vuelta + atribución:** Remote OK y Remotive lo exigen en sus términos y
  amenazan con cortar el acceso si no se cumple. Cada ficha linkea al aviso original
  y muestra el nombre de la fuente.
- **Máximo una consulta cada 6 horas por fuente:** Remotive pide explícitamente no
  pasar de 4 consultas por día. La espera se guarda en la tabla `estado_fuentes` y la
  respeta tanto el botón manual como el refresco automático.
- **No republicar hacia afuera:** Remotive prohíbe reenviar sus avisos a terceros.
  Esta app es local, de un solo usuario, sin publicación externa — no hay conflicto.

### Cómo funciona

1. **Se busca sola cada 6 horas** (tarea en segundo plano que arranca con la app,
   `app/main.py`), y también a demanda con el botón "Buscar ahora".
2. **Filtro de relevancia** (`app/services/relevancia.py`) contra el perfil real de
   este documento: suma por Django/React/Node/Python, por part-time o freelance
   (capacidad real 5-10 hs/semana), por LatAm o español; resta por seniority alta,
   stack ajeno (.NET, Java, PHP), rol no técnico y frontend puro sin backend. Lo que
   queda por debajo de 25 puntos **se descarta sin guardarse**.
3. **Bandeja de entrada:** lo que pasa el filtro entra con estado `nueva`, ordenado
   por puntaje. Berenice decide con dos botones: "Me interesa" (pasa a `por_postular`
   y entra al pipeline de siempre) o "No me sirve" (`descartada`).
4. **Nada se repite:** la deduplicación es por fuente + id externo, así que una oferta
   ya descartada no vuelve a aparecer en la siguiente búsqueda.

**El filtro es por palabras clave, no un modelo de IA.** Puede dejar pasar ruido y
puede descartar algo bueno; conviene mirar las fuentes directamente cada tanto. Los
pesos están en `relevancia.py` y se ajustan ahí.

### Archivos nuevos

```
app/services/
├── relevancia.py          # puntaje contra el perfil
├── ingesta.py             # orquesta, deduplica, respeta la espera
└── fuentes/
    ├── base.py            # OfertaExterna, limpieza de HTML, pedidos HTTP
    ├── getonbrd.py  remoteok.py  remotive.py  weworkremotely.py
```

Modelo ampliado (`origen`, `id_externo`, `descripcion`, `ubicacion`, `salario`,
`etiquetas`, `puntaje`, `fecha_publicacion`) más la tabla `estado_fuentes`. Como el
proyecto no usa Alembic, `app/database.py` suma las columnas faltantes en cada
arranque con `ALTER TABLE ADD COLUMN` (SQL estándar, sirve también para PostgreSQL).

**Sumar una fuente nueva:** crear un módulo en `fuentes/` con `NOMBRE`, `ETIQUETA`,
`SITIO`, `HORAS_ENTRE_CONSULTAS` y `obtener()`, y agregarlo a la lista de
`fuentes/__init__.py`. Nada más.

**Tests:** 58 en total (`pytest tests/`), ninguno sale a internet. Cubren el filtro de
relevancia, el parseo de cada fuente, la deduplicación, la espera entre consultas, que
una fuente caída no frene a las demás, la migración de columnas y las rutas.

---

## 5. DECISIONES TOMADAS

- 2026-08-20: se prioriza NO scrapear plataformas de empleo que lo prohíben en sus ToS (LinkedIn, Upwork, Workana, Indeed, Glassdoor). El sistema de búsqueda se diseñará alrededor de carga manual + fuentes con API/RSS pública reales, a definir en Fase 2.
- 2026-08-20: se recomienda posicionamiento "Full Stack Developer (Django + React/Node) con sistemas en producción real", pendiente de validación por Berenice.
- 2026-08-20: definida la oferta de servicios con Berenice — ver sección "Oferta de servicios freelance" arriba. Prioridad de clientes: PyMEs de Rosario > instituciones > subcontratos. Capacidad: 5-10 hs/semana. Mercado local/español (inglés técnico básico, no priorizar plataformas internacionales).
- 2026-08-21: modelo `OportunidadFreelance` (tabla `oportunidades_freelance`) agregado sin migración de alembic explícita — el proyecto ya depende de `Base.metadata.create_all` en el startup de la app para crear tablas nuevas (mismo patrón que el resto de los modelos).
- 2026-09-09: se conectan 4 fuentes públicas (Get on Board, Remote OK, Remotive, We Work Remotely) por API/RSS oficial. Se mantiene intacta la decisión de no scrapear: ninguna de estas plataformas lo prohíbe porque el canal usado es el que ellas mismas publican para redistribuir sus avisos.
- 2026-09-09: **Arbeitnow descartada** aunque su API funciona — es casi todo mercado alemán presencial, aportaba ruido.
- 2026-09-09: las ofertas importadas **no entran directo al pipeline** sino a una bandeja aparte (estado `nueva`). Si entraran como "por postular" se mezclarían decenas de avisos sin revisar con las postulaciones reales y el pipeline dejaría de ser confiable.
- 2026-09-09: el filtro de relevancia **descarta sin guardar** lo que no llega a 25 puntos. Se prefiere perder alguna oferta dudosa antes que volver la bandeja inusable — el umbral y los pesos se ajustan en `app/services/relevancia.py`.
- 2026-09-09: `create_all` no alcanzaba para las columnas nuevas (no toca tablas que ya existen). Se agregó `agregar_columnas_faltantes()` en `app/database.py`, que corre en cada arranque con `ALTER TABLE ADD COLUMN`. Sigue sin usarse Alembic: si en algún momento hace falta renombrar o borrar columnas, ahí sí habrá que incorporarlo.

## 6. LEARNING LOG

_(vacío — se completa cuando haya postulaciones reales y resultados que analizar)_

## 7. HISTORIAL DE POSTULACIONES

_(vacío — Fase 4 en adelante)_

## 8. MARKET INSIGHTS

_(vacío — se completa cuando se investigue mercado en Fase 2/6)_
