"""
API for storage application.

Implements several api endpints for file download and upload.
"""
from dependency_injector.wiring import Provide, inject
from aiohttp.web import RouteTableDef, Request, Response
from aiohttp import web, MultipartWriter

from .models import DownloadData
from .file_handlers import FileHandler


route = RouteTableDef()


@route.post("/download/")
@inject
async def download(
        request: Request,
        file_handler: FileHandler = Provide["file_handler"],
    ) -> Response:
    """Handle download file request."""
    data = DownloadData(**await request.json())
    file = await file_handler.download(data.file_name)

    with MultipartWriter(subtype="image/png") as writer:
        writer.append(file, {"Content-Type": "image/png"}) # type: ignore

        headers = {
            "Content-Type": "multipart/x-mixed; "
                            f"boundary={writer.boundary}"
        }
        response = web.StreamResponse(headers=headers)
        await response.prepare(request)
        await writer.write(response)

        return response # type: ignore



@route.post("/upload/")
async def upload(request: Request) -> Response:
    """Handle upload file request."""
    _ = request
    return Response()
