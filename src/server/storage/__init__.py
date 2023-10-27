from aiohttp.web import Application

from .api import route


def get_app() -> Application:
    """Create app funcion."""
    app = Application()
    app.add_routes(routes=route)
    return app
