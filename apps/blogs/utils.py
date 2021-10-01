import random
from fastapi import HTTPException
import string
from config import settings
from fastapi import HTTPException
import base64
from PIL import Image
import datetime
import base64
import io


async def generate_random_string(
    length: int = 10, charcaters: str = string.ascii_letters, /
) -> str:
    random_string = ""
    for _ in range(length):
        random_string += random.choice(charcaters)
    return random_string

async def convert_base64_toimage_and_save_file(base64_encoded: str,/) -> str:
    try:
        image = base64.b64decode(base64_encoded)
        file_path = f"{datetime.datetime.now().strftime('%d%m%Y%H%M%S%f')}.png"
        imagePath = (settings.MEDIA_ROOT + '/' + file_path)
        img = Image.open(io.BytesIO(image))
        img.save(imagePath, 'png')
        return '/media/' + file_path
    except (ValueError, OSError, UnicodeDecodeError, base64.binascii.Error):
        raise HTTPException(status_code=400,detail="invalid base64 image")

