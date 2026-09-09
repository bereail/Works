# LOG DE DECISIONES

Registro cronológico de decisiones importantes tomadas durante el proyecto. Cada entrada:
fecha, decisión, motivo.

---

## 2026-08-11 — Kickoff del proyecto

- **Ubicación de la carpeta de proyecto:** se crea `PROYECTO-CARRERA-IT/` en
  `Desktop/bere/`, como hermana de `GIT/`, no dentro de ella. Motivo: `GIT/` debe contener
  únicamente repositorios de código; este proyecto es de gestión/documentación y no es un
  repositorio en sí mismo.
- **Alcance de esta etapa:** exclusivamente GitHub (perfil + repositorios). No se toca CV,
  portfolio, LinkedIn ni búsqueda laboral hasta que esta etapa esté cerrada.
- Se realizó inventario completo de `GIT/` (19 carpetas, 14 repos git) y se cruzó contra los
  repos públicos de `github.com/bereail` (18 públicos vía API). Ver detalle en
  `01-GITHUB/AUDITORIA-GITHUB.md`.
- **Documentación institucional del Hospital Eva Perón en Glicemia-Calculadora:** Berenice
  confirmó que tiene autorización del hospital para publicar el protocolo oficial (PDF con
  sello y autorización de Dirección Médica) y los documentos relacionados en `Info/`/`Test/`.
  Decisión: se mantienen esos archivos en el repositorio público, no se eliminan del
  historial. No volver a plantear esto como bloqueante en próximas sesiones.

## 2026-08-11 (continuación) — Desvinculación de la marca ailonline.com.ar

Berenice pidió sacar toda mención a `ailonline.com.ar` de sus repos de portfolio, para que no
queden asociados a su marca freelance. Alcance acordado:

- **Solo menciones cosméticas** (links de crédito en footers, README): se sacan.
- **Infraestructura real de deploy no se toca**: `Bebi`, `librook` y `VI` usan
  `ailonline.com.ar` como hosting real (ALLOWED_HOSTS, proxy de dev, URLs de reset de
  contraseña por email, deploy scripts). Tocar esto rompería el acceso real a esos sitios. Se
  deja así hasta que, repo por repo en su auditoría correspondiente, se decida migrar a otro
  hosting.
- **`Portfolio` (ailonline-home) no se toca**: ES el código fuente del sitio ailonline.com.ar
  en sí — no aplica desvincularlo de sí mismo. Ya está privado, fuera del alcance de esta
  limpieza.
- Ejecutado en `statuapp` (commit `c80e031`) y `Portfolio-Rodrigo` (commit `eec2fcb`): se
  reemplazó el link "Ailonline" del footer por el LinkedIn de Berenice Solohaga.
- **Regla para el futuro:** en todo README/footer nuevo que se escriba para estos repos de
  portfolio, usar LinkedIn o el nombre de Berenice como crédito, nunca ailonline.com.ar.
