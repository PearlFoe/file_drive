"""Enty poing of the server."""
from aiohttp import web

from src.server import get_app as root_v1
from src.server.containers import Container
from src.settings import Settigns


def _get_container() -> Container:
    """
    Create server container for dependency managing.

    :return Container: Declarative container.
    """
    env = Settigns()

    container = Container()
    container.env.from_dict(env.model_dump())

    return container


async def get_app() -> web.Application:
    """Create server application."""
    app = web.Application()

    app.add_subapp(prefix="/api/v1/", subapp=root_v1())
    app.container = _get_container()

    return app
