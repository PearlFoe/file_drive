import pytest_asyncio
from aiohttp.test_utils import TestServer
from aiohttp import web

from src.server.app import get_app


@pytest_asyncio.fixture
async def server(aiohttp_server: TestServer) -> web.Server:
    app = await get_app()
    return await aiohttp_server(app)
