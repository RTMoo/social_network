from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as SerializerValidationError


def validate_min_length_if_not_empty(
    field_name: str, value: str, is_model_exception: bool = False
):
    min_length = 2
    error_message = "Длина значения должна быть либо пустой, либо не менее 2 символов"

    if value and len(value) < min_length:
        if is_model_exception:
            raise DjangoValidationError({field_name: error_message})

        raise SerializerValidationError({field_name: error_message})
