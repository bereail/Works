# Agentes de IA — diseño

**Objetivo:** definir qué agentes de IA tiene sentido construir de verdad, no solo listar roles.
**Estado:** Diseño completo. Depende de Etapa 6 (automatizaciones core) para los disparadores.

## Decisión de diseño: 3 agentes reales, no 12

En el pedido original se mencionaron doce roles de IA (recepción, ventas, marketing, SEO, diagnóstico, presupuestos, seguimiento, atención al cliente, redacción, publicidad, análisis, dashboard). Al tamaño actual del negocio (un solo operador, volumen bajo-medio), doce agentes separados serían **complejidad sin beneficio real**: cada uno es un punto más de mantenimiento, de costo de API, y de cosas que pueden romperse — sin que haya volumen que justifique separarlos. Se consolidan en tres, que cubren las mismas funciones:

### Agente 1 — Atención
Cubre: recepción, ventas de primer contacto, atención al cliente, seguimiento.
Es el motor de las automatizaciones 1, 3 y 6 de `08-Automatizaciones/01-AUTOMATIZACIONES-CORE.md`. Clasifica, responde lo repetitivo, escala a Berenice lo que tiene criterio o ticket alto de por medio.

### Agente 2 — Contenido
Cubre: marketing, redacción, publicidad, SEO.
Genera **borradores** de posteos, copys, respuestas a comentarios y textos de página — nunca publica solo. Todo pasa por revisión de Berenice antes de salir, porque la voz de marca (Fase 3) es parte del producto, no un detalle.

### Agente 3 — Análisis
Cubre: análisis de datos, apoyo de dashboard.
Una vez que haya suficiente volumen de tickets cargados (Etapa 9), ayuda a leer tendencias (qué servicio se vende más, qué canal trae mejores clientes, dónde se pierde tiempo) — no reemplaza el dashboard, lo explica en criollo cuando hace falta.

## Lo que deliberadamente NO se automatiza con IA

**Diagnóstico técnico.** Un agente de IA no le dice al cliente qué tiene la computadora en nombre de PC Fix. Eso sería automatizar exactamente lo que sostiene el posicionamiento de marca (Fase 3: "criterio técnico real") — si el diagnóstico lo pone una IA sin supervisión, la marca deja de tener la ventaja que la diferencia de la competencia relevada en Rosario. La IA puede *ayudar* a Berenice a redactar el diagnóstico en criollo para el cliente, pero el criterio técnico lo pone ella.

**Precio del presupuesto.** Mismo argumento que en la automatización 2: hasta no tener precios propios calibrados con datos reales de Rosario, el número lo pone una persona.

## Modelo de IA a usar

No hace falta el modelo más caro para todo:
- **Clasificación de mensajes, redacción de borradores, respuestas estándar:** un modelo liviano alcanza — incluso Ollama local (gratis, sin depender de una API paga) es candidato una vez que haya servidor propio (`DECISIONES-PENDIENTES.md`, punto 3).
- **Diagnóstico asistido, análisis de datos, casos donde el matiz importa:** ahí sí conviene un modelo de mayor calidad (Claude/GPT/Gemini vía API), porque el costo de un error es más alto que el costo de la llamada a la API.

Regla general: gastar en el modelo caro solo donde el error sale caro. En todo lo demás, priorizar la opción gratuita/open source, en línea con la preferencia general de evitar herramientas cerradas cuando hay alternativa.
