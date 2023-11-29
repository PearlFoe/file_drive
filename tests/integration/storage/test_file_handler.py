from os import path


from src.server.storage.file_handlers import FileHandler


class TestFileHandler:
    __test_data_folder = "tests/data/"
    __test_file_name = "Lenna.png"
    __test_file_path = path.join(__test_data_folder, __test_file_name)

    def _get_multipart_reader(self) -> None:
        ...

    async def test_file_write(self, file_handler: FileHandler) -> None:
        ...
