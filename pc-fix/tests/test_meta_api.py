"""publicar_en_facebook y publicar_en_instagram hablan con la Graph API real de Meta
— estos tests simulan las respuestas HTTP para no salir a internet ni gastar
publicaciones reales. Sirven para detectar si un cambio rompe cómo se arma el pedido
o cómo se interpreta la respuesta (éxito, o error de Meta)."""

from types import SimpleNamespace

import pytest

from app.services import meta_api


def _respuesta(status_code=200, json_data=None):
    return SimpleNamespace(status_code=status_code, json=lambda: json_data or {})


def _cuenta(**extra):
    base = dict(id_externo="123456", access_token="token-de-prueba", url_base_publica="")
    base.update(extra)
    return SimpleNamespace(**base)


class TestPublicarEnFacebook:
    def test_publica_la_foto_con_el_caption_y_devuelve_el_post_id(self, monkeypatch, tmp_path):
        pedidos = []

        def post_falso(url, params=None, data=None, files=None, timeout=None):
            pedidos.append(dict(url=url, params=params, data=data))
            return _respuesta(200, {"post_id": "123456_789"})

        monkeypatch.setattr(meta_api.httpx, "post", post_falso)
        imagen = tmp_path / "flyer.jpg"
        imagen.write_bytes(b"contenido falso de imagen")

        post_id = meta_api.publicar_en_facebook(_cuenta(), "Texto del posteo", str(imagen))

        assert post_id == "123456_789"
        assert pedidos[0]["url"] == f"{meta_api.URL_BASE}/123456/photos"
        assert pedidos[0]["params"] == {"access_token": "token-de-prueba"}
        assert pedidos[0]["data"] == {"caption": "Texto del posteo"}

    def test_usa_el_id_si_no_viene_post_id(self, monkeypatch, tmp_path):
        monkeypatch.setattr(meta_api.httpx, "post", lambda *a, **k: _respuesta(200, {"id": "solo-id"}))
        imagen = tmp_path / "flyer.jpg"
        imagen.write_bytes(b"x")

        assert meta_api.publicar_en_facebook(_cuenta(), "texto", str(imagen)) == "solo-id"

    def test_error_de_meta_levanta_error_publicacion_meta(self, monkeypatch, tmp_path):
        monkeypatch.setattr(
            meta_api.httpx, "post",
            lambda *a, **k: _respuesta(400, {"error": {"message": "Token vencido"}}),
        )
        imagen = tmp_path / "flyer.jpg"
        imagen.write_bytes(b"x")

        with pytest.raises(meta_api.ErrorPublicacionMeta, match="Token vencido"):
            meta_api.publicar_en_facebook(_cuenta(), "texto", str(imagen))

    def test_error_sin_mensaje_usa_el_default(self, monkeypatch, tmp_path):
        monkeypatch.setattr(meta_api.httpx, "post", lambda *a, **k: _respuesta(500, {}))
        imagen = tmp_path / "flyer.jpg"
        imagen.write_bytes(b"x")

        with pytest.raises(meta_api.ErrorPublicacionMeta, match="Error desconocido"):
            meta_api.publicar_en_facebook(_cuenta(), "texto", str(imagen))


class TestPublicarEnInstagram:
    def test_crea_el_contenedor_y_despues_lo_publica(self, monkeypatch):
        pedidos = []

        def post_falso(url, params=None, data=None, timeout=None):
            pedidos.append(dict(url=url, data=data))
            if url.endswith("/media"):
                return _respuesta(200, {"id": "creation-id-1"})
            return _respuesta(200, {"id": "media-publicado-1"})

        monkeypatch.setattr(meta_api.httpx, "post", post_falso)

        media_id = meta_api.publicar_en_instagram(
            _cuenta(), "Texto del posteo", "https://ailonline.com.ar/pcfix/flyer.jpg"
        )

        assert media_id == "media-publicado-1"
        assert len(pedidos) == 2
        assert pedidos[0]["url"] == f"{meta_api.URL_BASE}/123456/media"
        assert pedidos[0]["data"] == {
            "image_url": "https://ailonline.com.ar/pcfix/flyer.jpg",
            "caption": "Texto del posteo",
        }
        assert pedidos[1]["url"] == f"{meta_api.URL_BASE}/123456/media_publish"
        assert pedidos[1]["data"] == {"creation_id": "creation-id-1"}

    def test_error_creando_el_contenedor_no_intenta_publicar(self, monkeypatch):
        llamadas = []

        def post_falso(url, params=None, data=None, timeout=None):
            llamadas.append(url)
            return _respuesta(400, {"error": {"message": "URL de imagen no accesible"}})

        monkeypatch.setattr(meta_api.httpx, "post", post_falso)

        with pytest.raises(meta_api.ErrorPublicacionMeta, match="URL de imagen no accesible"):
            meta_api.publicar_en_instagram(_cuenta(), "texto", "https://ejemplo.com/x.jpg")

        assert len(llamadas) == 1  # nunca llegó a pedir media_publish

    def test_error_publicando_el_contenedor_ya_creado(self, monkeypatch):
        def post_falso(url, params=None, data=None, timeout=None):
            if url.endswith("/media"):
                return _respuesta(200, {"id": "creation-id-1"})
            return _respuesta(400, {"error": {"message": "El contenedor expiró"}})

        monkeypatch.setattr(meta_api.httpx, "post", post_falso)

        with pytest.raises(meta_api.ErrorPublicacionMeta, match="El contenedor expiró"):
            meta_api.publicar_en_instagram(_cuenta(), "texto", "https://ejemplo.com/x.jpg")
