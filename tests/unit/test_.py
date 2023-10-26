from aiohttp import web


async def test_(server: web.Server) -> None:
    assert server
