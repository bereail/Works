"""El filtro de relevancia es lo que decide qué oferta le llega a Berenice y cuál se
descarta sin que ella la vea nunca. Si se rompe, la bandeja se llena de ruido o —peor—
se pierden ofertas buenas en silencio."""

from app.services import relevancia
from app.services.fuentes.base import OfertaExterna


def oferta(titulo, descripcion="", etiquetas=None, ubicacion="", empresa=""):
    return OfertaExterna(
        id_externo="1",
        titulo=titulo,
        empresa=empresa,
        descripcion=descripcion,
        ubicacion=ubicacion,
        etiquetas=etiquetas or [],
    )


class TestCoincidenciaPorPalabra:
    """El caso que motivó `contiene`: buscar subcadenas sueltas confundía tecnologías."""

    def test_java_no_matchea_dentro_de_javascript(self):
        assert relevancia.contiene("java", "backend java y node") is True
        assert relevancia.contiene("java", "full-stack javascript react") is False

    def test_matchea_al_final_del_titulo(self):
        assert relevancia.contiene("lead", "technical lead") is True

    def test_matchea_terminos_con_simbolos(self):
        assert relevancia.contiene(".net", "full-stack .net y react") is True
        assert relevancia.contiene("c#", "desarrollador c# senior") is True

    def test_no_matchea_dentro_de_otra_palabra(self):
        assert relevancia.contiene("ios", "somos curiosos") is False


class TestPuntaje:
    def test_django_en_el_titulo_es_lo_mas_relevante(self):
        con_django = relevancia.calcular_puntaje(oferta("Desarrollador Django"))
        generica = relevancia.calcular_puntaje(oferta("Desarrollador de software"))
        assert con_django > generica
        assert con_django >= relevancia.PUNTAJE_MINIMO

    def test_el_stack_pesa_mas_en_el_titulo_que_en_la_descripcion(self):
        en_titulo = relevancia.calcular_puntaje(oferta("Desarrollador Django"))
        en_descripcion = relevancia.calcular_puntaje(
            oferta("Desarrollador de software", descripcion="ideal si sabés django")
        )
        assert en_titulo > en_descripcion

    def test_part_time_suma_porque_su_capacidad_es_de_5_a_10_horas(self):
        completo = relevancia.calcular_puntaje(oferta("Django Developer full time"))
        parcial = relevancia.calcular_puntaje(oferta("Django Developer part-time"))
        assert parcial > completo

    def test_latam_suma_frente_al_mercado_en_ingles(self):
        argentina = relevancia.calcular_puntaje(oferta("Django Developer", ubicacion="Argentina"))
        sin_ubicacion = relevancia.calcular_puntaje(oferta("Django Developer"))
        assert argentina > sin_ubicacion

    def test_seniority_alta_resta(self):
        semi = relevancia.calcular_puntaje(oferta("Django Developer"))
        jefatura = relevancia.calcular_puntaje(oferta("Head of Engineering Django"))
        assert jefatura < semi

    def test_stack_ajeno_en_el_titulo_resta(self):
        propio = relevancia.calcular_puntaje(oferta("Full-Stack Developer React Node"))
        ajeno = relevancia.calcular_puntaje(oferta("Full-Stack Developer Java Angular"))
        assert ajeno < propio

    def test_rol_ajeno_se_detecta_por_las_etiquetas_aunque_el_titulo_sea_neutro(self):
        """El caso real de Remote OK: un aviso titulado 'Social Comms' que entraba
        a la bandeja porque el título no delataba que era de marketing."""
        puntaje = relevancia.calcular_puntaje(
            oferta("Social Comms", etiquetas=["marketing", "social media", "content writing"])
        )
        assert puntaje < relevancia.PUNTAJE_MINIMO

    def test_frontend_puro_resta_porque_no_aprovecha_el_perfil(self):
        completo = relevancia.calcular_puntaje(oferta("React Developer con Node"))
        solo_front = relevancia.calcular_puntaje(oferta("React Developer"))
        assert solo_front < completo

    def test_las_fuentes_internacionales_pesan_un_poco_menos(self):
        aviso = oferta("Django Developer")
        assert relevancia.calcular_puntaje(aviso, "remoteok") < relevancia.calcular_puntaje(aviso, "getonbrd")

    def test_el_puntaje_nunca_se_va_de_rango(self):
        pesima = relevancia.calcular_puntaje(oferta("Head of Marketing Salesforce SAP"))
        buenisima = relevancia.calcular_puntaje(
            oferta(
                "Desarrollador Full-Stack Django React part-time",
                descripcion="python postgresql testing pytest dashboard freelance",
                ubicacion="Argentina",
                etiquetas=["django", "react", "node"],
            )
        )
        assert 0 <= pesima <= 100
        assert 0 <= buenisima <= 100


class TestMotivos:
    def test_explica_por_que_llego_la_oferta(self):
        encontrados = relevancia.motivos(
            oferta("Desarrollador Django part-time", ubicacion="Argentina")
        )
        assert "django" in encontrados
        assert "part-time" in encontrados
        assert "argentina" in encontrados
