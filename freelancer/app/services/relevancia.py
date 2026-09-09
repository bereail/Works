"""Puntaje de relevancia de una oferta contra el perfil real de Berenice.

Es un filtro por palabras clave, no un modelo de lenguaje: cuenta señales del
perfil documentado en FREELANCER_MASTER_CONTEXT.md y suma o resta puntos. Sirve
para que la bandeja de entrada no se llene de avisos de .NET, marketing o
puestos senior, pero no reemplaza leer el aviso.

Criterios que vienen del master context (no inventados):
- Stack real demostrado: Django, React, Node/Express, PostgreSQL, testing.
- Priorizar Django / Django + React y full stack Node + React.
- No priorizar frontend puro sin backend.
- Mercado español / LatAm por sobre plataformas internacionales en inglés.
- Capacidad real de 5-10 hs/semana: part-time, freelance y por proyecto valen más
  que un full-time en relación de dependencia.
"""

import re

from app.services.fuentes.base import OfertaExterna

PUNTAJE_MINIMO = 25

STACK_NUCLEO = {
    "django": 25,
    "python": 18,
    "react": 18,
    "node": 15,
    "express": 12,
    "fastapi": 12,
    "full stack": 15,
    "fullstack": 15,
    "full-stack": 15,
    "postgres": 8,
    "postgresql": 8,
    "typescript": 8,
    "javascript": 8,
    "sqlalchemy": 8,
    "rest api": 6,
    "backend": 8,
    "back-end": 8,
}

SENALES_EXTRA = {
    "testing": 5,
    "pytest": 6,
    "vitest": 6,
    "playwright": 6,
    "dashboard": 6,
    "sistema de gestion": 8,
    "backoffice": 6,
    "reportes": 4,
}

MODALIDAD_COMPATIBLE = {
    "part-time": 20,
    "part time": 20,
    "medio tiempo": 20,
    "freelance": 18,
    "contract": 12,
    "por proyecto": 15,
    "por horas": 15,
    "hourly": 10,
}

MERCADO_CERCANO = {
    "argentina": 15,
    "latam": 12,
    "latin america": 12,
    "rosario": 15,
    "chile": 6,
    "uruguay": 6,
    "colombia": 6,
    "peru": 6,
    "mexico": 6,
    "spanish": 8,
    "espanol": 8,
}

SENIORITY_ALTA = {
    "senior": 12,
    "lead": 15,
    "tech lead": 15,
    "principal": 15,
    "staff engineer": 15,
    "architect": 15,
    "arquitecto": 15,
    "head of": 20,
    "manager": 15,
    "director": 20,
    "cto": 20,
}

STACK_AJENO = {
    ".net": 20,
    "c#": 20,
    "php": 18,
    "laravel": 18,
    "ruby": 18,
    "rails": 18,
    "golang": 15,
    "rust": 15,
    "scala": 15,
    "salesforce": 20,
    "sap": 20,
    "abap": 20,
    "cobol": 20,
    "wordpress": 15,
    "drupal": 15,
    "java": 15,
    "kotlin": 12,
    "flutter": 10,
    "android": 10,
    "ios": 10,
    "sharepoint": 15,
}

ROLES_AJENOS = {
    "designer": 30,
    "disenador": 30,
    "marketing": 35,
    "sales": 35,
    "ventas": 35,
    "recruiter": 35,
    "writer": 30,
    "copywriter": 30,
    "customer support": 30,
    "community manager": 35,
    "social media": 35,
    "social comms": 35,
    "content writing": 30,
    "seo specialist": 30,
    "accountant": 35,
    "contador": 35,
    "product owner": 20,
    "scrum master": 20,
    "data entry": 35,
}

# Estas fuentes son mercado internacional en inglés, que el master context pide no
# priorizar todavía (inglés técnico básico). No se descartan, pero pesan menos.
FUENTES_INTERNACIONALES = {"remoteok", "remotive", "weworkremotely"}


def contiene(termino: str, texto: str) -> bool:
    """Busca el término como palabra entera.

    Hace falta ser preciso: buscando la subcadena suelta, "java" matcheaba dentro de
    "javascript" y "lead" no matcheaba al final de "Technical Lead". Se usa
    lookaround en vez del borde de palabra de las regex porque varios términos
    empiezan o terminan con un símbolo (".net", "c#") y ahí ese borde no aplica.
    """
    patron = r"(?<!\w)" + re.escape(termino) + r"(?!\w)"
    return re.search(patron, texto) is not None


def calcular_puntaje(oferta: OfertaExterna, fuente: str = "") -> int:
    """Devuelve un puntaje de 0 a 100. Cuanto más alto, más se parece a lo que
    Berenice puede y quiere hacer."""
    titulo = oferta.titulo.lower()
    etiquetas = " ".join(oferta.etiquetas).lower()
    encabezado = f"{titulo} {etiquetas}"
    texto = oferta.texto_completo

    puntaje = 0

    # El stack pesa el doble si aparece en el título o en las etiquetas del aviso:
    # ahí describe el puesto, en la descripción puede ser solo un "nice to have".
    for termino, peso in STACK_NUCLEO.items():
        if contiene(termino, encabezado):
            puntaje += peso
        elif contiene(termino, texto):
            puntaje += peso // 2

    for diccionario in (SENALES_EXTRA, MODALIDAD_COMPATIBLE, MERCADO_CERCANO):
        for termino, peso in diccionario.items():
            if contiene(termino, texto):
                puntaje += peso

    for termino, penalidad in SENIORITY_ALTA.items():
        if contiene(termino, titulo):
            puntaje -= penalidad

    # El stack y el rol ajenos se miran también en las etiquetas: un aviso de
    # marketing puede tener un título neutro ("Social Comms") y delatarse ahí.
    for termino, penalidad in STACK_AJENO.items():
        if contiene(termino, encabezado):
            puntaje -= penalidad

    for termino, penalidad in ROLES_AJENOS.items():
        if contiene(termino, encabezado):
            puntaje -= penalidad

    if _es_frontend_puro(encabezado):
        puntaje -= 10

    if fuente in FUENTES_INTERNACIONALES:
        puntaje -= 5

    return max(0, min(100, puntaje))


def _es_frontend_puro(encabezado: str) -> bool:
    """Frontend sin backend no aprovecha el diferencial del perfil.

    Se mira solo el título y las etiquetas: en la descripción completa casi siempre
    aparece la palabra "api" y el chequeo nunca daría verdadero.
    """
    hay_frontend = any(contiene(t, encabezado) for t in ("react", "frontend", "front-end", "vue", "angular"))
    hay_backend = any(contiene(t, encabezado) for t in ("django", "python", "node", "express", "backend", "back-end", "api", "postgres", "full stack", "fullstack", "full-stack"))
    return hay_frontend and not hay_backend


def motivos(oferta: OfertaExterna) -> list[str]:
    """Las señales concretas que hicieron subir el puntaje, para mostrarlas en la
    ficha y que Berenice pueda entender por qué le llegó esta oferta."""
    texto = oferta.texto_completo
    encontrados = []
    for diccionario in (STACK_NUCLEO, MODALIDAD_COMPATIBLE, MERCADO_CERCANO, SENALES_EXTRA):
        for termino in diccionario:
            if termino not in encontrados and contiene(termino, texto):
                encontrados.append(termino)
    return encontrados[:8]
