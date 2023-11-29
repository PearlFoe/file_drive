from aiohttp import ClientSession, MultipartReader


from src.server.storage.file_handlers import FileHandler
from src.server.storage.models import FileMetadata


async def test_validation_success(client: ClientSession, file_metadata: FileMetadata) -> None:
    response = await client.post(
        "/api/v1/storage/download/",
        json=file_metadata.model_dump()
    )
    assert response.status == 200


async def test_validation_error(client: ClientSession) -> None:
    response = await client.post(
        "/api/v1/storage/download/",
        json={}
    )
    assert response.status == 400


async def test_binary_multupart_response(
        client: ClientSession,
        file_handler_mock: FileHandler,
        file_metadata: FileMetadata
    ) -> None:
    response = await client.post(
        "/api/v1/storage/download/",
        json=file_metadata.model_dump()
    )
    wrapper = MultipartReader.from_response(response)

    metadata_reader = await wrapper.next()
    metadata = await metadata_reader.read()
    file_reader = await wrapper.next()
    file = await file_reader.read()

    assert response.status == 200
    assert file == await file_handler_mock._read("test_path")
    assert FileMetadata.model_validate_json(metadata.decode()) == file_metadata
