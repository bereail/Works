# AUDITORÍA DE GITHUB — Fotografía inicial (2026-08-11)

## 1. Perfil de GitHub (bereail)

Primera impresión de un recruiter con 60 segundos: **débil**. No transmite profesionalismo.

| Elemento | Estado actual | Problema |
|---|---|---|
| Foto de perfil | Avatar genérico | No hay foto/identidad visual |
| Bio | "⚛️ BERE bereail" | No dice qué hace, ni stack, ni rol |
| Ubicación | Rosario, Santa Fe, Argentina | OK |
| Links | Ninguno | Falta link a ailonline.com.ar, LinkedIn, etc. |
| README de perfil (bereail/bereail) | No existe | Gran oportunidad perdida — es lo primero que se ve |
| Pinned repos | e-commerce, statuapp, ReadMe-Fullstack-App, movieApp, Glicemia-Calculadora, Bebi | Mezcla proyectos de práctica (movieApp, ReadMe-Fullstack-App parecen tutoriales) con proyectos serios. `Bebi` tiene un problema grave de higiene de repo (ver abajo) y no debería estar pinneado tal cual. |
| Repos públicos totales | 18 | Ninguno archivado — hay duplicados visibles (3 repos de Glicemia) |
| Seguidores | 5 | No es prioritario |

**Pendiente:** esto se aborda en detalle más adelante en esta etapa (no es el primer repo, pero
es una mejora rápida y de alto impacto — se recomienda hacerla apenas se cierre el primer
repositorio auditado, para tener ya algo bueno que pinnear).

## 2. Inventario: local (`GIT/`) vs remoto (`github.com/bereail`)

### Repos con carpeta local Y remoto en GitHub (14)

| Repo | Visibilidad remota | Branch | Cambios sin commit | Último commit |
|---|---|---|---|---|
| ail | privado (no listado en API pública) | main | 1 | 2025-03-17 |
| Arbolada | público | main | 0 | 2026-06-24 |
| Bebi | público | main | 0 | 2026-07-31 |
| DB2 | privado (no listado) | main | 0 | 2025-06-06 |
| dnt-web | privado (no listado) | master | 1 | 2026-08-06 |
| Glicemia-Calculadora | público | main | 1 | 2026-07-21 |
| HostingAilonline | privado (no listado) | main | 6 | 2025-03-21 |
| librook | público | main | 24 | 2026-07-03 |
| plan-de-escape | público | main | 0 | 2026-07-24 |
| Portfolio | público | main | 1 | 2026-07-31 |
| Portfolio-Rodrigo | público | main | 0 | 2026-05-14 |
| statuapp | público | main | 0 | 2026-07-08 |
| stockTonerDesktop | privado (no listado) | main | 2 | 2026-07-30 |
| VI | público | main | 0 | 2026-07-30 |

> "Privado (no listado)" = no aparece en la API pública sin autenticación. Muy probablemente
> son repos privados en GitHub. A confirmar contigo si corresponde.

### Carpetas locales SIN git (5)

- `chatBot`, `PropuestaFichaArcade`, `Test` — a definir qué son y si se publican.
- `PCFIX` — proyecto de negocio (reparación de PCs), no es código de portfolio. Fuera de alcance de esta etapa.
- `work` — carpeta de trabajo miscelánea (flyers, borradores). No es un repositorio.

### Repos en GitHub SIN carpeta local en `GIT/` (9) — huérfanos remotos

`zkteco-f22`, `gameRos`, `Glicemia-Version-Estable`, `alboradaClaude`, `CasinoFlor`,
`Glicemia-CalculadoraNew`, `movieApp`, `ReadMe-Fullstack-App-Django-REST-React-`, `e-commerce`.

**Hallazgo importante:** existen **3 repositorios distintos de Glicemia** en GitHub
(`Glicemia-Calculadora`, `Glicemia-Version-Estable`, `Glicemia-CalculadoraNew`). Esto es
confuso para cualquiera que visite el perfil — no queda claro cuál es la versión "real". Hay
que consolidar en uno solo y archivar/eliminar los otros dos (con tu confirmación).

## 3. Hallazgos de seguridad (revisados 2026-08-11)

✅ **Buena noticia:** las bases de datos SQLite con datos reales (`db.sqlite3` en
`Glicemia-Calculadora`, `Arbolada`, `stockTonerDesktop`) están correctamente listadas en
`.gitignore` y **no están trackeadas en git**. No hay datos de pacientes ni datos de negocio
expuestos en los remotos por esta vía.

🔴 **Problema grave de higiene (no es un secreto, pero es una bandera roja fuerte):**
- **Bebi**: el entorno virtual completo de Python (`bebiwine/venv/`) está trackeado en git —
  6764 archivos versionados, la mayoría librerías de terceros. Además, el commit más reciente
  se llama *"Agregar .gitignore raíz para prevenir que se vuelvan a commitear secretos"*, lo
  que sugiere que en el historial pasado hubo secretos reales expuestos. **Pendiente crítico:**
  revisar el historial completo de Bebi antes de decidir si se sanea o se reescribe.
- **stockTonerDesktop**: mismo problema, `.venv/` trackeado — 10142 archivos versionados.

Ambos casos requieren limpieza del historial de git (remover la carpeta del venv de todos los
commits, no solo del último) antes de poder mostrarse como profesionales. Esto es un cambio
que reescribe historial — **se avisará y pedirá confirmación explícita antes de tocarlo**.

## 4. README — estado real por repo

