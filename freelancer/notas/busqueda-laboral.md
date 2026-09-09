# Búsqueda laboral — estado general del proyecto

Palabra clave para retomar: **"BUSQUEDA-LABORAL"**
Última actualización: 2026-09-01

## Objetivo
Conseguir trabajo real (no solo "mejorar el perfil"): desarrolladora web / frontend /
backend / full stack, Python/Django, React, automatización/integraciones, freelance,
remoto, part-time, en Argentina y también internacional. Prioridad: aumentar
posibilidades reales de ser contactada, entrevistada y contratada.

## Estado por plataforma (28/08/2026)

### Workana — 90% completado
- Perfil: https://www.workana.com/freelancer/63d44d79f5345e56371c294576c18327
- Bio, título ("Scripting & Automations"), 3 habilidades (React Native, Python, Chatbot),
  idioma, historia laboral: todo cargado.
- "Proyectos destacados" cargados con datos reales (Librook, METANUTRIC, StockFlow, Vi).
- **Único bloqueante para el 100%: falta la foto de perfil** (+10%, es el único ítem del
  checklist con puntaje pendiente). Berenice no la tiene lista todavía, queda pendiente
  por su decisión — no insistir, retomar cuando la traiga.
- Detalle completo en memoria: [[workana_perfil_optimizacion]]

### LinkedIn — completo y activo
- https://www.linkedin.com/in/berenice-solohaga
- Foto real, headline fuerte, bio completa, 4 experiencias laborales, educación (UTN),
  15 habilidades, sección Destacado, 2 posts técnicos con buen engagement.
- **"Open to Work" activado (28/08/2026)**, visible solo para técnicos de selección
  (no para su empleador actual ni clientes). Configurado con cargos (Programador
  informático, Programador full stack, Desarrollador de Python), modalidad
  (presencial/híbrido/remoto), tipo de empleo (jornada completa + contrato por obra).
- Verificación de identidad de LinkedIn (proceso con documento + selfie vía app móvil,
  servicio "Persona") quedó **pendiente por decisión de Berenice** — no se puede hacer
  desde el navegador de escritorio, requiere el celular.

### GitHub — auditado (github.com/bereail)
- 5 repos públicos (bereail/bereail README de perfil + Glicemia-Calculadora + StockFlow
  + VI + librook), todos con licencia MIT, CI (tests.yml, algunos deploy.yml), 0 issues
  abiertos, buen volumen de commits, READMEs muy completos (problema → funcionalidades →
  capturas → arquitectura → notas de seguridad). Sin secretos filtrados (revisado).
- Repos privados relevantes: **StatuApp** (proyecto sólido, demo pública en Netlify, sin
  secretos, hoy oculto — candidato a hacerse público sin fricción). **Bebi** (mencionado
  en el portfolio con demo propia, pero el repo de GitHub no tiene ni descripción).
- Pendientes menores: nombre de perfil dice "BERE" en vez de "Berenice Solohaga", bio de
  GitHub cortada a la mitad.
- 🔴 Hallazgo crítico (en curso, ver abajo): el demo de Glicemia-Calculadora linkeaba
  a `http://138.36.238.175:8001/login` (HTTP sin cifrar, IP cruda, descripta como
  "instancia real del sistema"). Berenice confirmó que es SU VPS propio (no
  infraestructura del hospital), y pidió armar un nuevo deploy de demo sin login en
  `ailonline.com.ar/glicemia` sin tocar la instancia actual — **tarea en curso**, ver
  [[project_glicemia_deploy]] y el archivo `glicemia-deploy-notas.md` en esta misma
  carpeta.

### Portfolio (ailonline.com.ar) — auditado, con una sorpresa
- El sitio publicado hoy es minimalista: grilla de proyectos con tags de tecnología,
  sin bio, sin datos de contacto, sin footer.
- **Pero el código fuente local YA tiene la versión mejorada** (bio, footer con
  GitHub/LinkedIn/mail, detalle expandible por proyecto, sección de stack) en la rama
  `ailonline-redesign` del repo `HostingAilonline`
  (`C:\Users\bsolohaga\Desktop\bere\GIT\HostingAilonline`), commit del 24/08 marcado
  **WIP**, sin mergear a `main` todavía. El propio commit dice qué falta: reverificar
  tema claro, responsive mobile, consola sin errores, y aprobación visual de Berenice.
- Portfolio muestra 8 proyectos (incluye Bebi, Random, Portfolio-cliente/Rodrigo) que no
  aparecen en LinkedIn/GitHub — inconsistencia detectada. "Random" está literalmente
  etiquetado como "proyecto experimental de exploración y pruebas" — se recomendó
  sacarlo de la vista principal.

