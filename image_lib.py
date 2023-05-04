import io

import aiohttp
from PIL import Image
from fastapi import HTTPException


async def download_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Image not found")
            return await response.read()


async def rotate_image(image_bytes: io.BytesIO) -> io.BytesIO:
    image = Image.open(image_bytes)
    rotated_image = image.rotate(-90, expand=True)
    rotated_image_bytes = io.BytesIO()
    rotated_image.save(rotated_image_bytes, format="PNG")
    rotated_image_bytes.seek(0)
    return rotated_image_bytes
