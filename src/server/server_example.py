"""HTTP server."""
from aiohttp import web


async def process_file(request: web.Request) -> web.Response:
    """
    Multipart file request handler.

    :param request: aiohttp.web.Request object.
    :return: aiohttp.web.Response object.
    """
    reader = await request.multipart()
    print(reader.headers)
    return web.Response(status=200)


def main() -> None:
    """
    Start web server.

    Handles post request with binary data/
    """
    app = web.Application()
    app.add_routes(
        [
            web.post("/file/", process_file)
        ]
    )
    web.run_app(app=app)


if __name__ == "__main__":
    main()
