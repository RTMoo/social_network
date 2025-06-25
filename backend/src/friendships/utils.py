from django.db.models import Model
from typing import List


def sort_models(data: List[Model]) -> List[Model]:
    """
    Сортирует список моделей по их первичному ключу.

    Args:
        data (List[Model]): Список моделей для сортировки.

    Returns:
        List[Model]: Отсортированный список моделей.
    """

    return sorted(data, key=lambda x: x.pk)
