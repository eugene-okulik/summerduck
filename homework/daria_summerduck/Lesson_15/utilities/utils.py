import re
from functools import wraps
from collections import defaultdict

# Precompile regular expressions
input_pattern = re.compile(r"^[A-Za-z\s]+$")
sanitize_pattern = re.compile(r"[^\w\s]")


def handle_db_exceptions(func):
    """Decorator to handle exceptions in database operations"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            raise ValueError(f"Error in {func.__name__}: {error}")

    return wrapper


def validate_input(input_string: str) -> bool:
    """Custom validation rules, e.g., name should be alphabetic and non-empty"""
    return bool(input_pattern.match(input_string))


def validate_id(id: int) -> None:
    """Optional validation or sanitization for numeric ID"""
    if not isinstance(id, int):
        raise ValueError("ID must be an integer")
    if id <= 0:
        raise ValueError("ID must be a positive integer")


def sanitize_string(input_string: str) -> str:
    """Remove any SQL special characters or dangerous patterns"""
    sanitized_string = sanitize_pattern.sub("", input_string)
    return sanitized_string.strip()


def validate_and_sanitize_params(func):
    """Decorator to validate and sanitize string arguments and validate ID"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        sanitized_args = []
        sanitized_kwargs = {}

        for arg in args:
            if isinstance(arg, str):
                if not validate_input(arg) and not re.match(r"\d{2}-\d{4}", arg):
                    raise ValueError(f"Invalid input: {arg}")
                sanitized_args.append(sanitize_string(arg))
            elif isinstance(arg, int):
                validate_id(arg)
                sanitized_args.append(arg)
            else:
                sanitized_args.append(arg)

        for key, value in kwargs.items():
            if isinstance(value, str):
                if not validate_input(value) and not re.match(r"\d{2}-\d{4}", value):
                    raise ValueError(f"Invalid input: {value}")
                sanitized_kwargs[key] = sanitize_string(value)
            elif isinstance(value, int):
                validate_id(value)
                sanitized_kwargs[key] = value
            elif value.__class__.__name__ == "DateRange":
                sanitized_kwargs[key] = value

        return func(*sanitized_args, **sanitized_kwargs)

    return wrapper


def organize_student_details(details):
    organized_data = {
        "name": details[0]["name"],
        "second_name": details[0]["second_name"],
        "id": details[0]["id"],
        "group_title": details[0]["group_title"],
        "books": list(
            set(detail["book_title"] for detail in details if detail["book_title"])
        ),
        "subjects": defaultdict(lambda: {"lessons": defaultdict(set)}),
    }

    for detail in details:
        lesson_title = detail["lesson_title"]
        subject_title = detail["subject_title"]
        mark_value = detail["mark_value"]

        if subject_title and lesson_title:
            organized_data["subjects"][subject_title]["lessons"][lesson_title].add(
                mark_value
            )

    # Convert sets back to lists for JSON serialization
    for subject in organized_data["subjects"].values():
        for lesson in subject["lessons"]:
            subject["lessons"][lesson] = list(subject["lessons"][lesson])

    return organized_data
