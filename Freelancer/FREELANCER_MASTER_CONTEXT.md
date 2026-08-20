# FREELANCER — Fuente de verdad

Este archivo es la única fuente de verdad del proyecto "Freelancer" de Berenice (carrera como Desarrolladora Full Stack, independiente de PCfix Informática). Cualquier conversación nueva sobre este tema debe empezar leyendo este archivo — no volver a pedirle que explique de nuevo su perfil, proyectos o estrategia.

**Regla de este archivo:** no duplicar información. Si un dato cambia, se actualiza acá mismo, no se crea una versión nueva.

Última actualización: 2026-08-20 (Fase 0 — Auditoría inicial).

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
| **stockTonerDesktop** | Django 5.2 embebido + pywebview + waitress, PyInstaller (.exe) | 70 tests | En uso real en el mismo hospital (inventario de insumos IT) |
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
- **stockTonerDesktop** — ⭐ STAR (caso de uso real, arquitectura de escritorio poco común como diferenciador).
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
- **Fase 1 (Perfil profesional + Employability Score):** parcial — score inicial calculado arriba, falta que Berenice confirme/corrija supuestos no verificables (LinkedIn, inglés, oferta de servicios).
- **Fases 2-9** (Job Discovery, Matching Engine, Application Generator, CRM, Client Prospecting, Analytics, Autopilot, Learning System): **no empezadas** — se construyen de a una, después de validar la Fase 1 con Berenice. No construir todo de una vez (regla explícita del proyecto: evitar sobreingeniería).
- En la app (`PCFIX/app/`), la sección "Freelancer" de `/inicio` existe como tile reservado ("Próximamente") — todavía sin código funcional.

## 5. DECISIONES TOMADAS

- 2026-08-20: se prioriza NO scrapear plataformas de empleo que lo prohíben en sus ToS (LinkedIn, Upwork, Workana, Indeed, Glassdoor). El sistema de búsqueda se diseñará alrededor de carga manual + fuentes con API/RSS pública reales, a definir en Fase 2.
- 2026-08-20: se recomienda posicionamiento "Full Stack Developer (Django + React/Node) con sistemas en producción real", pendiente de validación por Berenice.
- 2026-08-20: definida la oferta de servicios con Berenice — ver sección "Oferta de servicios freelance" arriba. Prioridad de clientes: PyMEs de Rosario > instituciones > subcontratos. Capacidad: 5-10 hs/semana. Mercado local/español (inglés técnico básico, no priorizar plataformas internacionales).

## 6. LEARNING LOG

_(vacío — se completa cuando haya postulaciones reales y resultados que analizar)_

## 7. HISTORIAL DE POSTULACIONES

_(vacío — Fase 4 en adelante)_

## 8. MARKET INSIGHTS

_(vacío — se completa cuando se investigue mercado en Fase 2/6)_
