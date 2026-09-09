import os

from flask import Flask, render_template, request

from app import db
from app.services import reportes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_BASE_DATOS = os.path.join(BASE_DIR, "datos.db")

app = Flask(__name__, template_folder="ui/templates", static_folder="ui/static")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{RUTA_BASE_DATOS}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def formatear_moneda(valor: float) -> str:
    return "$ " + f"{valor:,.0f}".replace(",", ".")


app.jinja_env.filters["moneda"] = formatear_moneda

MAPA_COLORES_CATEGORIA = {
    "Indumentaria": "--serie-1",
    "Calzado": "--serie-2",
    "Accesorios": "--serie-3",
    "Hogar y Deco": "--serie-4",
    "Tecnología": "--serie-5",
}


@app.route("/")
def panel():
    periodo = request.args.get("periodo", "90")
    if periodo not in reportes.PERIODOS_VALIDOS:
        periodo = "90"

    fecha_maxima = reportes.obtener_fecha_maxima()
    if fecha_maxima is None:
        return render_template("dashboard.html", sin_datos=True, periodos=reportes.PERIODOS_VALIDOS)

    fecha_desde, fecha_hasta = reportes.calcular_rango(periodo, fecha_maxima)
    agrupado_por_semana = periodo == "todo"

    pedidos = reportes._pedidos_en_rango(fecha_desde, fecha_hasta)
    kpis = reportes.calcular_kpis(pedidos)
    serie_ventas = reportes.ventas_por_periodo(pedidos, agrupado_por_semana)
    serie_categorias = reportes.ventas_por_categoria(pedidos)
    productos_top = reportes.top_productos(pedidos, cantidad=8)

    return render_template(
        "dashboard.html",
        sin_datos=False,
        periodo=periodo,
        periodos=reportes.PERIODOS_VALIDOS,
        kpis=kpis,
        serie_ventas=serie_ventas,
        serie_categorias=serie_categorias,
        productos_top=productos_top,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        agrupado_por_semana=agrupado_por_semana,
        mapa_colores_categoria=MAPA_COLORES_CATEGORIA,
    )


if __name__ == "__main__":
    app.run(port=5002, debug=True)
