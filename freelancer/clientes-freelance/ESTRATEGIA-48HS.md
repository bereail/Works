# Captación de clientes freelance — sprint de 48 horas

**Objetivo:** conseguir cliente(s) pagos por ARS 100.000-300.000 en las próximas 48
horas, con trabajos chicos y rápidos que Berenice pueda entregar de verdad con lo
que ya sabe hacer. **No es una estrategia de marca a largo plazo** — es para cerrar
la primera venta rápido. Fecha de arranque: 2026-09-11.

**Separado a propósito de `freelancer/app/` (búsqueda de empleo en relación de
dependencia/part-time) y de `pc-fix/` (el otro negocio) — ver `memoria/ESTADO_ACTUAL.md`
para no mezclar los tres.** Esta carpeta es solo la pata de "conseguir clientes que
paguen por trabajos freelance puntuales".

**Regla de esta carpeta, igual que el resto del repo (es público en GitHub):
nunca escribir acá nombres reales de clientes, teléfonos ni datos de contacto de
terceros.** Usar categorías, no nombres.

---

## 1. Oferta principal

> **Arreglo, mantengo y mejoro webs y sistemas ya existentes — rápido, con
> diagnóstico honesto antes de cobrar el trabajo grande.**

No es "te construyo un producto desde cero". Es entrar a algo que ya existe (una
web, un sistema, un proyecto que quedó a medias) y resolver un problema concreto:
un bug, un servidor que hay que dejar andando, una funcionalidad que falta, algo
que quedó lento.

## 2. Tres paquetes con precios (en pesos, foco en velocidad de cierre)

| Paquete | Qué incluye | Precio orientativo | Entrega |
|---|---|---|---|
| **1. Diagnóstico exprés** ("ojo técnico") | Reviso tu web/sistema y te entrego un informe corto: qué está pasando, qué se puede arreglar y cuánto costaría arreglarlo. Sin compromiso de nada más. | **ARS 60.000-80.000** | 24-48 hs |
| **2. Arreglo o mejora puntual** | Un bug concreto, una funcionalidad chica, una integración simple con una API externa, o una optimización de rendimiento puntual. | **ARS 120.000-220.000** según alcance | 2-5 días |
| **3. Puesta en marcha / mantenimiento** | Retomar un proyecto que quedó a medio hacer, dejarlo funcionando en un servidor real (Linux/Nginx), o dejar un sistema con mantenimiento correctivo al día. | **ARS 250.000-300.000** | ~1 semana |

**Por qué estos números y no otros:** están calculados para que un solo cliente del
Paquete 2 o 3 ya cubra el objetivo de 100-300k, sin inventar una tarifa por hora
nueva — es consistente con el piso ya definido en `FREELANCER_MASTER_CONTEXT.md`
(USD 15-25/hora para arrancar, sistema chico USD 600-1.500) llevado a un formato de
paquete cerrado, más fácil de vender rápido que "cotizame por hora".

**Movida más realista para 48hs:** el Paquete 1 es la puerta de entrada — es barato,
rápido y fácil de decir que sí. Cerrar uno o dos de esos hoy/mañana, y de ahí
convertir al menos uno en Paquete 2 o 3 en la misma semana.

## 3. Propuesta de valor (solo lo que se puede demostrar)

- **Sistemas reales en producción, no proyectos de práctica:** dos sistemas propios
  (Glicemia-Calculadora, StockFlow) se usan de verdad todos los días en un hospital.
- **Testing exhaustivo** en los 4 proyectos reales — poco común en un freelancer
  chico, y es la mejor garantía de que un arreglo no rompe algo más.
- **Deploy real de punta a punta:** servidor propio, `rsync`/`ssh`, CI/CD con GitHub
  Actions, no solo "funciona en mi máquina".
- **Diagnóstico antes de cobrar el trabajo grande:** el cliente no compra a ciegas —
  primero sabe qué tiene y cuánto sale, con el Paquete 1.
- Trato directo, sin agencia ni intermediarios de por medio.

**Lo que NO se dice porque no está demostrado:** experiencia previa retomando
proyectos de otros desarrolladores (los 4 proyectos reales los armó ella desde cero),
inglés avanzado, ni trabajo freelance pago anterior. Si en la conversación con un
cliente potencial surge alguna de estas preguntas, contestar la verdad — no improvisar
una respuesta que la comprometa después.

## 4. Qué proyecto de portfolio usar para demostrar cada capacidad

Los 4 proyectos reales primero (son la prueba más fuerte); las 3 piezas de
`portafolio-*` son **demos/simulaciones explícitamente marcadas como tales en su
propio README** — sirven para mostrar un patrón puntual, nunca presentarlas como
trabajo para un cliente real.

| Se pide... | Mostrar |
|---|---|
| Django | Glicemia-Calculadora o StockFlow (los dos en uso real en el Hospital Eva Perón) |
| React | VI o librook ([demo pública](https://ailonline.com.ar/vi/) / [demo pública](https://ailonline.com.ar/librook/), botón "Ver sin cuenta") |
| Node/Express + APIs propias | VI o librook |
| Integraciones con APIs externas | librook (OpenLibrary) o VI (TMDB) — reales. `portafolio-integracion-formulario-crm` como demo si hace falta mostrar el patrón formulario→CRM→notificación |
| Deploy / Linux / Nginx / servidor propio | VI y librook (VPS propio, `deploy.sh`, CI/CD con GitHub Actions) |
| Bases de datos (Postgres/SQLite) | VI y librook (Postgres), Glicemia (migración SQLite→Postgres) |
| Automatizaciones | StockFlow (automatiza inventario); `portafolio-bot-whatsapp` y `portafolio-integracion-formulario-crm` como demos del patrón formulario/pedido → proceso automático → notificación |
| Auditoría técnica | La metodología ya aplicada en la propia auditoría de perfil de GitHub (`FREELANCER_MASTER_CONTEXT.md`) — se puede ofrecer el mismo tipo de proceso sobre el sistema del cliente |
| Reparación de bugs / mejoras chicas / rendimiento | Cualquiera de los 4 reales, según el stack que use el cliente |
| Continuación de proyectos abandonados | **No hay un caso propio real de esto todavía** — no reclamarlo como experiencia. Se puede ofrecer igual (es una extensión directa de las otras capacidades), pero sin decir "ya hice esto antes" |

## 10. Tipos de clientes a contactar HOY (por velocidad de cierre, no por tamaño)

**PC FIX es un negocio aparte (reparación de PC/hardware) — sus clientes no son
leads de esto. No mezclar los dos públicos ni las dos ofertas.**

1. **Comercios/PyMEs de Rosario con web vieja, rota, o sin web** — visita en
   persona o WhatsApp directo, ofreciendo el Paquete 1 primero.
2. **Contactos personales/conocidos con negocio propio** — pedir referidos
   explícitamente ("¿conocés a alguien con una web o sistema que ande mal?").
3. **Grupos de Facebook/WhatsApp de comerciantes de Rosario** — publicar el
   mensaje corto (ver `mensajes-contacto.md`), ofreciendo el Paquete 1 primero.
4. **LinkedIn, 1er y 2do grado** — dueños de PyME o freelancers/agencias que
   subcontraten trabajo chico.
5. **Workana** — buscar específicamente ofertas de "arreglo de bug", "mantenimiento"
   o "mejora puntual", no proyectos grandes desde cero — mejor tasa de cierre en
   48hs y coincide con la oferta real.

---

Ver `mensajes-contacto.md` para los textos listos por canal.
