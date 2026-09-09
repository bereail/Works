# Deploy nuevo de Glicemia (METANUTRIC) — notas de continuidad

Palabra clave para retomar: **"GLICEMIA-DEPLOY"**

## Objetivo (pedido exacto de Berenice)
- NO tocar nada de la instancia actual: `http://138.36.238.175:8001/login`
- Crear un **nuevo** deploy del proyecto Glicemia-Calculadora
- Publicarlo en `ailonline.com.ar/glicemia`, **sin login**, como demo pública de prueba
- Actualizar el link "Ver demo" de la tarjeta de Glicemia en el home de ailonline.com.ar para que apunte ahí (no a la IP cruda)

## Accesos y credenciales relevadas en esta sesión
- **Servidor de Glicemia** (el de la demo actual):
  `ssh -p 5440 root@138.36.238.175` — contraseña **retirada de este archivo el
  2026-09-09 por seguridad** (había quedado en texto plano y el repo es público en
  GitHub). Hostname real del server: `vps-5945389-x` (confirma que es un VPS propio
  de Berenice, no infraestructura directa del hospital).
  ⚠️ **Pendiente crítico**: rotar esta contraseña (la vieja quedó expuesta en el
  historial de git) y pasar a auth por clave SSH (ya hay `~/.ssh/id_ed25519` e
  `~/.ssh/id_deploy_vi` generadas localmente, se podría agregar la pública a
  `authorized_keys` del server y desactivar password auth por completo).
  **Conexión probada y funcionando en su momento** (vía plink, ver nota técnica abajo
  — el comando de ejemplo también tuvo la contraseña retirada).

- **Servidor de ailonline.com.ar** (hosting de VI, Librook, etc.):
  `168.181.187.241`, puerto SSH `5442` (visto en `~/.ssh/known_hosts`).
  Se intentó conectar con `id_ed25519` e `id_deploy_vi` como `root` → **timeout**,
  no hay respuesta TCP desde esta red/máquina. El deploy real de ese server se hace
  vía GitHub Actions con secrets (`SSH_PRIVATE_KEY`/`SSH_HOST`/`SSH_PORT`/`SSH_USER`)
  que no se pueden leer vía `gh api`.

### Nota técnica: cómo conectar por SSH con contraseña desde esta máquina
Esta máquina (Windows, Git Bash) no tiene `sshpass`. Sí tiene PuTTY (`plink`) instalado.
Forma que funcionó:
```
"/c/Program Files/PuTTY/plink" -ssh -P 5440 -pw '[CONTRASEÑA RETIRADA — rotar y pasar a auth por clave SSH]' \
  -hostkey "SHA256:OfHg7+IL8FegUOkC2Ogc4SIZKGmOUJAYifXVPODtxR0" \
  -batch root@138.36.238.175 "comando a ejecutar"
```
(El `-batch` normal falla pidiendo confirmar el host key; hay que pasarlo explícito con `-hostkey`.)

## Repos locales ya clonados (relevante, no hace falta re-clonar)
- `C:\Users\bsolohaga\Desktop\bere\GIT\Glicemia-Calculadora` — código fuente Django del
  proyecto. Contiene `db.sqlite3` y `usuarios_dump.sql` **con datos reales** — nunca usar
  esos archivos para poblar la demo pública, hay que armar fixtures con datos ficticios.
- `C:\Users\bsolohaga\Desktop\bere\GIT\HostingAilonline` — código fuente de ailonline.com.ar
  (React, Create React App). Remote: `github.com/bereail/HostingAilonline`.
  - El array `DESTACADOS` en `src/pages/Home/Home.jsx` tiene la tarjeta de Glicemia con
    `links: [{ label: 'Ver demo', url: 'http://138.36.238.175:8001/login/?next=/', ... }]`
    — esto es lo que hay que cambiar a la nueva URL de demo una vez que exista.

## Hallazgo importante sobre el portfolio (corrige la auditoría anterior)
La rama actual es `ailonline-redesign` (no `main`), último commit 24/08 marcado **WIP**.
Ese commit YA agrega: bio ("Berenice Solohaga — Desarrolladora Full Stack" + tagline),
footer con GitHub/LinkedIn/mail de contacto, sección "Más detalles" expandible por
proyecto, y sección de stack tecnológico — o sea, varios de los gaps que se habían
señalado en la auditoría completa (falta de bio, falta de contacto) **ya están resueltos
en código**, simplemente no están mergeados a `main` ni desplegados todavía. La carpeta
`build/` está desactualizada (21/08, previa al commit del redesign).
El propio mensaje de commit dice qué falta antes de mergear: reverificar tema claro
end-to-end, responsive mobile, consola sin errores, y aprobación visual de Berenice.

