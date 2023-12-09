import pytest
from aiohttp.web_request import Request
from aiohttp import MultipartReader
from pydantic import ValidationError

from src.server.storage.multipart_handlers import MutipartHandler
from src.server.storage.models import FileMetadata

from tests.mocks.streams import Stream


class TestMultipartHandler:
    async def test_create_response(
            self,
            multipart_handler: MutipartHandler,
            request_mock: Request,
            file_data: bytes,
            file_metadata: FileMetadata,
        ):
        response = await multipart_handler.create_response(request_mock, file_data, file_metadata)
        assert response.reason == "OK"
        assert "multipart/x-mixed" in response.content_type

    async def test_parse_request(
            self,
            multipart_handler: MutipartHandler,
            mp_reader_mock: MultipartReader,
            file_data: bytes,
            file_metadata: FileMetadata
        ):
        md, fd = await multipart_handler.parse_reques_data(mp_reader_mock)
        assert md == file_metadata
        assert fd == file_data

    async def test_parse_request__invalid_metadata(
            self,
            multipart_handler: MutipartHandler,
            mp_reader_mock: MultipartReader,
            mp_raw_content: tuple[str, bytes]
        ):
        _, content = mp_raw_content
        mp_reader_mock._content = Stream(content.replace(b"{", b"}}"))  # invalid json

        with pytest.raises(ValidationError):
            await multipart_handler.parse_reques_data(mp_reader_mock)
