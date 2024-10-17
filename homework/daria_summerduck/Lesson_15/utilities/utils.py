import random
import re
from functools import wraps
from typing import Optional
from test_data import RandomData
from datetime import datetime, timedelta
from dataclasses import dataclass


# Dataclasses for storing random data
@dataclass
class RandomName:
    first_name: str
    last_name: str


@dataclass
class DateRange:
    start_date: str
    end_date: str


# Utility function: a decorator to handle exceptions
def handle_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            raise ValueError(f"Error in {func.__name__}: {error}")

    return wrapper


def generate_random_names(
    first_name: Optional[str] = None,
    last_names: Optional[str] = None,
) -> RandomName:
    name = first_name or random.choice(RandomData.random_first_names)
    second_name = last_names or random.choice(RandomData.random_last_names)

    return RandomName(first_name=name, last_name=second_name)


def generate_random_book_title() -> str:
    adjective = random.choice(RandomData.adjectives)
    noun = random.choice(RandomData.nouns)
    connector = random.choice(RandomData.connectors)
    second_noun = random.choice(RandomData.nouns)

    return f"The {adjective} {noun} {connector} the {second_noun}"


def generate_random_group_title() -> str:

    descriptor = random.choice(RandomData.group_descriptors)
    subject = random.choice(RandomData.group_subjects)
    theme = random.choice(RandomData.group_themes)

    return f"{descriptor} {subject} {theme}"


def generate_random_dates() -> DateRange:
    start_date = datetime(2020, 9, 1)  # Starting from September 2020
    end_date = datetime(2030, 9, 30)  # Until September 2030

    # Generate random date between the given range
    random_start_date = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    # Ensure end date is after start date, at least one month after
    random_end_date = random_start_date + timedelta(days=random.randint(30, 365))

    # Change format mm yyyy
    return DateRange(
        start_date=random_start_date.strftime("%m-%Y"),
        end_date=random_end_date.strftime("%m-%Y"),
    )


def generate_random_subject_title() -> str:

    subject = random.choice(RandomData.subjects)
    theme = random.choice(RandomData.themes)

    return f"{theme} of {subject}"


def generate_random_lesson_title(subject: str) -> str:
    lesson_topic = random.choice(RandomData.lesson_themes)

    return f"{lesson_topic} in {subject}"


def generate_random_mark() -> str:
    return random.choice(RandomData.marks)


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
