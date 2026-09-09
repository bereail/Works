"""Generador de flyers por composición de plantilla HTML/CSS renderizada a PNG.

No hay generación de imágenes por IA en esta fase: se compone una plantilla
propia con variables (titular, subtítulo, CTA), coherente con "no generar
diseños aleatorios sin analizar el historial" — el diseño es siempre el mismo
sistema visual, lo que cambia es el contenido.
"""

from pathlib import Path
from uuid import uuid4

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

DIR_PLANTILLAS = Path(__file__).resolve().parent / "plantillas_flyer"
DIR_SALIDA = Path(__file__).resolve().parent.parent / "ui" / "static" / "generados"
DIR_SALIDA.mkdir(parents=True, exist_ok=True)

_entorno = Environment(loader=FileSystemLoader(str(DIR_PLANTILLAS)))


def generar_flyer(
    titular: str,
    subtitulo: str,
    cta: str,
    nombre_comercial: str,
    tagline: str,
    color_primario: str,
    color_acento: str,
    plantilla: str = "estandar",
) -> str:
    """Renderiza el flyer y devuelve la ruta relativa del PNG generado (bajo /static/generados)."""
    plantilla_html = _entorno.get_template(f"{plantilla}.html")
    html = plantilla_html.render(
        titular=titular, subtitulo=subtitulo, cta=cta,
        nombre_comercial=nombre_comercial, tagline=tagline,
        color_primario=color_primario, color_acento=color_acento,
    )

    nombre_archivo = f"flyer_{uuid4().hex[:10]}.png"
    ruta_salida = DIR_SALIDA / nombre_archivo

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(viewport={"width": 1080, "height": 1350})
        pagina.set_content(html)
        pagina.screenshot(path=str(ruta_salida))
        navegador.close()

    return f"generados/{nombre_archivo}"
