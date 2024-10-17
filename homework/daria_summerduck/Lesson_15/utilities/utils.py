import re
from functools import wraps


# Dataclasses for storing random data


# Utility function: a decorator to handle exceptions
def handle_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            raise ValueError(f"Error in {func.__name__}: {error}")

    return wrapper


def validate_input(input_string: str) -> bool:
    # Add custom validation rules, e.g., name should be alphabetic and non-empty
    return bool(re.match(r"^[A-Za-z\s]+$", input_string))


def validate_id(id):
    # Optional validation or sanitization for numeric ID
    if not isinstance(id, int) or id <= 0:
        raise ValueError("Invalid ID")


def sanitize_string(input_string: str) -> str:
    # Remove any SQL special characters or dangerous patterns
    sanitized_string = re.sub(r"[^\w\s]", "", input_string)
    return sanitized_string.strip()
