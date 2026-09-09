# AUDITORÍA — Glicemia-Calculadora

Estado: 🟢 Auditoría en curso.

> **Actualización 2026-08-11:** Berenice confirmó que tiene autorización del hospital para
> publicar el protocolo institucional. Se mantiene la documentación tal cual está. No se
> elimina nada de `Info/`/`Test/` por este motivo.

## 🔴 HALLAZGO CRÍTICO — Documentación institucional del hospital, pública en GitHub

La carpeta `Info/` y `Test/` están **trackeadas en git y públicas** en el repositorio remoto.
Contienen:

1. **`Info/PROTOCOLO DE MANEJO DE LA GLUCEMIA E INSULINA EN NUTRICION CRITICA (1).pdf`**
   Es el documento OFICIAL del **Hospital Escuela Eva Perón**: código de gestión de calidad
   `04.USN.N09`, vigente hasta 31/12/2028, **autorizado por el Dr. Gonzalez Ariel — Dirección
   Médica**, con nombres del equipo que lo elaboró y revisó (personal del hospital). No tiene
   datos de pacientes, pero es documentación institucional interna con autorización formal
   de la Dirección Médica — publicarlo sin permiso del hospital es un riesgo real, más allá de
   que no haya PHI (datos de pacientes).

2. **`Info/Proyecto_MVP_Protocolo_Glicemia_UCI.docx`** — especificación del proyecto, dice
   explícitamente: *"Desarrollar una aplicación web interna (intranet hospitalaria)..."*.
   Confirma que el sistema fue pensado como herramienta interna del hospital, no como proyecto
   personal desde el origen.

3. **`Info/Pantallas-Referencias.docx`** y **`Test/pruebas_app_glicemia_protocolo.docx/pdf`**
   — documentación de reglas clínicas y plan de pruebas. **No contienen datos identificables
   de pacientes** (sin nombres, DNI ni historias clínicas reales) — son reglas genéricas de
   rangos de glucemia.

4. **`protocolos_glicemia.html`** (raíz del repo) — título "Protocolos de Control de Glicemia
   — UCI HEEP" (Hospital Escuela Eva Perón). Contenido institucional también.

### Lo que SÍ está bien
- `db.sqlite3` (que sí podría tener mediciones reales cargadas) está correctamente en
  `.gitignore` y NO está en el repositorio. No hay datos de pacientes en la base de datos
  expuestos.
- `django_errors.log` tampoco está trackeado (aunque conviene agregarlo explícitamente al
  `.gitignore`, ya que hoy no figura ahí y expone rutas locales del sistema).

### Por qué esto importa
No es un tema de "prolijidad de portfolio" — es un tema de **confidencialidad institucional**.
Aunque no haya datos de pacientes, publicar un documento con sello y autorización formal de la
Dirección Médica de un hospital, en un repositorio público a tu nombre, puede tener
consecuencias laborales si el hospital no autorizó esa publicación.

### Decisión pendiente (de Berenice, no técnica)
¿El hospital autorizó formalmente que este protocolo se use como base de un proyecto público
de portfolio? Si no hay autorización clara, la recomendación es sacar esos archivos del
historial de git (no solo del último commit) y reemplazar el protocolo real por una versión
**genérica/ficticia** ("Hospital Demo", protocolo inventado con rangos similares) para el
README y las demos — así el proyecto sigue siendo una pieza de portfolio igual de fuerte, sin
exponer nada institucional.

---

## Resto de la auditoría (preliminar, a completar tras resolver lo anterior)

### Código
- App `pacientes/` es boilerplate vacío (`models.py` y `views.py` sin contenido, sin URLs
  registradas) — código muerto, candidato a eliminar.
- `_inspeccionar_pdf.py` en la raíz: script de debug suelto, trackeado en git, usa `fitz`
  (PyMuPDF) que ni siquiera está en `requirements.txt`. Candidato a eliminar.
- `requirements.txt` está guardado en **UTF-16** (típico de `pip freeze` en PowerShell sin
  `-Encoding utf8`) — puede fallar al instalar en Linux/Mac. Hay que regenerarlo en UTF-8.
- `requirements.txt` incluye dependencias que no son de este proyecto (`PySide6`, `pyinstaller`,
  `mysql-connector-python`) — parece generado desde un entorno Python global compartido con
  otros proyectos (stockTonerDesktop), no un venv propio. Da una mala señal de manejo de
  dependencias; hay que regenerarlo desde un venv limpio.
