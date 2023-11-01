import asyncio
import pytest
import pytest_asyncio
from aiohttp.test_utils import TestServer, TestClient
from aiohttp import web, ClientSession

from src.server.storage.file_handlers import FileHandler

from src.server import app, containers
from src.settings import Settigns


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> Settigns:
    return Settigns()


@pytest.fixture(scope="session")
def container(settings: Settigns) -> containers.Container:
    container = containers.Container()
    container.env.from_dict(settings.model_dump())
    return container


@pytest_asyncio.fixture(scope="function")
async def application(file_handler_mock: FileHandler) -> web.Application:
    server_app = await app.get_app()
    server_app.container.file_handler.override(file_handler_mock)

    return server_app


@pytest_asyncio.fixture(scope="function")
async def server(aiohttp_server: TestServer, application: web.Application) -> web.Server:
    return await aiohttp_server(application)



@pytest_asyncio.fixture(scope="function")
async def client(aiohttp_client: TestClient, application: web.Application) -> ClientSession:
    return await aiohttp_client(application)


@pytest.fixture(scope="class")
def file_handler_mock(settings: Settigns) -> FileHandler:
    async def _write(*args, **kwargs) -> None:
        return None

    async def _read(*args, **kwargs) -> bytes:
        return b""

    fh = FileHandler(storage_dir=settings.storage_dir)

    fh._read = _read
    fh._write = _write

    return fh


@pytest.fixture(scope="class")
def file_handler(settings: Settigns) -> FileHandler:
    return FileHandler(storage_dir=settings.storage_dir)