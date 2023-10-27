from aiohttp.web import Application

from .storage import get_app as storage_app


def get_app() -> Application:
    """Create app funcion."""
    app = Application()
    app.add_subapp(prefix="/storage", subapp=storage_app())
    return app
