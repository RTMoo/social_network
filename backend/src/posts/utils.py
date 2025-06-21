from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


def normalize_post_image(input_path, size=(1080, 720), quality=85):
    """Сжимает и нормализует оригинальное изображение поста"""
    img = Image.open(input_path).convert("RGB")
    img.thumbnail(size, Image.LANCZOS)

    byte_io = BytesIO()
    img.save(byte_io, format="JPEG", quality=quality)
    return ContentFile(byte_io.getvalue())


def make_post_preview(input_path, size=(400, 400), quality=95):
    """Создаёт уменьшенную версию (preview) для поста"""
    img = Image.open(input_path).convert("RGB")
    img.thumbnail(size, Image.LANCZOS)

    byte_io = BytesIO()
    img.save(byte_io, format="JPEG", quality=quality)
    return ContentFile(byte_io.getvalue())
