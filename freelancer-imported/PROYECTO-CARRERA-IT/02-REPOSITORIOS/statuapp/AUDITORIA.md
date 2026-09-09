# AUDITORÍA — statuapp

Estado: 🟡 Mejoras de documentación implementadas y pusheadas — falta una acción de Berenice
en Netlify para quedar 🟢 LISTO PARA PORTFOLIO.

## Resuelto en esta sesión (2026-08-11)

- README reescrito con arquitectura real, cifra correcta de monumentos y capturas reales
  (commit `6481688`, pusheado).
- Imagen de screenshots falsa (generada por IA) reemplazada por 3 capturas reales.
- `package.json` corregido (`"portfolio"` → `"statuapp"`).
- 3 PDFs de trabajo interno sacados del repo (preservados en
  `02-REPOSITORIOS/statuapp/docs-internos-removidos/`).
- 2 commits que estaban solo en local (nunca pusheados) subidos a GitHub, tras confirmar que
  el build compila sin errores.
- Se aclaró que el backend "Django REST" que mencionaba el README viejo no existe como tal:
  la arquitectura real es Next.js full-stack con Netlify Blobs como almacenamiento.

## ⏸️ Pendiente — acción de Berenice, no técnica

El deploy de Netlify (statuapp3.netlify.app) está desactualizado respecto al código que ya
está en GitHub: sigue mostrando "Próximamente mapa interactivo" aunque el mapa está
implementado y pusheado desde antes de esta sesión. Sin acceso a la cuenta de Netlify no se
puede diagnosticar ni forzar el redeploy. Revisar en Netlify: Site settings → Builds → Trigger
deploy (o revisar si el deploy automático desde GitHub sigue conectado).

## Contexto del proyecto

Catálogo interactivo de estatuas y monumentos de Rosario. Frontend en Next.js 15 (App Router)
+ TypeScript + Tailwind, con panel de administración propio (auth por sesión firmada
HMAC-SHA256). El backend/API mencionado en el README (`statuapp.onrender.com`, Django REST)
no tiene repo local ni fue encontrado en el inventario de GitHub — a confirmar con Berenice
dónde vive ese código.

## 🔴 Hallazgos importantes

1. **La imagen de screenshots del README es generada por IA, con texto ilegible/inventado**
   (`docs/screenshots/statuapp_screens.png`): "Filttar" en vez de "Filtrar", "Majerial" en vez
   de "Material", oraciones sin sentido como "Viene del de una restatuá, clivida dei in
   gratua...". No son capturas reales de la app. Esto es grave para credibilidad — cualquier
   revisor técnico lo nota de inmediato. **Reemplazada por 3 capturas reales** tomadas
   navegando la demo online (home, explorar con fotos reales, hallazgo del mapa — ver punto 2).

2. **La demo pública (statuapp3.netlify.app) no refleja el código real del repo**: la sección
   "Mapa" muestra "PRÓXIMAMENTE MAPA INTERACTIVO", pero el código de `/mapa` (Leaflet,
   coordenadas reales desde la API) está implementado y en GitHub desde el commit `1ef6f76`.
   El deploy de Netlify parece desactualizado o desconectado del repo — **esto no lo puedo
   arreglar yo sin acceso a la cuenta de Netlify de Berenice**. Pendiente: que Berenice revise
   el deploy en Netlify (Site settings → Builds) y dispare un redeploy manual si hace falta.

3. **2 commits locales sin pushear** (había código más nuevo en la máquina que en GitHub):
   "Refactor de UI, catálogo ampliado y panel admin mejorado" y "Aplica sugerencias: fotos
   libres, coordenadas corregidas y limpieza". Ya pusheados en esta sesión, tras confirmar que
   el build (`npm run build`) compila sin errores.

4. **README describe una arquitectura de monorepo que no existe en este repo**: menciona
   carpetas `backend/`, `frontend/`, `db/` como si estuvieran todas en este repositorio, pero
   este repo es solo el frontend Next.js. Alguien que siga las instrucciones de instalación
   ("cd backend...") no va a encontrar esa carpeta. Hay que corregirlo para reflejar que es
   solo el frontend, con el backend deployado aparte.

5. **Número de monumentos exagerado**: el README dice "+1500 monumentos", pero el dataset real
   en el código (`app/src/data/statues/seed.ts`) tiene 27 estatuas con slug único. Hay que
   corregir la cifra a algo verificable.

6. **Commits de autor genérico**: 2 commits (los recién pusheados) quedaron con autor
   "Your Name <you@example.com>" por la configuración de git sin terminar de configurar en la
   máquina. Se corrigió la configuración global de git (ahora usa "Berenice Solohaga" +
   email noreply de GitHub) para que no se repita. Berenice decidió no reescribir esos 2
   commits puntuales (bloqueado además por el sistema de seguridad del agente).

## 🟡 Hallazgos menores

- `package.json` tiene `"name": "portfolio"` — genérico, debería decir `"statuapp"`.
- README tiene artefactos de copiar/pegar sin limpiar ("Copiar código" suelto, bloques de
  código mal cerrados) y un enlace roto a un video de YouTube sin URL real.
- No hay tests automatizados (a diferencia de Glicemia-Calculadora, que tiene 108).
- Hay 3 PDFs de trabajo en la carpeta `presentación/` (con espacio y tilde en el nombre) que
  no son código ni documentación de uso — a evaluar si conviene sacarlos del repo de código.

## ✅ Lo que está bien

- Sin secrets ni `.env` trackeados en ningún commit del historial.
- Arquitectura de autenticación del panel admin sólida: sesión firmada con HMAC-SHA256 usando
  Web Crypto API, compatible con Edge (middleware) y Node (route handlers) — buena señal
  técnica, vale la pena destacarla en el README.
- Stack moderno y bien elegido: Next.js 15, React 19, Radix UI, react-hook-form + zod,
  Leaflet, Resend.
- `.gitignore` correcto y completo.
- El build compila limpio, sin errores ni warnings relevantes.
- Demo real (una vez cargada) se ve prolija: buen copy, fotos reales de los monumentos,
  descripciones bien escritas.

## Puntaje

| Categoría | Puntos | Nota |
|---|---|---|
| Código | 20/25 | Buena arquitectura serverless, auth HMAC sólida, sin tests |
| Arquitectura | 13/15 | Next.js full-stack + Netlify Blobs, bien resuelto |
| README/documentación | 14/15 | Ahora preciso y completo |
| UI/UX | 8/10 | Diseño dark prolijo, visto en la demo real |
| Git/historial | 7/10 | Buenos mensajes en general, pero 7 commits "Update README.md" y 2 "build" sin contexto |
| Testing | 0/10 | Sin tests automatizados |
| Deploy/demo | 3/5 | Demo online existe pero desactualizada (falta redeploy en Netlify) |
| Seguridad/configuración | 5/5 | Sin secrets expuestos, auth propia bien implementada |
| Presentación visual | 4/5 | 3 capturas reales; podría sumar la ficha de detalle y el panel admin |

**Total: ~74/100.** Sube a ~85+ apenas Berenice resuelva el redeploy de Netlify.
