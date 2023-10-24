"""HTTP client."""
import asyncio
import aiohttp


async def main() -> None:
    """Send simple binary data."""
    url = "http://0.0.0.0:8080/file/"
    file_path = "tests/data/Lenna.png"
    async with aiohttp.ClientSession() as s:
        data = aiohttp.FormData()
        with open(file_path, "rb") as f:
            data.add_field(
                name="file",
                value=f
            )
            async with s.post(url, data=data) as r:
                print(r.status)


if __name__ == "__main__":
    asyncio.run(main())
