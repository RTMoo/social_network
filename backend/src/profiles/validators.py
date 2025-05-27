from typing import Tuple


def validate_min_length_if_not_empty(value: str) -> Tuple[bool, str]:
    min_length = 2
    error_message = "Длина значения должна быть либо пустой, либо не менее 2 символов"

    if value and len(value) < min_length:
        return False, error_message
    return True, ""
