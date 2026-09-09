# Decisiones pendientes

Las 7 quedaron resueltas el 5 de agosto de 2026. Documento se mantiene como registro histórico — si algo cambia (ej. te sacás el monotributo, aparece presupuesto de ads), se actualiza acá y se destraba la etapa correspondiente.

## 1. Tiempo real disponible por semana — ✅ Resuelto
**1 a 5 horas semanales.** Es poco, y cambia la prioridad real del roadmap: con tan poco tiempo, automatizar lo repetitivo (Etapa 6) deja de ser "una mejora" y pasa a ser la condición para que el negocio sea sostenible. Se ajusta la cadencia de contenidos (`05-Redes/PLAN-DE-CONTENIDOS.md`) para no comerse el poco tiempo disponible — 2 posts/semana ya es una porción grande de 1-5 horas totales, se revisa si hace falta bajarla a 1/semana en la práctica.

## 2. Dominio propio — ✅ Resuelto
`ailonline.com.ar/pcfix`. No prioridad de corto plazo.

## 3. Hosting / servidor — ✅ Resuelto
**Tu propia PC.** Gratis, arranca ya. Riesgo conocido y aceptado: las automatizaciones solo funcionan mientras la PC esté prendida y conectada — válido como punto de partida; se reevalúa un VPS si en algún momento eso empieza a generar problemas reales (ej. perder mensajes de WhatsApp por PC apagada).
**Destraba:** despliegue real de Etapa 6 y Etapa 9.

## 4. WhatsApp — ✅ Resuelto
**Evolution API**, self-hosted en la misma PC del punto 3. Gratis, open source.
**Destraba:** la automatización de WhatsApp (Automatización 1 de `08-Automatizaciones/01-AUTOMATIZACIONES-CORE.md`), que es la de mayor impacto dado el poco tiempo disponible (punto 1).

## 5. Situación fiscal — ✅ Resuelto
**Todavía no monotributo**, sigue informal por ahora. El módulo de Finanzas (`11-Finanzas/`) se construye igual, pero los números son para **uso interno/estimativo**, no para facturación oficial, hasta que eso cambie.

## 6. Presupuesto de publicidad paga — ✅ Resuelto
**$0 por ahora.** Se prioriza 100% orgánico (redes + boca en boca + SEO cuando se retome la Etapa 7). Etapa 10 queda formalmente en pausa por decisión propia, no por bloqueo — se retoma si en algún momento aparece presupuesto real para probar.

## 7. Modalidad de atención — ✅ Resuelto
**Retiro y entrega en un punto fijo** (no a domicilio). Ajusta:
- El manual operativo (`14-Procedimientos/MANUAL-FLUJO-OPERATIVO.md`) — recepción y entrega asumen que el cliente se acerca, no que Berenice viaja.
- La comunicación en redes y (a futuro) la web: hay que aclarar la dirección/punto de encuentro. **Confirmado (7 ago 2026): Olive 1200, Rosario, Santa Fe (CP S2013BMJ)** — es la dirección cargada en el Perfil de Negocio de Google (pendiente de verificación por Berenice). *Pendiente menor: confirmar si coincide con la dirección ya cargada en Meta Business.*

---

## Qué cambia ahora que está todo resuelto

Con esto, el diseño de las Etapas 6 y 9 pasa de "listo para desplegar cuando se decida" a **listo para desplegar, punto**. El próximo paso natural es empezar la implementación real (Docker, Postgres, n8n, Evolution API) en tu PC — eso ya es instalar y correr software de verdad en tu máquina, así que antes de tocar nada ahí te aviso el plan concreto y confirmo con vos, en vez de instalarlo directo.
