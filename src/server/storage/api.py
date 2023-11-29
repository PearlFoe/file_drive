"""
API for storage application.

Implements several api endpints for file download and upload.
"""
from dependency_injector.wiring import Provide, inject
from aiohttp.web import RouteTableDef, Request, Response
from aiohttp import web
from pydantic import ValidationError

from .models import DownloadRequest, FileMetadata
from .file_handlers import FileHandler
from .multipart_handlers import MutipartHandler


route = RouteTableDef()


@route.post("/download/")
@inject
async def download(
        request: Request,
        file_handler: FileHandler = Provide["file_handler"],
        multipart_handler: MutipartHandler = Provide["multipart_handler"],
    ) -> web.StreamResponse:
    """Handle download file request."""
    try:
        data = DownloadRequest(**await request.json())
    except ValidationError as e:
        return Response(
            status=400,
            body=e.json()
        )

    file = await file_handler.download(data.file_name)
    metadata = FileMetadata(file_name=data.file_name)

    response = await multipart_handler.create_response(
        request=request,
        file=file,
        metadata=metadata,
    )

    return response



@route.post("/upload/")
@inject
async def upload(
        request: Request,
        file_handler: FileHandler = Provide["file_handler"],
    ) -> Response:
    """Handle upload file request."""
    reader = await request.multipart()
    await file_handler.upload(reader=reader)
    return Response(status=201)
