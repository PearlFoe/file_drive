import asyncio
import pytest
import pytest_asyncio
from aiohttp.test_utils import TestServer, TestClient
from aiohttp import web, ClientSession, MultipartWriter

from src.server.storage.file_handlers import FileHandler
from src.server.storage.models import FileMetadata

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


@pytest.fixture(scope="function")
def container(settings: Settigns, file_handler_mock: FileHandler) -> containers.Container:
    container = containers.Container()
    container.env.from_dict(settings.model_dump())

    container.file_handler.override(file_handler_mock)

    return container


@pytest_asyncio.fixture(scope="function")
async def application(container: containers.Container) -> web.Application:
    server_app = await app.get_app()
    server_app.container = container
    return server_app


@pytest_asyncio.fixture(scope="function")
async def server(aiohttp_server: TestServer, application: web.Application) -> web.Server:
    return await aiohttp_server(application)



@pytest_asyncio.fixture(scope="function")
async def client(aiohttp_client: TestClient, application: web.Application) -> ClientSession:
    return await aiohttp_client(application)


@pytest.fixture(scope="class")
def bytes_data() -> bytes:
    return b"test byte data"


@pytest.fixture(scope="class")
def file_handler_mock(settings: Settigns, bytes_data: bytes) -> FileHandler:
    async def _write(*args, **kwargs) -> None:
        return None

    async def _read(*args, **kwargs) -> bytes:
        return bytes_data

    fh = FileHandler(storage_dir=settings.storage_dir)

    fh._read = _read
    fh._write = _write

    return fh


@pytest.fixture(scope="class")
def file_handler(settings: Settigns) -> FileHandler:
    return FileHandler(storage_dir=settings.storage_dir)


@pytest.fixture(scope="class")
def file_metadata() -> FileMetadata:
    return FileMetadata(file_name="Lenna.png")


@pytest.fixture(scope="class")
def mp_writer_mock(bytes_data: bytes) -> MultipartWriter:
    with MultipartWriter(subtype="image/png") as mp_writer:
        mp_writer.append(
            bytes_data,
            {"Content-Type": "image/png"}  # type: ignore
        )
        return mp_writer
