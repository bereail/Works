from flask import Flask, jsonify, render_template, request

from app.models.lead import ESTADOS_VALIDOS
from app.services.leads import actualizar_estado_lead, listar_leads, registrar_lead


def registrar_rutas(app: Flask) -> None:
    @app.get("/")
    def formulario():
        return render_template("formulario.html")

    @app.get("/panel")
    def panel():
        return render_template("panel.html", estados=ESTADOS_VALIDOS)

    @app.get("/api/leads")
    def api_listar_leads():
        busqueda = request.args.get("q", "").strip()
        leads = listar_leads(busqueda)
        return jsonify([lead.a_diccionario() for lead in leads])

    @app.post("/api/leads")
    def api_crear_lead():
        datos = request.get_json(silent=True) or request.form

        campos_obligatorios = ["nombre", "email"]
        faltantes = [c for c in campos_obligatorios if not (datos.get(c) or "").strip()]
        if faltantes:
            return jsonify({
                "error": f"Faltan campos obligatorios: {', '.join(faltantes)}"
            }), 400

        lead = registrar_lead(datos)
        return jsonify(lead.a_diccionario()), 201

    @app.patch("/api/leads/<int:lead_id>")
    def api_actualizar_estado(lead_id: int):
        datos = request.get_json(silent=True) or {}
        nuevo_estado = datos.get("estado")

        if nuevo_estado not in ESTADOS_VALIDOS:
            return jsonify({"error": "Estado inválido"}), 400

        try:
            lead = actualizar_estado_lead(lead_id, nuevo_estado)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        if lead is None:
            return jsonify({"error": "Lead no encontrado"}), 404

        return jsonify(lead.a_diccionario())
