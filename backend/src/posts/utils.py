from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from typing import Tuple


def normalize_post_image(
    input_path: str, size: Tuple[int, int] = (1080, 720), quality: int = 85
) -> ContentFile:
    """
    Сжимает и нормализует оригинальное изображение поста.

    Args:
        input_path (str): Путь к исходному изображению.
        size (Tuple[int, int], optional): Размер выходного изображения. По умолчанию (1080, 720).
        quality (int, optional): Качество JPEG. По умолчанию 85.

    Returns:
        ContentFile: Сжатое изображение в формате JPEG.
    """
    img = Image.open(input_path).convert("RGB")
    img.thumbnail(size, Image.LANCZOS)

    byte_io = BytesIO()
    img.save(byte_io, format="JPEG", quality=quality)
    return ContentFile(byte_io.getvalue())


def make_post_preview(
    input_path: str, size: Tuple[int, int] = (400, 400), quality: int = 95
) -> ContentFile:
    """
    Создаёт уменьшенную версию (preview) для поста.

    Args:
        input_path (str): Путь к исходному изображению.
        size (Tuple[int, int], optional): Размер превью. По умолчанию (400, 400).
        quality (int, optional): Качество JPEG. По умолчанию 95.

    Returns:
        ContentFile: Превью изображения в формате JPEG.
    """
    img = Image.open(input_path).convert("RGB")
    img.thumbnail(size, Image.LANCZOS)

    byte_io = BytesIO()
    img.save(byte_io, format="JPEG", quality=quality)
    return ContentFile(byte_io.getvalue())
