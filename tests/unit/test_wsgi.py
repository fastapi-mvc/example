import pytest
from example import ApplicationLoader


class TestApplicationLoader:

    def test_should_create_wsgi_and_populate_defaults(self, asgi_app):
        # given / when
        wsgi = ApplicationLoader(asgi_app)

        # then
        assert wsgi.load() == asgi_app
        assert wsgi.cfg.worker_class_str == "uvicorn.workers.UvicornWorker"
        assert wsgi.cfg.address == [("127.0.0.1", 8000)]
        assert wsgi.cfg.env == {}
        assert wsgi.cfg.settings["bind"].value == ["127.0.0.1:8000"]
        assert wsgi.cfg.settings["raw_env"].value == []
        assert wsgi.cfg.settings["workers"].value == 2
        assert not wsgi.cfg.settings["daemon"].value
        assert not wsgi.cfg.settings["pidfile"].value

    def test_should_create_wsgi_and_override_config(self, asgi_app):
        # given / when
        wsgi = ApplicationLoader(
            application=asgi_app,
            overrides={
                "raw_env": ("FOOBAR=123",),
                "bind": "0.0.0.0:3000",
                "workers": 3,
                "daemon": True,
                "pidfile": "/tmp/api.pid"
            }
        )

        # then
        assert wsgi.cfg.address == [("0.0.0.0", 3000)]
        assert wsgi.cfg.env == {"FOOBAR": "123"}
        assert wsgi.cfg.settings["bind"].value == ["0.0.0.0:3000"]
        assert wsgi.cfg.settings["raw_env"].value == ["FOOBAR=123"]
        assert wsgi.cfg.settings["workers"].value == 3
        assert wsgi.cfg.settings["daemon"].value
        assert wsgi.cfg.settings["pidfile"].value == "/tmp/api.pid"

    def test_should_raise_when_invalid_override_given(self, asgi_app):
        # given
        overrides = {
            "unknown": True,
            "workers": None,
        }

        # when / then
        with pytest.raises(SystemExit):
            ApplicationLoader(application=asgi_app, overrides=overrides)