- `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` se leen de variables de entorno — buena práctica.
- 131 commits, mayoría con buen estilo (`feat:`, `fix:`, `refactor:`, `docs:`) — señal
  profesional real. Hay algunos mensajes pobres ("info", "claude", "borrar", "Limpiar") pero
  no es grave en un proyecto de este tamaño.
- Suite de tests existe (`calculadora/tests.py`, se menciona "41 tests OK" en un commit) — hay
  que correrla y confirmar que sigue pasando.

### Documentación
- Sin `README.md`. Es el problema más visible del repo hoy.

### Arquitectura (revisado)
- Buena separación de capas: `views.py` (orquestación) → `services.py` (delgado) →
  `utils/logic/resolver.py` (lógica clínica pura) → `utils/ui/presentation.py` (formato para
  la vista) → `utils/reportes/` (Excel/PDF). Es una arquitectura más prolija que la de un
  proyecto de práctica típico — vale la pena mostrarla explícitamente en el README.
- Control de acceso por grupos de Django (`Enfermeria`, `Medicos`, `Historial`) con
  `@login_required` + `@user_passes_test` en cada vista — correcto.
- Detalle menor: hay una excepción de acceso hardcodeada a `username == "metanutric"` en
  `tiene_acceso_historial` — funciona, pero debería resolverse con un grupo, no un username
  literal. Bandera 🟡, no crítica.
- El modelo `MedicionGlucemia` se asocia al **usuario que carga la medición** (enfermero/médico),
  no a un paciente identificado por nombre — el sistema no almacena datos identificatorios de
  pacientes en la base. Buen punto a favor de privacidad.

### Tests (revisado)
✅ **108 tests, todos pasan** (`python manage.py test calculadora`, 33s). Esto es un
diferencial fuerte para portfolio — la mayoría de los proyectos de portfolio de candidatos no
tienen testing real. Hay que destacarlo explícitamente en el README.

### Git (revisado)
- Rama `metricas` está 100% mergeada a `main` (no tiene commits propios pendientes) — es rama
  vieja, se puede borrar sin pérdida de nada.
- 131 commits, buena convención (`feat:`/`fix:`/`refactor:`/`docs:`).

---

## Lista de problemas clasificados

🔴 **Crítico**
- Ninguno pendiente (el hallazgo institucional quedó resuelto con la confirmación de Berenice).

🟠 **Importante**
- No hay `README.md`.
- `requirements.txt` en UTF-16 con dependencias ajenas al proyecto (PySide6, pyinstaller,
  mysql-connector-python) — hay que regenerarlo desde un venv limpio, en UTF-8.
- Hay 3 repos de "Glicemia" en GitHub (`Glicemia-Calculadora`, `Glicemia-Version-Estable`,
  `Glicemia-CalculadoraNew`) — confuso, hay que decidir cuál es el oficial y archivar el resto.
- Sin demo online ni usuario de prueba documentado.
- Sin screenshots.

🟡 **Mejora**
- App `pacientes/` vacía y sin usar — código muerto, eliminar.
- `_inspeccionar_pdf.py` en la raíz — script de debug suelto, eliminar del repo.
- Excepción de acceso hardcodeada a `username == "metanutric"` — mover a grupo de Django.
- `django_errors.log` no está en `.gitignore` (no está trackeado, pero conviene agregarlo
  explícitamente para que nunca se suba por error).
- Rama `metricas` obsoleta — se puede borrar (local y remota) tras confirmar con Berenice.
- 1 cambio sin commitear pendiente en el working tree — revisar y decidir si se commitea.

🟢 **Excelente (mantener)**
- 108 tests automatizados, todos pasando.
- Arquitectura en capas (views → services → lógica pura → presentación) — mejor que el
  promedio de proyectos de portfolio.
- `SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS` vía variables de entorno.
- Control de acceso por grupos de Django.
- 131 commits con buena convención de mensajes.

## ✅ Hallazgo adicional — RESUELTO (2026-08-11)

`ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` en `glicemia/settings.py` tenían IPs reales de la red
del hospital y una IP pública hardcodeadas como valor por defecto. Berenice confirmó sacarlas
asumiendo el riesgo de que el servidor real deba tener las variables de entorno
`DJANGO_ALLOWED_HOSTS`/`DJANGO_CSRF_TRUSTED_ORIGINS` configuradas. Corregido y pusheado en el
commit `2af89998`.