| Repo | README | Calidad |
|---|---|---|
| statuapp | Sí, propio | Bueno — tiene demo online, descripción clara |
| dnt-web | Sí, propio | Básico — solo instrucciones de `npm run dev` |
| librook | Sí | Boilerplate de Vite sin personalizar |
| Portfolio-Rodrigo | Sí | Boilerplate de Vite sin personalizar |
| HostingAilonline | Sí | Boilerplate de Create React App sin personalizar |
| ail, Arbolada, DB2, Glicemia-Calculadora, plan-de-escape, Portfolio, stockTonerDesktop, VI | No | Sin README |

**8 de 14 repos no tienen README real.** Este es el problema más grave y más rápido de
resolver de toda la auditoría.

## 5. Clasificación preliminar por nivel

> Clasificación de primera pasada, a nivel de "fotografía". Se ajusta a medida que se audita
> cada repo en profundidad (Etapa 7 del proceso: código, arquitectura, tests, etc.)

### NIVEL A — Portfolio principal (candidatos)
- **Glicemia-Calculadora** — proyecto médico serio, prioridad explícita de Berenice. Necesita README, tests, demo, consolidación (hay 2 duplicados en GitHub).
- **statuapp** — ya tiene demo online y buen README. El más cerca de "terminado".
- **VI** — tiene screenshots ya generados, tests (`verify.mjs`), workflow de GitHub Actions.
- **librook** — stack sólido (React + Vite + Supabase), pero 24 cambios sin commit y README sin personalizar.

### NIVEL B — Portfolio secundario
- **dnt-web** — e-commerce con stack moderno (Next.js 16, TS, Tailwind), buena vidriera de frontend.
- **Portfolio-Rodrigo** — trabajo freelance real para un cliente.
- **Arbolada** — Django, a auditar en profundidad (sin README aún).
- **stockTonerDesktop** — app de escritorio con Django embebido, buena idea de producto, pero requiere limpieza grave de historial primero.

### NIVEL C — Académico / histórico
- **DB2** — carpetas "PARCIAL1", "PARCIAL2", claramente contenido de facultad. Mantener pero no destacar.

### NIVEL D — Requiere decisión (archivar / rehacer / no publicar tal cual)
- **ail** — sin README, estructura confusa (mezcla proyectos anidados).
- **HostingAilonline** — README default sin personalizar, commit único de 2025.
- **Portfolio** — parece ser el sitio comercial de ailonline, no un "portfolio de programadora" — a aclarar su propósito real.
- **plan-de-escape** — nombre y contenido (PDFs) poco claros, a investigar de qué se trata.
- **Bebi** — bloqueada por el problema de seguridad/higiene de git hasta sanear el historial.

### Repos remotos huérfanos (sin carpeta local)
Pendiente decisión: archivar o eliminar en GitHub `zkteco-f22`, `gameRos`,
`Glicemia-Version-Estable`, `alboradaClaude`, `CasinoFlor`, `Glicemia-CalculadoraNew`,
`movieApp`, `ReadMe-Fullstack-App-Django-REST-React-`, `e-commerce` — varios son claramente
duplicados o ejercicios de tutorial que no aportan a la imagen profesional.

## 6. Visibilidad — estado final tras autenticación (2026-08-11)

Con `gh` CLI autenticado como `bereail` se ve el inventario completo real: **46 repos**, no 18
(la API pública sin login solo mostraba los que ya eran públicos). Se aplicó el criterio
"público solo lo que ya suma como carta de presentación; todo lo demás, privado hasta que se
audite":

**Públicos (6):** Arbolada, Glicemia-Calculadora, librook, Portfolio-Rodrigo, statuapp, VI.

**Pasados a privado en esta sesión:** Bebi, DB2, plan-de-escape, Portfolio (confirmado por
Berenice que no es su web real), Glicemia-Version-Estable, Glicemia-CalculadoraNew,
zkteco-f22, gameRos, alboradaClaude, CasinoFlor, movieApp,
ReadMe-Fullstack-App-Django-REST-React-, e-commerce.

**Repos privados adicionales descubiertos** (no estaban en el inventario porque no eran
visibles sin autenticación, y no tienen carpeta en `GIT/` local): `Control-Salud-Adulto-Mayor`,
`GenericAPI`, `HOLOS`, `HospitalComputos`, `MET-SIST1`, `MovieAPI`, `NEW_API_HEEP`,
`PARCIAL-DB`, `PPSPROYECT`, `PatrimonioHEEP`, `Programacion3UTN`, `ReactNativeCurso`,
`TPI-LAB4-ToDoList`, `TextEditorApp`, `UltracorWeb`, `UnipackWeb`, `UserDemoApi`, `WakeMap`,
`back-up-ultracor`, `bar-menus`, `book-store-personal`, `checkoutMP`, `tup-lc2-clima-app`.
Varios nombres sugieren proyectos del ámbito hospitalario/laboral — ya estaban privados, no se
tocaron. Pendiente: decidir si alguno amerita clonarse localmente y evaluarse para portfolio,
o si quedan fuera del alcance de este proyecto por ser trabajo institucional.

**Pendiente:** `dnt-web` sigue privado — Berenice decidió esperar a que le toque su turno de
auditoría completa en el roadmap antes de hacerlo público, en lugar de exponerlo sin revisar.

## 7. Propuesta de orden de trabajo

1. **Glicemia-Calculadora** (primero — prioridad explícita, proyecto insignia)
2. statuapp (pulir lo que ya está cerca de listo)
3. VI
4. librook
5. dnt-web
6. Portfolio-Rodrigo
7. Arbolada
8. stockTonerDesktop (después de resolver el historial)
9. Bebi (después de resolver el historial)
10. Repos nivel C/D — decisión de archivar, ocultar o mejora mínima
11. Limpieza de repos huérfanos en GitHub
12. Cierre de perfil de GitHub (bio, foto, pinned, README de perfil)

Este orden se puede reordenar según lo que decidas, pero no se saltea el criterio de "cerrar
antes de pasar al siguiente" salvo razón técnica.
