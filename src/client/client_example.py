"""HTTP client."""
import aiofiles
import asyncio
import aiohttp


async def main() -> None:
    """Send request and writes image from response."""
    url = "http://0.0.0.0:8080/api/v1/storage/download/"
    data = {
        "file_name": "Lenna.png"
    }
    async with aiohttp.ClientSession() as s, s.post(url, json=data) as r:
        print(r.headers)
        print(r.status)

        reader = aiohttp.MultipartReader.from_response(r)
        sub_reader = await reader.next()

        async with aiofiles.open("storage/1.png", "wb") as f:
            await f.write(
                await sub_reader.read() # type: ignore
            )


if __name__ == "__main__":
    asyncio.run(main())