## Plan de mejoras — estado de implementación (2026-08-11)

✅ Implementado (en el working tree local, staged con `git add`, **sin commitear todavía**):
1. README.md profesional con capturas, arquitectura, instalación, tests y disclaimer médico.
2. `requirements.txt` regenerado en UTF-8, verificado instalando en un venv limpio (108 tests OK).
3. Eliminados `pacientes/` (app vacía) y `_inspeccionar_pdf.py`.
4. `django_errors.log`, `*.spec`, `build/`, `dist/` agregados al `.gitignore`.
5. 5 capturas de pantalla reales tomadas corriendo la app localmente (login, control de
   glicemia, resultado de evaluación, historial, dashboard de métricas) — guardadas en
   `docs/screenshots/`.

✅ También resuelto:
- IPs hardcodeadas en `settings.py` — corregido, commit `2af89998`.
- Rama `metricas` (ya mergeada) — borrada local y remota.
- Commits `2af89998` y `cabd451e` pusheados a `main` en GitHub.

⏸️ Pendiente (decisión de Berenice):
4. Excepción hardcodeada `username == "metanutric"` — no se tocó, por el riesgo de romper
   acceso real si ese usuario no está en el grupo "Historial" en la base de producción.
8. Consolidar los 3 repos de Glicemia en GitHub — pendiente de autenticación con `gh` (login
   en curso, esperando confirmación de Berenice en el navegador).

## Plan de mejoras (propuesto, pendiente de aprobación para implementar)

1. Redactar `README.md` profesional: qué problema resuelve, para quién, arquitectura en capas
   (destacando los 108 tests), stack, instalación, variables de entorno, cómo correr los tests,
   captura de pantalla, y la aclaración de que es una herramienta de apoyo y no reemplaza
   criterio médico.
2. Regenerar `requirements.txt` desde un venv limpio del proyecto, en UTF-8.
3. Eliminar `pacientes/` (app vacía) y `_inspeccionar_pdf.py` (script de debug).
4. Mover la excepción de `username == "metanutric"` a un grupo de Django.
5. Agregar `django_errors.log` al `.gitignore`.
6. Tomar 4-5 screenshots de las pantallas principales (login, control de glicemia, historial,
   dashboard de métricas) para el README.
7. Decidir estrategia de demo: ¿usuario de prueba con contraseña segura documentada, o
   despliegue de una instancia demo online con datos ficticios?
8. Consolidar los 3 repos de Glicemia en GitHub — archivar `Glicemia-Version-Estable` y
   `Glicemia-CalculadoraNew` (a confirmar con Berenice cuál es realmente el más viejo/obsoleto).
9. Borrar la rama `metricas` (ya mergeada).

## Puntaje actualizado tras implementar el plan (2026-08-11)

| Categoría | Puntos | Nota |
|---|---|---|
| Código | 22/25 | Sin código muerto ni scripts sueltos. Queda pendiente el username hardcodeado. |
| Arquitectura | 14/15 | Separación en capas ejemplar para el tamaño del proyecto |
| README/documentación | 14/15 | README completo con arquitectura, instalación, tests y disclaimer |
| UI/UX | 8/10 | Diseño dark consistente y prolijo (visto corriendo la app), no se evaluó responsive/accesibilidad a fondo |
| Git/historial | 9/10 | Rama vieja borrada, commits claros y separados por tema |
| Testing | 10/10 | 108 tests, todos pasan |
| Deploy/demo | 2/5 | Usuario de prueba documentado en README, sigue sin demo online desplegada |
| Seguridad/configuración | 5/5 | Env vars, control de acceso por grupos, IPs internas ya no expuestas |
| Presentación visual | 5/5 | 5 screenshots reales de la app en funcionamiento |

**Total: ~89/100.** Puntaje inicial: 57/100. Pendiente para subir más: demo online desplegada
y resolver la excepción hardcodeada de `username == "metanutric"`.

## Estado final: 🟢 LISTO PARA PORTFOLIO (con una salvedad)

Cumple el estándar de "puede mostrarse a un recruiter y a un desarrollador senior". La única
salvedad pendiente es la consolidación de los 3 repos de Glicemia en GitHub (archivar los
duplicados), que depende de la autenticación con `gh` CLI.
