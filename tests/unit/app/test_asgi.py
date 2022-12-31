from example.config import settings
from example.app.router import root_api_router
from example.app.asgi import (
    get_application,
    on_startup,
    on_shutdown,
)
from example.app.exceptions import (
    HTTPException,
    http_exception_handler,
)


class TestGetApplication:

    def test_should_create_app_and_populate_defaults(self):
        # given / when
        app = get_application()

        # then
        assert app.title == settings.PROJECT_NAME
        assert app.debug == settings.DEBUG
        assert app.version == settings.VERSION
        assert app.docs_url == settings.DOCS_URL
        assert app.router.on_startup == [on_startup]
        assert app.router.on_shutdown == [on_shutdown]
        assert all(r in app.routes for r in root_api_router.routes)
        assert app.exception_handlers[HTTPException] == http_exception_handler
