from aiohttp import ClientSession, MultipartWriter


async def test_upload(client: ClientSession, mp_writer_mock: MultipartWriter) -> None:
    response = await client.post("/api/v1/storage/upload/", data=mp_writer_mock)
    assert response.status == 201
