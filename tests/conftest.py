import pytest_asyncio
from aiohttp.test_utils import TestServer, TestClient
from aiohttp import web, ClientSession

from src.server.app import get_app


@pytest_asyncio.fixture(scope="function")
async def server(aiohttp_server: TestServer) -> web.Server:
    app = await get_app()
    return await aiohttp_server(app)


@pytest_asyncio.fixture(scope="function")
async def client(aiohttp_client: TestClient) -> ClientSession:
    app = await get_app()
    return await aiohttp_client(app)