## Postulaciones enviadas
1. **Crossing Hurdles** — Full Stack Developer, contrato remoto, $65-120/hora, 10-40
   hs/semana. Postulada vía LinkedIn Easy Apply el 28/08/2026. Pendiente de respuesta —
   hacer seguimiento en LinkedIn > Mis empleos > Solicitados.
2. **InvGate** — Software Engineer - Python/Django, Argentina (híbrido/remoto según
   ubicación, oficinas en Belgrano CABA). Postulada vía Greenhouse el 31/08/2026, con
   el CV actualizado tras auditoría completa (ver `CV_Berenice_Solohaga_2026.pdf` en
   Descargas — reescrito con posicionamiento Backend Developer Python/Django, cargo
   real del hospital aclarado, clientes freelance reales nombrados). Confirmación
   recibida ("Thank you for your application!"). Pendiente de respuesta.
3. **BC Tecnología — Developer Back-end Python + FastAPI** — remoto, Semi Senior.
   Postulada vía Get on Board el 31/08/2026. Mejor fit de las tres de esta tanda
   (requisitos excluyentes: 2+ años Python, FastAPI, REST, SQL/NoSQL, Git — todos
   cubiertos). Pretensión declarada: 1350 USD bruto. Aclaró honestamente que su
   experiencia con FastAPI es de un proyecto personal de la facultad (API de turnos,
   con la autenticación como desafío principal), no de producción.
4. **Alluxi — Desarrollador Full-Stack Python/React** — remoto, Semi Senior,
   $1500-2000 USD/mes. Postulada vía Get on Board el 31/08/2026, en inglés (exigencia
   de la oferta). Riesgo identificado: el puesto exige inglés profesional y horario
   fijo US Eastern/Central full-time con cámara encendida; nivel de inglés declarado
   honestamente como Intermedio (B1), por debajo de lo pedido — postulada de todos
   modos por decisión de Berenice. Requirió conectar GitHub (bereail) vía OAuth a
   Get on Board, autorizado por Berenice en el momento.
5. **BC Tecnología — Full-Stack Developer Python Node.js** — remoto, Semi Senior.
   Postulada vía Get on Board el 31/08/2026 como opción de bajo costo/fit más débil:
   la oferta pide Angular (no React) y AWS avanzado (Lambda, Step Functions,
   EventBridge), que Berenice no tiene — se respondió con honestidad en las preguntas
   técnicas (sin Angular, sin AWS, dispuesta a aprender).
6. **Sophilabs — Fullstack Python/Django Developer** — remoto LatAm (incluye
   Argentina). Postulada el 01/09/2026 vía formulario directo en el sitio de la
   empresa (`sophilabs.com/careers/fullstack-pythondjango-developer-202608`),
   encontrada por LinkedIn Jobs y confirmada con "Thank you, your application was
   submitted successfully". Mejor fit de la tanda: LinkedIn marcó explícitamente que
   su perfil "cumple algunos requisitos indispensables" (a diferencia de otras
   descartadas), y tenía solo 16 clics de otros candidatos al momento de postular
   (baja competencia). Riesgo conocido: la oferta pide "Fluency in English is a
   must" y su nivel es Intermedio/B1. Se completó con nombre, mail
   (berenicesolohaga@gmail.com), celular (3413184829, confirmado por Berenice
   específicamente para esta postulación) y `CV_Berenice_Solohaga_2026.pdf`.
   Existe una variante **Back End Python/Django Developer** en la misma empresa (más
   pura en Django, 44 clics ya, descripción no se pudo verificar completa) que quedó
   como segunda opción a evaluar si esta no tiene respuesta en unos días — no
   postulada todavía por decisión de Berenice, para no duplicar con el mismo
   empleador de entrada.

Vacantes revisadas y descartadas en esta tanda por no calzar con la regla de "no
perseguir stacks que no tiene": **NTT DATA** (Full Stack Engineer Python — pedía
C#/.NET 8 pesado), **Perform** (Full Stack Developer Python — pedía AWS+Azure
hands-on, y LinkedIn marcó explícitamente "te faltan requisitos indispensables"),
**Oowlish** (Full Stack Web Engineer Python & React — +100 solicitudes, publicada
hace 2 meses, saturada).

**Seguimiento (01/09/2026):** Crossing Hurdles (vía LinkedIn) sigue sin respuesta,
4 días después la solicitud todavía figura como no vista por la empresa.

