from aiohttp import ClientSession


async def test_download(client: ClientSession) -> None:
    response = await client.post("/api/v1/storage/download/")
    assert response.status == 200
