"""
API for storage.

Implements several api endpints for file download and upload.
"""
from aiohttp.web import RouteTableDef, Request, Response

route = RouteTableDef()


@route.post("/download/")
async def download(request: Request) -> Response:
    """Handle download file request."""
    _ = request
    return Response()


@route.post("/upload/")
async def upload(request: Request) -> Response:
    """Handle upload file request."""
    _ = request
    return Response()