Get on Board: se pudo entrar finalmente usando el link mágico que la cuenta (registrada
con `bereailsolohaga@hotmail.com`, no vinculada a GitHub pese a que el botón de GitHub
aparece) manda por mail — el login con GitHub OAuth nunca funciona para esta cuenta,
solo manda un magic link. Las 3 postulaciones siguen en **ENVIADA**, 0 mensajes, sin
cambios desde el 31/08: BC Tecnología (Full-Stack Python Node.js), Alluxi (Full-Stack
Python/React), BC Tecnología (Back-end Python + FastAPI). También apareció una
postulación vieja no registrada antes: **Talana — Back-end Developer Python** (remoto
Chile, $1800-2500/mes), ahora **EXPIRADA** — confirmado con Berenice que es suya, de
antes de que se empezara a trackear esto en este archivo. Sin acción pendiente.

InvGate (Greenhouse) no tiene portal de candidato con login público — no se puede
chequear desde el navegador, solo llega novedad por mail.

Las tres de Get on Board se armaron subiendo `CV_Berenice_Solohaga_2026.pdf` como
nuevo CV del perfil (reemplazando uno anterior desactualizado que mencionaba
proyectos inexistentes como "StatuApp"/"ReadMe" en el texto guardado de experiencia).
El campo de experiencia y perfil profesional de Get on Board quedó reescrito
backend-first, coherente con el CV y la auditoría, y se guarda automáticamente para
próximas postulaciones en esa plataforma.

## Auditoría completa (resumen — la auditoría íntegra se hizo en el chat, no está
guardada palabra por palabra, pero estos son los puntos que hay que recordar):

**Posicionamiento recomendado, en orden:**
1. Full Stack Developer (Django + React/Node) con experiencia en producción real — es
   su headline actual, correcto.
2. Backend / Python-Django Developer.
3. Automatización / Integraciones (mejor para freelance/part-time).

**Diferencial real (con evidencia, no relato):** sistemas propios en uso real dentro de
un hospital (METANUTRIC en la UCI, StockFlow en IT), con tests automatizados,
trazabilidad y control de acceso por rol — no son proyectos de práctica. Es un
diferencial genuino frente a candidatas junior típicas.

**Puntajes (0-100) de la auditoría:** GitHub 78, LinkedIn 85, Portfolio 60, Calidad de
proyectos 85, Presentación profesional 70, Empleabilidad actual 75, Capacidad técnica
demostrable 82, Diferenciación 88, Probabilidad de conseguir entrevistas 70.

**Las 10 acciones de los próximos 30 días (de la auditoría):**
1. ~~Resolver el demo HTTP/IP de METANUTRIC~~ ✅ hecho (ver Glicemia deploy).
2. ~~Arreglar nombre y bio de GitHub~~ ✅ hecho (28/08) — "BERE" → "Berenice Solohaga",
   bio actualizada.
3. ~~Hacer público StatuApp~~ ✅ hecho (28/08) — y pineado entre los 5 destacados del
   perfil de GitHub.
4. ~~Portfolio con bio/contacto~~ — **ya estaba resuelto**, no en la rama vieja
   `ailonline-redesign` que se había visto antes, sino en `main` (la que realmente
   está deployada), con su propia serie de commits (tema claro/oscuro, SEO, footer con
   contacto). Verificado en vivo.
5. ~~Sacar "Random" del portfolio~~ ✅ hecho (28/08) — commit `225c30a1` en
   `HostingAilonline`, deployado y verificado en `ailonline.com.ar`.
6. ~~Decidir qué hacer con Bebi~~ ✅ decidido (28/08) — ver detalle abajo.
7. Postularse 3-5 vacantes de calidad por semana → **6 enviadas** (Crossing Hurdles,
   InvGate, BC Tecnología FastAPI, Alluxi, BC Tecnología Node.js, Sophilabs
   Fullstack) — meta semanal cumplida el 31/08/2026 y superada el 01/09/2026.
8. ~~Mandar 2-3 mensajes/semana a recruiters técnicos~~ ✅ hecho (01/09/2026) —
   3 solicitudes de conexión con nota personalizada enviadas por LinkedIn (todas en
   "Pendiente"): **Daniela Soto** (Talent Acquisition freelance, background en
   desarrollo web), **Joaquín Canciani** (IT Recruiter & Technical Sourcer, Rosario,
   foco en conectar talento LatAm con oportunidades globales — mismo ciudad que
   Berenice), **Federico Manes** (Senior Tech Recruiter en RUBICON, mercados US &
   LATAM). Los tres son contactos de 2º grado con conexiones en común. Nota: LinkedIn
   limita a 3 invitaciones personalizadas por mes en la cuenta free — se usaron las 3
   de este mes en esta tanda, no se puede mandar otra personalizada hasta el próximo
   ciclo (revisar fecha de reset si se quiere seguir el ritmo semanal).