También en ese `Home.jsx` ya está mapeado un proyecto "Bebi" con demo en
`ailonline.com.ar/bebi/` y un cliente "Portfolio · Rodrigo" en `ailonline.com.ar/rodrigo/`
— o sea el portfolio real (código) tiene más consistencia con lo que se ve en vivo de lo
que parecía al auditar solo el sitio ya publicado (viejo).

## Patrón de deploy existente (para modelar el de Glicemia)
Visto en `.github/workflows/deploy.yml` de VI y Librook (ambos Node, no Django):
- Build del frontend → `rsync` a `/var/www/html/<nombre>/` en el server de ailonline.
- Backend (si aplica) → `rsync` a `/var/www/<nombre>-api/`, reinicio con
  `systemctl restart <nombre>-api`.
- Todo corre por GitHub Actions, usando GitHub Secrets del repo (no visibles vía API).
- **Glicemia-Calculadora y StockFlow (ambos Django) solo tienen `tests.yml`, no
  `deploy.yml`** — no hay un pipeline de deploy automatizado ya armado para Django en
  esta infraestructura. Hay que crearlo desde cero, o hacer el deploy manual por SSH.

## Decisión pendiente para cuando retomemos
¿Dónde vive el nuevo demo de Glicemia?
1. **En el mismo server de Glicemia (138.36.238.175)**, en un puerto/instancia nueva
   (ej. gunicorn en :8002) sin tocar la de :8001, y después `ailonline.com.ar/glicemia`
   apunta ahí (reverse proxy o redirect) — más simple porque SÍ tenemos acceso SSH
   confirmado a este server.
2. **En el server de ailonline (168.181.187.241)**, replicando el patrón de VI/Librook
   bajo `/var/www/html/glicemia` + un proceso Django propio — más prolijo pero requiere
   acceso SSH a ese server que hoy no pudimos confirmar desde esta red.

Dado que HOY tenemos acceso confirmado solo al servidor de Glicemia (opción 1), el
camino más viable para arrancar es la opción 1, salvo que Berenice consiga después
acceso al server de ailonline (o corra el deploy ella vía GitHub Actions).

## Diseño del "modo demo sin login" (a definir con Berenice)
- Variable de entorno tipo `DEMO_MODE=1` que:
  - Carga fixtures con datos **ficticios** (nunca `db.sqlite3`/`usuarios_dump.sql` reales).
  - O bien desactiva `@login_required` en las vistas relevantes, o autologuea un usuario
    de demo de solo lectura.
- Mantener claramente separado del `settings.py` de producción real.

## Estado: DEPLOY DE BACKEND COMPLETADO (28/08/2026)

