# Automatizaciones core — especificación

**Objetivo:** diseñar en papel cada automatización del manual operativo antes de tocar infraestructura real.
**Prioridad:** alta · **Estado:** Diseño completo. Despliegue real bloqueado por `DECISIONES-PENDIENTES.md` (puntos 3 y 4: hosting y WhatsApp Business API).
**Stack propuesto:** n8n (orquestador) + PostgreSQL (datos) + Evolution API (WhatsApp, open source) + Python/FastAPI donde n8n se quede corto + un modelo de IA (Claude/GPT/Gemini por API, u Ollama local para lo que no necesite el modelo más potente) + Docker para empaquetar todo.

Cada automatización sigue el mismo formato: disparador → flujo → qué reemplaza → por qué así.

---

## 1. Recepción y triage de WhatsApp

- **Disparador:** mensaje entrante al WhatsApp Business de PC Fix.
- **Flujo:** Evolution API recibe el mensaje → dispara un webhook a n8n → n8n busca o crea el cliente/ticket en Postgres → el texto pasa a un agente de IA con instrucciones de clasificar la consulta (reparación estándar / venta de hardware / consulta PyME-alto ticket / urgente / spam) y extraer datos si están (tipo de equipo, síntoma) → según la clasificación:
  - **Estándar:** el agente responde directo con los próximos pasos (qué datos manda el cliente), tono de marca de Fase 3, y guarda todo en el ticket.
  - **Urgente o PyME/alto ticket:** el agente NO responde solo — le avisa a Berenice (Telegram o su propio WhatsApp) con el resumen, para que tome la posta ella. Estas conversaciones son las que más valor tienen y las que más se benefician de atención personalizada real.
- **Qué reemplaza:** el primer mensaje repetitivo ("hola, ¿qué le pasa a tu compu?", "¿qué modelo es?") que hoy se escribe a mano cada vez.
- **Por qué así:** reduce el volumen de mensajes de bajo valor sin sacarle a Berenice el control de las conversaciones que sí importan — coherente con que ella quiere dedicar su tiempo a diagnósticos complejos y atención personalizada, no a chatear.

## 2. Generador de presupuesto

- **Disparador:** Berenice carga diagnóstico + ítems en un formulario simple (o directo en el futuro CRM).
- **Flujo:** n8n arma el presupuesto con la plantilla de marca (mano de obra separada de insumos, sin letra chica, tal como quedó definido en el manual operativo) → lo envía por WhatsApp/mail → actualiza el ticket a `presupuestado`.
- **Qué reemplaza:** escribir el presupuesto a mano cada vez, con formato inconsistente.
- **Nota importante:** el **monto** lo decide Berenice, no la IA — al menos hasta tener precios propios calibrados con el mystery shopping pendiente de Fase 2. Automatizar el número antes de tener criterio de precio propio sería automatizar un error.

## 3. Seguimiento de estado visible

- **Disparador:** cambio de estado del ticket.
- **Flujo:** n8n dispara un mensaje corto de WhatsApp en cada cambio relevante (`aceptado` → `en_reparacion` → `listo`), sin que Berenice tenga que redactarlo cada vez.
- **Qué reemplaza:** el "che, ¿cómo va mi compu?" que hoy interrumpe el trabajo técnico — y es, según el relevamiento de Fase 2, algo que ningún competidor de Rosario parece estar ofreciendo.

## 4. Control de calidad

- **Disparador:** Berenice intenta marcar un ticket como `listo`.
- **Flujo:** el sistema exige un checklist mínimo completo (enciende / problema resuelto / no se generó uno nuevo / datos intactos) antes de permitir el cambio de estado.
- **Qué reemplaza:** nada de IA acá — es disciplina de proceso forzada por el sistema, no una sugerencia que se puede saltear "por las dudas que hay apuro".

## 5. Entrega y garantía

- **Disparador:** ticket pasa a `entregado`.
- **Flujo:** n8n genera un comprobante de garantía (plantilla simple, PDF) con fecha de vencimiento según el alcance del trabajo, lo manda por WhatsApp/mail y crea el registro en la tabla `garantias`.
- **Qué reemplaza:** redactar y calcular la garantía a mano, con riesgo de olvidarla.

## 6. Seguimiento post-entrega + reseña

- **Disparador:** cron en n8n, X días después de `entregado` (valor a definir, por ejemplo 5–7 días).
- **Flujo:** mensaje automático preguntando cómo sigue el equipo → la respuesta se clasifica (positiva/negativa) → si es positiva, dispara automáticamente el pedido de reseña con link directo a Google Business Profile; si es negativa, notifica a Berenice para intervención manual — **nunca se pide reseña en automático a una respuesta negativa o dudosa.**
- **Qué reemplaza:** el seguimiento que hoy no se hace nunca, y que en Fase 1 se identificó como diferencial de confianza casi inexistente en la competencia.

## 7. Recomendaciones / venta cruzada

- **Disparador:** cierre del diagnóstico.
- **Flujo (arranca con reglas simples, sin IA todavía):** ejemplos — `tipo_disco = HDD` → sugerir upgrade a SSD; `origen = comercio/PyME` → sugerir plan de abono mensual. Se implementa como reglas fijas en n8n al principio; se puede sofisticar con IA más adelante si hace falta.
- **Qué reemplaza:** que la venta cruzada dependa de que a Berenice se le ocurra en el momento.

---

## Orden de implementación sugerido cuando se resuelvan las decisiones de infraestructura

1. Modelo de datos en Postgres (base de todo lo demás).
2. Automatización 1 (WhatsApp) — es la de mayor impacto inmediato en el pilar "experiencia de cliente".
3. Automatización 3 (seguimiento de estado) — bajo esfuerzo, alto impacto en confianza.
4. Automatización 6 (seguimiento + reseñas) — construye la prueba social que hoy falta (debilidad clave de Fase 1).
5. El resto (presupuesto, calidad, garantía, venta cruzada), en cualquier orden según lo que más fricción genere en el día a día real.
