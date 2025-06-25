from typing import Any
from uuid import uuid4
from rest_framework.exceptions import PermissionDenied
from posts.models import Post
from accounts.models import CustomUser
from posts.selectors import get_post
from posts.utils import normalize_post_image, make_post_preview
from posts.utils import decrement_posts_count, increment_posts_count
from django.db import transaction


def create_post(data: dict[str, Any], sender: CustomUser) -> Post:
    """
    Создает новый пост с изображением и увеличивает количество постов у автора.

    Args:
        data (dict[str, Any]): Словарь с данными поста.
        sender (CustomUser): Пользователь, который создает пост.

    Returns:
        Post: Созданный пост.
    """
    image = data.pop("image")

    # Нормализация изображения
    normalized_image = normalize_post_image(image)
    preview_image = make_post_preview(normalized_image)

    post = Post.objects.create(author=sender, **data)

    # Создание уникальных имен для изображений
    image_name = f"{uuid4()}.jpeg"
    preview_name = f"thumb_{image_name}"

    with transaction.atomic():
        # Сохранение изображений в базу данных
        post.image.save(image_name, normalized_image, save=True)
        post.preview.save(preview_name, preview_image, save=True)

        increment_posts_count(user=sender)

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


def delete_post(post_id: int, sender: CustomUser) -> None:
    """
    Удаляет существующий пост и уменьшает количество постов у автора.

    Args:
        post_id (int): id поста, который нужно удалить.
        author (CustomUser): Автор поста.

    Raises:
        PermissionDenied: Если пост не принадлежит автору.
    """
    post = get_post(post_id)

    if post.author != sender:
        raise PermissionDenied()

    with transaction.atomic():
        post.delete()
        decrement_posts_count(user=sender)
