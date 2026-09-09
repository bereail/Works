"""Cada fuente devuelve el JSON o el XML con su propia forma. Estos tests usan
respuestas de ejemplo con la estructura real de cada API (recortadas) para verificar
el mapeo, sin salir a internet."""

import pytest

from app.services.fuentes import getonbrd, remoteok, remotive, weworkremotely
from app.services.fuentes.base import limpiar_html


class TestRemoteOk:
    def test_saltea_el_aviso_legal_que_viene_primero(self, monkeypatch):
        """El primer elemento del array de Remote OK no es una oferta."""
        respuesta = [
            {"legal": "API Terms of Service: Please link back...", "last_updated": 1788834930},
            {"id": "123", "position": "Django Developer", "company": "Acme", "url": "https://remoteok.com/x"},
        ]
        monkeypatch.setattr(remoteok, "pedir_json", lambda *a, **k: respuesta)

        ofertas = remoteok.obtener()
        assert len(ofertas) == 1
        assert ofertas[0].titulo == "Django Developer"

    def test_arma_el_rango_de_salario(self, monkeypatch):
        respuesta = [{"id": "1", "position": "Dev", "salary_min": 90000, "salary_max": 150000}]
        monkeypatch.setattr(remoteok, "pedir_json", lambda *a, **k: respuesta)

        assert remoteok.obtener()[0].salario == "USD 90.000-150.000"

    def test_sin_salario_no_inventa_nada(self, monkeypatch):
        monkeypatch.setattr(remoteok, "pedir_json", lambda *a, **k: [{"id": "1", "position": "Dev"}])
        assert remoteok.obtener()[0].salario == ""


class TestRemotive:
    def test_mapea_el_aviso(self, monkeypatch):
        respuesta = {"jobs": [{
            "id": 2091045, "title": "Backend Developer", "company_name": "Unio",
            "url": "https://remotive.com/x", "candidate_required_location": "Worldwide",
            "tags": ["python", "django"], "publication_date": "2026-09-07T01:10:43",
            "job_type": "full_time",
        }]}
        monkeypatch.setattr(remotive, "pedir_json", lambda *a, **k: respuesta)

        oferta = remotive.obtener()[0]
        assert oferta.id_externo == "2091045"
        assert oferta.empresa == "Unio"
        assert oferta.etiquetas == ["python", "django"]
        assert oferta.fecha_publicacion.year == 2026

    def test_un_contrato_por_horas_se_marca_como_proyecto_freelance(self, monkeypatch):
        respuesta = {"jobs": [{"id": 1, "title": "Dev", "job_type": "contract"}]}
        monkeypatch.setattr(remotive, "pedir_json", lambda *a, **k: respuesta)

        assert remotive.obtener()[0].tipo == "proyecto_freelance"

    def test_respeta_el_limite_de_consultas_que_piden_sus_terminos(self):
        """Remotive pide un máximo de 4 consultas por día."""
        assert remotive.HORAS_ENTRE_CONSULTAS >= 6


class TestGetOnBoard:
    def _respuesta(self, **atributos):
        base = {
            "title": "Desarrollador Full-Stack", "description": "<p>Django y React</p>",
            "remote_modality": "fully_remote", "countries": ["Chile"],
            "published_at": 1788460925, "category_name": "Programming", "perks": ["flexible_hours"],
            "company": {"data": {"attributes": {"name": "TCIT"}}},
        }
        base.update(atributos)
        return {"data": [{"id": "dev-full-stack-tcit", "attributes": base}], "meta": {"total_pages": 1}}

    def test_extrae_el_nombre_de_la_empresa_expandida(self, monkeypatch):
        monkeypatch.setattr(getonbrd, "pedir_json", lambda *a, **k: self._respuesta())
        assert getonbrd.obtener()[0].empresa == "TCIT"

    def test_arma_la_url_del_aviso_con_el_identificador(self, monkeypatch):
        monkeypatch.setattr(getonbrd, "pedir_json", lambda *a, **k: self._respuesta())
        assert getonbrd.obtener()[0].url == "https://www.getonbrd.com/jobs/dev-full-stack-tcit"

    def test_combina_modalidad_y_pais_en_la_ubicacion(self, monkeypatch):
        monkeypatch.setattr(getonbrd, "pedir_json", lambda *a, **k: self._respuesta())
        assert getonbrd.obtener()[0].ubicacion == "Remoto - Chile"

    def test_una_empresa_sin_expandir_no_rompe_la_importacion(self, monkeypatch):
        monkeypatch.setattr(getonbrd, "pedir_json", lambda *a, **k: self._respuesta(company=None))
        assert getonbrd.obtener()[0].empresa == ""

    def test_corta_al_llegar_a_la_ultima_pagina(self, monkeypatch):
        llamadas = []

        def contar(*a, **k):
            llamadas.append(k.get("params"))
            return self._respuesta()

        monkeypatch.setattr(getonbrd, "pedir_json", contar)
        getonbrd.obtener()
        assert len(llamadas) == 1


class TestWeWorkRemotely:
    RSS = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0"><channel>
      <item>
        <title>Zeta Global: Senior Django Developer</title>
        <region>Anywhere in the World</region>
        <category>Full-Stack Programming</category>
        <description>&lt;p&gt;Buscamos alguien con Django&lt;/p&gt;</description>
        <pubDate>Tue, 18 Aug 2026 20:32:19 +0000</pubDate>
        <guid>https://weworkremotely.com/remote-jobs/zeta</guid>
        <link>https://weworkremotely.com/remote-jobs/zeta</link>
      </item>
    </channel></rss>"""

    def test_separa_la_empresa_del_puesto(self, monkeypatch):
        """En este feed el título viene como 'Empresa: Puesto'."""
        monkeypatch.setattr(weworkremotely, "pedir_texto", lambda *a, **k: self.RSS)

        oferta = weworkremotely.obtener()[0]
        assert oferta.empresa == "Zeta Global"
        assert oferta.titulo == "Senior Django Developer"

    def test_convierte_la_fecha_del_rss(self, monkeypatch):
        monkeypatch.setattr(weworkremotely, "pedir_texto", lambda *a, **k: self.RSS)

        fecha = weworkremotely.obtener()[0].fecha_publicacion
        assert (fecha.year, fecha.month, fecha.day) == (2026, 8, 18)

    def test_un_titulo_sin_dos_puntos_queda_entero(self, monkeypatch):
        rss = self.RSS.replace("Zeta Global: Senior Django Developer", "Django Developer")
        monkeypatch.setattr(weworkremotely, "pedir_texto", lambda *a, **k: rss)

        oferta = weworkremotely.obtener()[0]
        assert oferta.empresa == ""
        assert oferta.titulo == "Django Developer"


class TestLimpiezaDeHtml:
    def test_convierte_el_html_de_la_api_en_texto_legible(self):
        assert limpiar_html("<p>Hola</p><p>Mundo</p>") == "Hola\nMundo"

    def test_traduce_las_entidades(self):
        assert limpiar_html("<p>Django &amp; React</p>") == "Django & React"

    def test_recorta_las_descripciones_largas(self):
        largo = limpiar_html("<p>" + "palabra " * 500 + "</p>", largo_maximo=100)
        assert len(largo) <= 104
        assert largo.endswith("...")

    def test_texto_vacio_no_rompe(self):
        assert limpiar_html("") == ""