9. ~~Publicar 1 post técnico más en LinkedIn~~ ✅ superado (01/09/2026) — Berenice
   publicó **dos** posts técnicos nuevos por su cuenta, no coordinados en este chat:
   "Turnero" (reserva de turnos con seña vía Mercado Pago Checkout Pro, Django +
   React/TS/Vite dockerizado, webhook que revalida contra la API de MP en vez de
   confiar en el POST, 10 tests aislados) y una función nueva de "Librook" (registrar
   libros leídos por voz/lenguaje natural, Web Speech API nativa sin IA paga, parser
   propio en español). Sumados al de METANUTRIC de la semana anterior, tiene 3 posts
   técnicos activos con buen engagement (43, 41 y 107 impresiones).
   **Turnero es un proyecto nuevo que no estaba auditado** — vale la pena sumarlo al
   portfolio/GitHub en algún momento, no se hizo hoy.
10. Completar verificación de identidad de LinkedIn (pendiente, decisión de Berenice).

**Nota técnica de deploy de ailonline.com.ar** (útil para la próxima vez que haya que
tocar el portfolio): el repo es `HostingAilonline` (Create React App), rama `main` es
la que está realmente en producción. Deploy manual desde esta máquina (no hay acceso
al pipeline de GitHub Actions): `npm run build` local → subir con `pscp` listando cada
archivo/carpeta de `build/` explícitamente (nunca `-r .`, dejó la carpeta destino
vacía sin avisar una vez) a una carpeta temporal en el servidor → **verificar el
contenido subido con `ls` antes de tocar nada** → backup de
`/var/www/html/ailonline-home` → `rsync -a --delete` desde la carpeta temporal →
`chown www-data:www-data`. Credenciales del servidor en `glicemia-deploy-notas.md`
(mismo VPS).

**Las 5 cosas que la auditoría dijo que NO hacer:** no construir proyectos nuevos, no
aprender tecnología nueva antes de postularse, no rediseñar el portfolio entero (solo
terminar lo que ya está en la rama WIP), no mandar mensajes genéricos masivos, no
perseguir vacantes que piden 10+ años o stacks que no tiene (Azure pesado, .NET).

## Bebi — decisión tomada (28/08/2026)

**Hallazgo de seguridad**: el repo `bereail/Bebi` (privado) tiene versionado
`bebiwine/db_export_deploy.json` — un export real de la base de datos de producción:
`auth.user` (4), `sessions.session` (3), `authtoken.token` (2), `vinos.vino` (19). Es
decir, usuarios reales, sesiones y **tokens de autenticación** quedaron en el
historial de git. También tiene una carpeta `bebiwine/libros/` que no tiene nada que
ver con vinos (resto de otro proyecto, sin limpiar).

**Decisión de Berenice**: dejar el repo privado tal como está, sin tocarlo. Si algún
día se quisiera hacer público, primero hay que purgar ese archivo del historial
completo (no alcanza con borrarlo en un commit nuevo) y rotar esos tokens.

**En el portfolio**: Bebi se queda como está hoy — solo la demo pública
(`ailonline.com.ar/bebi/`), sin link a "Ver código". No hizo falta ningún cambio, ya
estaba así.

**Cómo Berenice sigue cargando sus vinos** (no requiere ningún cambio, ya funciona):
el repo privado en GitHub no tiene ninguna relación con el funcionamiento de la app en
producción — son cosas independientes. La app Bebi ya tiene login y panel de admin
propios (`Login.jsx`, `MisVinos.jsx`, `NuevoVino.jsx`, `EditarVino.jsx`, todo detrás de
`ProtectedRoute`). Entra a **`ailonline.com.ar/bebi/login`** con su usuario para cargar
o editar vinos (`/mis-vinos`, `/nuevo-vino`, `/vinos/:id/editar`). Los visitantes desde
el portfolio solo ven la parte pública (`Home`, `Explorar`, fichas vía `/vino/:token`).

## Sub-proyectos activos
- **Deploy demo de Glicemia** — ✅ **completo** (28/08/2026). Nueva demo pública sin
  login en `ailonline.com.ar/glicemia`, con datos ficticios, sin tocar el sistema real
  (`138.36.238.175:8001`, verificado intacto). Home de ailonline.com.ar actualizado y
  pusheado a GitHub. Detalle completo en [[project_glicemia_deploy]] y
  `glicemia-deploy-notas.md` en esta carpeta. Pendiente: Berenice tiene que rotar la
  contraseña root del VPS (quedó en texto plano en el chat).

## Cómo retomar
Decir "sigamos con la búsqueda laboral" o la palabra clave "BUSQUEDA-LABORAL" alcanza
para que cualquier sesión futura lea este archivo primero y continúe sin repreguntar
nada ya resuelto acá.
