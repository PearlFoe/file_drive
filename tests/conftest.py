import uuid
import asyncio
import pytest
import pytest_asyncio
from aiohttp.test_utils import TestServer, TestClient, make_mocked_request
from aiohttp.web_request import Request
from aiohttp import web, ClientSession, MultipartWriter, MultipartReader

from src.server.storage.file_handlers import FileHandler
from src.server.storage.models import FileMetadata
from src.server.storage.multipart_handlers import MutipartHandler

from src.server import app, containers
from src.settings import Settigns

from tests.mocks.streams import Stream


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
def request_mock() -> Request:
    return make_mocked_request(
        method="post",
        path="api/test_path/",
    )


@pytest.fixture(scope="class")
def multipart_request_mock(mp_writer_mock: MultipartWriter) -> Request:
    return make_mocked_request(
        method="post",
        path="api/test_path/",
        writer=mp_writer_mock,
        headers={"Content-Type": f"multipart/x-mixed; boundary={mp_writer_mock.boundary}"}
    )


@pytest.fixture(scope="class")
def file_data() -> bytes:
    return b"test byte data"


@pytest.fixture(scope="class")
def file_metadata() -> FileMetadata:
    return FileMetadata(file_name="Lenna.png")


@pytest.fixture(scope="class")
def file_handler_mock(settings: Settigns, file_data: bytes) -> FileHandler:
    async def _write(*args, **kwargs) -> None:
        return None

    async def _read(*args, **kwargs) -> bytes:
        return file_data

    fh = FileHandler(storage_dir=settings.storage_dir)

    fh._read = _read
    fh._write = _write

    return fh


@pytest.fixture(scope="class")
def file_handler(settings: Settigns) -> FileHandler:
    return FileHandler(storage_dir=settings.storage_dir)


@pytest.fixture(scope="class")
def mp_raw_content(file_metadata: FileMetadata, file_data: bytes) -> tuple[str, bytes]:
    encoding = "utf-8"
    boundary = uuid.uuid4().hex
    content =  bytes(
        f"--{boundary}\r\n" +\
        "Content-Type: application/json\r\n\r\n" +\
        file_metadata.model_dump_json() +\
        f"\r\n--{boundary}\r\n" +\
        "Content-Type: image/png\r\n\r\n" +\
        file_data.decode(encoding=encoding) +\
        f"\r\n--{boundary}--",
        encoding=encoding
    )

    return boundary, content


@pytest.fixture(scope="class")
def mp_reader_content(mp_raw_content: tuple[str, bytes]) -> tuple[dict, Stream]:
    boundary, content = mp_raw_content
    headers = {"Content-Type": f"multipart/x-mixed; boundary={boundary}"}
    sr = Stream(content=content)
    return headers, sr

@pytest.fixture(scope="class")
def mp_writer_mock(file_data: bytes) -> MultipartWriter:
    with MultipartWriter(subtype="image/png") as mp_writer:
        mp_writer.append(
            file_data,
            {"Content-Type": "image/png"}  # type: ignore
        )
        return mp_writer


@pytest_asyncio.fixture(scope="class")
async def mp_reader_mock(mp_reader_content: tuple[dict, asyncio.StreamReader]) -> MultipartReader:
    headers, content = mp_reader_content
    return MultipartReader(headers, content)


@pytest.fixture(scope="class")
def multipart_handler() -> MutipartHandler:
    return MutipartHandler()
