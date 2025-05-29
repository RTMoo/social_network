from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw


def crop_center_square(img):
    w, h = img.size
    if w > h:
        left = (w - h) // 2
        box = (left, 0, left + h, h)
    else:
        top = (h - w) // 2
        box = (0, top, w, top + w)
    return img.crop(box)


def make_circle_avatar(input_path, size=(400, 400)):
    img = Image.open(input_path).convert("RGBA")

    # Приводим к квадрату
    img = crop_center_square(img)

    # Ресайз до нужного размера
    img = img.resize(size, Image.LANCZOS)

    # Круглая маска
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    # Применяем маску
    result = Image.new("RGBA", size)
    result.paste(img, (0, 0), mask)

    # Сохраняем в байты
    byte_io = BytesIO()
    result.save(byte_io, format='PNG')
    return ContentFile(byte_io.getvalue())
