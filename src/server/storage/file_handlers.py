"""File handler module."""
import os

import aiofiles
from aiohttp import MultipartReader


class FileHandler:
    """Handles async read/write file logic."""

    def __init__(
        self,
        storage_dir: str,
    ) -> None:
        self.storage_path = storage_dir

    async def _write(self, file_path: str, reader: MultipartReader) -> None:
        part = await reader.next()
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(
                await part.read() # type: ignore
            )

    async def _read(self, file_path: str) -> bytes:
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()

    async def upload(self, reader: MultipartReader) -> None:
        """
        Save data form reader into storage.

        :param reader (MultipartReader): Multipart reader from request.
        """
        file_name = reader.headers.get("filename", "Lenna.png")
        file_path = os.path.join(self.storage_path, file_name)
        await self._write(file_path=file_path, reader=reader)

    async def download(self, file_name: str) -> bytes:
        """
        Get file content from storage.

        :param file_name (str): Name of the file in the storage.
        :return bytes: File content.
        """
        file_path = os.path.join(self.storage_path, file_name)
        return await self._read(file_path=file_path)
