from django.db.models import Model


def sort_models(data: list[Model]) -> list[Model]:
    """
    Приводит список моделей к порядку сортировки
    """

    return sorted(data, key=lambda x: x.pk)
