"""Enty poing of backend of the app."""
from aiohttp import web

_ROUTERS = []

async def get_app() -> web.Application:
    """Create server application."""
    app = web.Application()

    app.add_routes(_ROUTERS)

    return app