1. ~~Probar la conexión SSH~~ ✅
2. ~~Explorar el server~~ ✅ — **hallazgo clave: este VPS (138.36.238.175) ES el
   servidor real de ailonline.com.ar** (nginx sirve el dominio desde acá mismo, con
   SSL de Let's Encrypt). No es un servidor aparte del de VI/Librook — todo vive junto
   acá. `/etc/nginx/sites-available/ailonline` tiene un bloque por proyecto
   (`/glicemia/`, `/bebi/`, `/vi/`, `/librook/`, `/rodrigo/`, `/random/`, etc.)
3. ~~Confirmar arquitectura con Berenice~~ ✅ — confirmó repointear `/glicemia/` de
   nginx hacia la demo nueva, sin tocar el backend real en :8001.
4. ~~Diseñar y armar el modo demo sin login~~ ✅ — resuelto con un middleware propio
   (`DemoAutoLoginMiddleware`) que autologuea un usuario `demo` con los grupos
   `Enfermeria` + `Historial` (el control de acceso real de la app es por grupo, no
   solo login — `tiene_acceso_home`/`tiene_acceso_historial` en `views.py`). Sembradas
   6 mediciones de ejemplo con datos inventados.
5. ~~Deploy nuevo del backend~~ ✅ — **funcionando en producción**:
   - Código: clonado del repo público de GitHub (no de la carpeta real) en
     `/var/serverDeploy/glicemia_demo/` en el VPS.
   - Settings propios: `glicemia/settings_demo.py` (hereda de `settings.py`, agrega
     `FORCE_SCRIPT_NAME='/glicemia'`, `STATIC_URL='/glicemia/static/'` y el middleware
     de auto-login). Nada de esto toca el código/carpeta real (`glicemia_8010`).
   - Servicio systemd nuevo: `glicemia-demo.service`, gunicorn en `127.0.0.1:8002`
     (puerto libre, no interfiere con nada existente).
   - nginx: cambiado el bloque `/glicemia/` de `proxy_pass :8001` → `:8002`, y el
     alias de estáticos de una ruta rota (`glicemia_8001`, no existía) a la real
     (`glicemia_demo/staticfiles/`). Backup del config viejo en
     `/root/ailonline.nginx.bak.20260828110451` en el server. Validado con `nginx -t`
     antes de `systemctl reload nginx` (reload, no restart — no tocó otros sitios).
   - **Verificado**: `https://ailonline.com.ar/glicemia/` entra directo al calculador
     sin login, estáticos cargan bien, historial funciona. La instancia real en
     `http://138.36.238.175:8001/login` sigue exactamente igual, intacta, verificado.
   - Servicio viejo roto `glicemia8001.service` (186k reinicios fallidos, carpeta
     inexistente) — **no se tocó**, sigue ahí como estaba, ajeno a todo esto.

## Pendiente — actualizar el home (en curso)
- **Hallazgo importante**: lo que está deployado en `ailonline.com.ar` HOY no es la
  rama `ailonline-redesign` que se había visto antes (esa quedó como experimento
  paralelo, sin usar) — es la rama **`main`**, con su propia serie de commits más
  reciente (tema claro/oscuro, tags de tecnologías, SEO, footer con contacto por
  mail, StatuApp en vivo), último commit `0838464e` del 27/08. La auditoría anterior
  que decía "falta bio/contacto, está en una rama WIP sin mergear" ya no aplica tal
  cual — esa rama (`main`) ya tiene footer/contacto, solo faltaba corregir el link de
  Glicemia.
- Ya se editó `src/pages/Home/Home.jsx` en la rama `main` local (repo
  `C:\Users\bsolohaga\Desktop\bere\GIT\HostingAilonline`): la URL de Glicemia pasó de
  `http://138.36.238.175:8001/login/?next=/` a `https://ailonline.com.ar/glicemia/`.
- `npm run build` se lanzó y sigue corriendo en background al momento de guardar esta
  nota — falta: confirmar que terminó bien, deployar el `build/` resultante al server
  (`/var/www/html/ailonline-home/`, vía scp/rsync con plink dado que no hay acceso al
  pipeline de GitHub Actions desde acá), verificar visualmente el link nuevo en la
  home, y commitear + pushear el cambio de `Home.jsx` a GitHub (rama `main`).
- Nota: la carpeta `static/js/` del server tiene varios `main.*.js` de builds viejos
  sin limpiar (no rompe nada, cada deploy pisa `index.html`/`asset-manifest.json`
  apuntando al build correcto, pero acumula basura) — no es parte de esta tarea,
  mencionar si en algún momento se quiere limpiar.

## TAREA COMPLETA (28/08/2026)
1. ~~Build~~ ✅ compiló bien (`main.ff34c010.js`).
2. ~~Deploy del build~~ ✅ — subido vía `pscp` a `/root/ailonline-home-new/`,
   verificado el contenido, backup del sitio anterior, swap con `rsync -a --delete`,
   `chown www-data`. **Nota del incidente**: el primer intento de subida con
   `pscp -r .` dejó la carpeta destino vacía sin avisar (exit code 0 igual) — el swap
   con `--delete` borró el sitio real por unos segundos antes de que se notara. Se
   restauró al toque desde el backup. La segunda vez se subió listando cada
   archivo/carpeta explícitamente (no con `.`) y se verificó el contenido en el
   servidor ANTES de tocar producción — así se hizo bien. Para la próxima: siempre
   verificar `ls` en destino antes de cualquier `rsync --delete`.
3. ~~Verificar en el navegador~~ ✅ — `ailonline.com.ar` → tarjeta Glicemia → abre
   `ailonline.com.ar/glicemia/` directo al calculador, sin login.
4. ~~Commit + push~~ ✅ — commit `4e3a95af` en `bereail/HostingAilonline` rama `main`.
5. **Pendiente para Berenice**: rotar la contraseña root del VPS (la pasó en texto
   plano en el chat) y considerar pasar a auth por clave SSH.

## Estado final
- Demo pública funcionando: `https://ailonline.com.ar/glicemia/` (sin login, datos
  ficticios, separada por completo del sistema real).
- Sistema real intacto y verificado: `http://138.36.238.175:8001/login` sigue igual.
- Home de ailonline.com.ar actualizado y pusheado a GitHub.
- Limpieza pendiente (opcional, no urgente): quedaron backups en
  `/root/ailonline-home.bak.*` y `/root/ailonline-home.bak.*-v2` en el servidor, y
  varios `main.*.js` viejos sin usar en `/var/www/html/ailonline-home/static/js/` de
  deploys anteriores — no rompen nada, solo ocupan espacio.
