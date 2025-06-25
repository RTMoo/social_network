from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
from PIL.Image import Image as PILImage
from typing import Tuple


def crop_center_square(img: PILImage) -> PILImage:
    """
    Обрезает изображение по центру до квадрата.

    Args:
        img (PILImage): Исходное изображение.

    Returns:
        PILImage: Обрезанное квадратное изображение.
    """
    w, h = img.size
    if w > h:
        left = (w - h) // 2
        box = (left, 0, left + h, h)
    else:
        top = (h - w) // 2
        box = (0, top, w, top + w)
    return img.crop(box)


def make_circle_avatar(
    input_path: str, size: Tuple[int, int] = (400, 400)
) -> ContentFile:
    """
    Создаёт круглую аватарку из изображения по указанному пути.

    Args:
        input_path (str): Путь к исходному изображению.
        size (Tuple[int, int], optional): Размер выходного изображения. По умолчанию (400, 400).

    Returns:
        ContentFile: Круглая аватарка в формате PNG.
    """
    img = Image.open(input_path).convert("RGBA")
    img = crop_center_square(img)
    img = img.resize(size, Image.LANCZOS)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    result = Image.new("RGBA", size)
    result.paste(img, (0, 0), mask)
    byte_io = BytesIO()
    result.save(byte_io, format="PNG")
    return ContentFile(byte_io.getvalue())
