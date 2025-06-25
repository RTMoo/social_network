from typing import Any
from uuid import uuid4
from rest_framework.exceptions import PermissionDenied
from posts.models import Post
from accounts.models import CustomUser
from posts.selectors import get_post
from posts.utils import normalize_post_image, make_post_preview


def create_post(data: dict[str, Any], author: CustomUser) -> Post:
    """
    Создает новый пост с изображением.

    Args:
        data (dict[str, Any]): Словарь с данными поста.
        author (CustomUser): Автор поста.

    Returns:
        Post: Созданный пост.
    """
    image = data.pop("image")

    # Нормализация изображения
    normalized_image = normalize_post_image(image)
    preview_image = make_post_preview(normalized_image)

    post = Post.objects.create(author=author, **data)

    # Создание уникальных имен для изображений
    image_name = f"{uuid4()}.jpeg"
    preview_name = f"thumb_{image_name}"

    # Сохранение изображений в базу данных
    post.image.save(image_name, normalized_image, save=True)
    post.preview.save(preview_name, preview_image, save=True)

    return post


def update_post(data: dict[str, Any], post_id: int) -> Post:
    """
    Обновляет существующий пост.

    Args:
        data (dict[str, Any]): Словарь с данными для обновления.
        post_id (int): id поста, который нужно обновить.

    Returns:
        Post: Обновленный пост.
    """
    post = get_post(post_id)

    for key, value in data.items():
        setattr(post, key, value)

    post.save()

    return post


def delete_post(post_id: int, author: CustomUser) -> None:
    """
    Удаляет существующий пост.

    Args:
        post_id (int): id поста, который нужно удалить.
        author (CustomUser): Автор поста.

    Raises:
        PermissionDenied: Если пост не принадлежит автору.
    """
    post = get_post(post_id)

    if post.author != author:
        raise PermissionDenied()

    post.delete()
