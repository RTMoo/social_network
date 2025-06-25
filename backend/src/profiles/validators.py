from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as SerializerValidationError


def validate_min_length_if_not_empty(
    field_name: str, value: str, is_model_exception: bool = False
) -> None:
    """
    Проверяет минимальную длину значения, если оно не пустое.

    Args:
        field_name (str): Название поля.
        value (str): Проверяемое значение.
        is_model_exception (bool, optional): Если True, выбрасывает исключение модели. По умолчанию False.

    Raises:
        DjangoValidationError: Если значение слишком короткое и is_model_exception=True.
        SerializerValidationError: Если значение слишком короткое и is_model_exception=False.
    """
    min_length = 2
    error_message = "Длина значения должна быть либо пустой, либо не менее 2 символов"

    if value and len(value) < min_length:
        if is_model_exception:
            raise DjangoValidationError({field_name: error_message})

        raise SerializerValidationError({field_name: error_message})
