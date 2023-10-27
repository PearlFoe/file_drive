from aiohttp import ClientSession


async def test_upload(client: ClientSession) -> None:
    response = await client.post("/api/v1/storage/upload/")
    assert response.status == 200
