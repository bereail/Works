# Integración Formulario Web → CRM (con notificación automática)

Demo de portafolio que reproduce un flujo de automatización muy común en negocios reales: una **landing page** con formulario de contacto que, al enviarse, crea automáticamente un **lead** en un mini-CRM interno, dispara una **notificación** simulada y permite gestionar ese lead desde un panel sin recargar la página.

## ¿Qué hace el proyecto?

- **Formulario público (`/`)**: landing page de una consultora ficticia ("Nimbus Consultora") con un formulario de contacto (nombre, email, teléfono, empresa, mensaje y "cómo nos conociste"). Al enviarlo, se guarda el lead vía `fetch` (sin recargar la página) y se muestra una confirmación in-page animada, sin usar `alert()` nativo.
- **Panel CRM interno (`/panel`)**: tabla con todos los leads recibidos, ordenados por fecha (más reciente primero). Incluye:
  - Mini-KPIs con el total de leads y el conteo por estado (Nuevo / Contactado / Convertido / Descartado).
  - Buscador en vivo por nombre o email.
  - Cambio de estado por lead con un `<select>`, actualizado vía `fetch` (PATCH) sin recargar la página completa.
  - Actualización periódica automática de la tabla (polling) para reflejar nuevos leads.
- **Servicio de notificación (`app/services/notificaciones.py`)**: al crearse un lead, se ejecuta una función separada que simula el envío de una notificación (se loguea en consola y se guarda en la tabla `Notificacion`), demostrando el patrón **formulario → CRM → notificación** típico de una automatización real, sin depender de servicios externos.

## Stack

- **Backend**: Python 3 + Flask
- **Base de datos**: SQLite + SQLAlchemy (ORM, pensado para portar a PostgreSQL sin cambios de código)
- **Frontend**: HTML + CSS + JavaScript vanilla (fetch API), sin frameworks
- **Tests**: pytest (casos de servicios: alta de lead, notificación y cambio de estado)

## Estructura

```
portafolio-integracion-formulario-crm/
├── app/
│   ├── models/
│   │   └── lead.py          # modelos Lead y Notificacion (SQLAlchemy)
│   ├── services/
│   │   ├── leads.py         # lógica de negocio: registrar_lead, actualizar_estado_lead, listar_leads
│   │   └── notificaciones.py # simula el envío de notificación al crear un lead
│   ├── static/
│   │   ├── css/estilos.css
│   │   └── js/formulario.js, panel.js
│   ├── templates/
│   │   ├── formulario.html
│   │   └── panel.html
│   ├── rutas.py             # endpoints Flask (vistas + API JSON)
│   ├── main.py               # punto de entrada, corre en el puerto 5003
│   └── __init__.py           # application factory
├── tests/
│   └── test_leads.py
├── capturas/                  # screenshots para el portafolio
└── requirements.txt
```

## Cómo correrlo

```bash
cd portafolio-integracion-formulario-crm
pip install -r requirements.txt
python -m app.main
```

El servidor queda escuchando en **http://localhost:5003**:

- `http://localhost:5003/` → formulario público
- `http://localhost:5003/panel` → panel CRM interno

Para correr los tests:

```bash
python -m pytest tests/
```

La base de datos SQLite (`crm.db`) se crea automáticamente en el primer arranque.

---

### Descripción lista para pegar en Workana

> Desarrollo una integración automatizada entre un formulario web y un CRM propio: cada envío del formulario crea un lead en tiempo real, dispara una notificación automática y queda disponible en un panel de gestión con estados, KPIs y búsqueda — todo con actualizaciones parciales sin recargar la página. Construido en Python (Flask) con SQLAlchemy/SQLite, pensando en portabilidad hacia bases de datos en producción. Ideal como base para automatizar la captación de leads de cualquier landing page, sitio o campaña, conectándola a tu sistema de gestión interno.
