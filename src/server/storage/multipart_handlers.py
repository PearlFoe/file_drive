"""Handler for mutipart content."""
from aiohttp import web, MultipartReader, BodyPartReader, MultipartWriter

from .models import FileMetadata


class MutipartHandler:
    """
    Multipart data handler.

    Implements several classmethods handling all
    work with multipart requests and responses.
    """

    @staticmethod
    async def create_response(request: web.Request, file: bytes, metadata: FileMetadata) -> web.StreamResponse:
        """
        Create prepared response object.

        Add file content and its metadata into it.

        :param request: Reques object using to prepare response.
        :param file: File content.
        :param metadata: File metadata.
        :return: Prepared response.
        """
        with MultipartWriter(subtype="image/png") as file_writer:
            headers = {
                "Content-Type": f"multipart/x-mixed; boundary={file_writer.boundary}"
            }
            response = web.StreamResponse(headers=headers)
            await response.prepare(request)

            file_writer.append(
                metadata.model_dump_json(),
                {"Content-Type": "application/json"}
            )
            file_writer.append(
                file,
                {"Content-Type": "image/png"}
            )

            await file_writer.write(response)

        return response

    @staticmethod
    async def parse_reques_data(data: MultipartReader) -> tuple[FileMetadata, BodyPartReader | MultipartReader | None]:
        """
        Multipart request body parser.

        :param data: Request body. Should contain two parts:
            - file metadata
            - file content
        :return: Parsed request body: metadata and file content.
        """
        md_reader = await data.next()
        md_content = await md_reader.read()
        metadata = FileMetadata.model_validate_json(md_content.decode())

        fd_reader = await data.next()
        fd_content = await fd_reader.read()

        return metadata, fd_content
