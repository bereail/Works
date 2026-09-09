# AUDITORÍA — stockTonerDesktop

Estado: 🟢 LISTO PARA PORTFOLIO — puntaje 85/100. Sigue **privado** (fuera del foco de los 4
repos objetivo hasta que Berenice pida hacerlo público).

## Contexto

App de escritorio (Django + pywebview + waitress, empaquetada con PyInstaller) para gestión
de inventario de insumos IT: tóners, PCs, impresoras, préstamos, reparaciones, pedidos.
Desarrollada por Berenice para su trabajo real como Analista de Sistemas.

## 🔴 Hallazgos críticos (resueltos, historial reescrito)

1. **Entorno virtual completo versionado**: `.venv/` con 9934 archivos (98% de los 10142
   archivos trackeados). El `.git` pesaba 54MB.
2. **`db.sqlite3` trackeado** a pesar de estar en `.gitignore` (se agregó al gitignore
   después de que ya estaba en el índice — el mismo patrón de error que en Glicemia). Contenía
   pocos datos (1 tóner, 1 servicio, 2 movimientos).
3. **Ejecutables de PyInstaller versionados** (`build/`, `dist/`): .exe de 8MB, DLLs, empaquetado
   completo de la app — no debían estar en git nunca (son artefactos regenerables).
4. **`inventario_data.json` con dump completo de datos operativos reales**: 21 servicios/sectores
   reales del hospital (Cirugía, Clínica Médica, DXI, Maternidad, etc.), 7 PCs, 6 impresoras,
   19 movimientos, entre otros. Trackeado en el HEAD actual, no solo en el historial viejo.
5. **13 capturas de pantalla en `screenshots/` con los mismos datos reales** (sectores del
   hospital visibles) — descubierto al revisar visualmente `servicios.png` y `dashboard.png`.

**Todo esto se resolvió reescribiendo el historial completo con `git-filter-repo`** (repo
privado, sin colaboradores — Berenice confirmó antes de proceder). El `.git` pasó de 54MB a
6.6MB. Se hizo backup del `.git` original antes de tocar nada, en
`02-REPOSITORIOS/stockTonerDesktop/git-backup-pre-filter-repo/`. Las 13 capturas viejas con
datos reales se preservaron fuera del repo en
`02-REPOSITORIOS/stockTonerDesktop/screenshots-con-datos-reales-hospital/`.

## 🟡 Hallazgos menores (resueltos)

- Sin README (agregado).
- Fixtures `inventario/fixtures/servicios.json` y `toners.json` estaban **rotos** (usaban
  campos de una versión anterior del modelo `Toner`) — hacían fallar `python manage.py seed`
  con `DeserializationError`. Corregidos con datos genéricos compatibles con el modelo actual.

## ✅ Muy bien

- **70 tests automatizados**, todos pasan.
- `SECRET_KEY` generada automáticamente por instalación y persistida fuera del repo (no
  hardcodeada).
- `DEBUG` se desactiva solo automáticamente cuando la app corre empaquetada (`.exe`) — buen
  criterio para una app de escritorio distribuida.
- Los datos reales (SQLite, backups) viven en la carpeta de datos de la aplicación del sistema
  operativo, completamente separados del repo — el diseño es correcto, el problema era solo
  higiene de git heredada de versiones viejas.
- Arquitectura dual bien pensada: mismo código sirve como app web (`runserver`) o como app de
  escritorio empaquetada (`pywebview` + PyInstaller).
- `seed.py` es idempotente (no siembra si ya hay datos).

## Cambios implementados (pusheados con `--force`, commit `cf98ff0`)

1. Historial completo reescrito (ver arriba).
2. README.md: qué resuelve, arquitectura web/escritorio, stack, instalación, testing.
3. 2 capturas nuevas con datos 100% ficticios (dashboard, tóner) — generadas corriendo la app
   localmente contra una base de datos temporal separada de los datos reales de Berenice.
4. Fixtures corregidos.
5. `.gitignore` reforzado (`inventario_data.json`, `*_data.json`).

## Puntaje

| Categoría | Puntos | Nota |
|---|---|---|
| Código | 21/25 | Buenas prácticas de configuración; el problema era solo el historial de git |
| Arquitectura | 14/15 | Dual web/escritorio bien resuelta |
| README/documentación | 14/15 | Completo |
| UI/UX | 8/10 | Dashboard prolijo y responsive, visto en la demo local |
| Git/historial | 7/10 | Limpio tras la reescritura; se descuenta por haber necesitado esta intervención |
| Testing | 10/10 | 70 tests, todos pasan |
| Deploy/demo | 3/5 | App de escritorio, no aplica demo online tradicional |
| Seguridad/configuración | 5/5 | SECRET_KEY, DEBUG y datos reales bien manejados tras la limpieza |
| Presentación visual | 3/5 | 2 capturas ficticias; podría sumar más módulos |

**Total: 85/100.**
