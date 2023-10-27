"""Enty poing of the server."""
from aiohttp import web

from . import get_app as root_v1


async def get_app() -> web.Application:
    """Create server application."""
    app = web.Application()

    app.add_subapp(prefix="/api/v1/", subapp=root_v1())

    return app
