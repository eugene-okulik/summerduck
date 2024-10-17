import random
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class DateRange:
    start_date: str
    end_date: str


class RandomData:
    first_names = [
        "Daria",
        "Eugene",
        "Alex",
        "Maria",
        "John",
    ]

    last_names = [
        "Summerduck",
        "Winterfox",
        "Springbreeze",
        "Autumnleaf",
        "Snowfall",
    ]

    subjects = [
        "Physics",
        "Mathematics",
        "Philosophy",
        "Computer Science",
        "History",
        "Biology",
    ]

    lesson_themes = [
        "Overview",
        "Key Concepts",
        "Fundamentals",
        "Applications",
        "Case Studies",
        "Challenges",
    ]

    adjectives = [
        "Mysterious",
        "Forgotten",
        "Enchanted",
        "Whispering",
        "Lost",
        "Silent",
    ]

    nouns = [
        "Journey",
        "Forest",
        "Legacy",
        "Ocean",
        "Castle",
        "Secret",
    ]

    connectors = [
        "of",
        "and",
        "in",
        "to",
    ]

    marks = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
    ]

    themes = [
        "Introduction",
        "Foundations",
        "Advanced Concepts",
        "Principles",
        "Theory",
        "Applications",
    ]

    group_descriptors = [
        "Dynamic",
        "Innovative",
        "Creative",
        "Elite",
        "Advanced",
    ]

    group_subjects = [
        "Developers",
        "Designers",
        "Engineers",
        "Thinkers",
        "Creators",
    ]

    group_themes = [
        "Alliance",
        "Collective",
        "Squad",
        "Team",
        "Network",
    ]

    @classmethod
    def first_name(cls) -> str:
        """Returns a random first name from the list."""
        return random.choice(cls.first_names)

    @classmethod
    def last_name(cls) -> str:
        """Returns a random last name from the list."""
        return random.choice(cls.last_names)

    @classmethod
    def book_title(cls) -> str:
        """Generates a random book title."""
        return (
            f"The {random.choice(cls.adjectives)} "
            f"{random.choice(cls.nouns)} "
            f"{random.choice(cls.connectors)} "
            f"the {random.choice(cls.nouns)}"
        )

    @classmethod
    def group_title(cls) -> str:
        """Generates a random group title."""
        return (
            f"{random.choice(cls.group_descriptors)} "
            f"{random.choice(cls.group_subjects)} "
            f"{random.choice(cls.group_themes)}"
        )

    @classmethod
    def start_and_end_dates(
        cls,
        start: datetime = datetime(2020, 9, 1),
        end: datetime = datetime(2030, 9, 30),
        date_format: str = "%m-%Y",
    ) -> DateRange:
        """Generates a random start and end date within the given range."""
        random_start_date = start + timedelta(
            days=random.randint(0, (end - start).days)
        )
        assert random_start_date < end, "Start date should be before end date."
        random_end_date = random_start_date + timedelta(days=random.randint(30, 365))
        return DateRange(
            start_date=random_start_date.strftime(date_format),
            end_date=random_end_date.strftime(date_format),
        )

    @classmethod
    def subject_title(cls) -> str:
        """Generates a random subject title."""
        return f"{random.choice(cls.themes)} of {random.choice(cls.subjects)}"

    @classmethod
    def lesson_title(cls, subject: str) -> str:
        """Generates a random lesson title."""
        return f"{random.choice(cls.lesson_themes)} in {subject}"

    @classmethod
    def mark(cls) -> str:
        """Returns a random mark from the list."""
        return random.choice(cls.marks)
