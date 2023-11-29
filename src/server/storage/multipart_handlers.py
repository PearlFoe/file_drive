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
                {"Content-Type": "application/json"}  # type: ignore
            )
            file_writer.append(
                file,
                {"Content-Type": "image/png"}  # type: ignore
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
        data_reader = await data.next()
        metadata = await data.next()

        metadata = FileMetadata.model_validate(str(metadata))

        return metadata, data_reader
