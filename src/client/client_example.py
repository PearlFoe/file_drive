"""HTTP client."""
import argparse
import asyncio

import aiofiles
import aiohttp



async def _write_img(reader: aiohttp.MultipartReader) -> None:
    async with aiofiles.open("storage/Lenna.png", "wb") as f:
        await f.write(
            await reader.read()
        )


async def _read_img() -> bytes:
    async with aiofiles.open("storage/Lenna.png", "rb") as f:
        return await f.read()


async def _download_img() -> None:
    url = "http://0.0.0.0:8080/api/v1/storage/download/"
    data = {
        "file_name": "Lenna.png"
    }
    async with aiohttp.ClientSession() as s, s.post(url, json=data) as r:
        print(r.headers)
        print(r.status)

        reader = aiohttp.MultipartReader.from_response(r)
        sub_reader = await reader.next()
        await _write_img(sub_reader)


async def _upload_img() -> None:
    url = "http://0.0.0.0:8080/api/v1/storage/upload/"

    with aiohttp.MultipartWriter(subtype="image/png") as file_writer:
        headers = {
            "Content-Type": f"multipart/x-mixed; boundary={file_writer.boundary}"
        }
        file_writer.append(await _read_img())

        async with aiohttp.ClientSession() as s, s.post(url, data=file_writer, headers=headers) as r:
            print(r.status)


async def main(command: str) -> None:
    """Send request and writes image from response."""
    match command:
        case "u":
            await _upload_img()
        case "d":
            await _download_img()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c")
    args = parser.parse_args()

    asyncio.run(main(args.c))
