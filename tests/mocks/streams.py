import io
from typing import Any, Optional

class Stream:
    content: Any

    def __init__(self, content: Any) -> None:
        self.content = io.BytesIO(content)

    async def read(self, size: Optional[Any] = None):
        return self.content.read(size)

    def at_eof(self):
        return self.content.tell() == len(self.content.getbuffer())

    async def readline(self):
        return self.content.readline()

    def unread_data(self, data: Any) -> None:
        self.content = io.BytesIO(data + self.content.read())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.content.close()
