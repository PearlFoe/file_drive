from aiohttp import ClientSession, MultipartReader


from src.server.storage.file_handlers import FileHandler


async def test_validation_success(client: ClientSession) -> None:
    response = await client.post(
        "/api/v1/storage/download/",
        json={"file_name": "Lenna.png"}
    )
    assert response.status == 200


async def test_validation_error(client: ClientSession) -> None:
    response = await client.post(
        "/api/v1/storage/download/",
        json={}
    )
    assert response.status == 400


async def test_binary_multupart_response(
        client: ClientSession, file_handler_mock: FileHandler) -> None:
    response = await client.post(
        "/api/v1/storage/download/",
        json={"file_name": "Lenna.png"}
    )

    reader = MultipartReader.from_response(response)
    sub_reader =await reader.next()

    assert await sub_reader.read() == await file_handler_mock._read("test_path")
