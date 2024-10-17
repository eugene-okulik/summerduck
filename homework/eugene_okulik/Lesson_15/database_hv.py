import mysql.connector as mysql
import random
from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class RandomName:
    first_name: str
    last_name: str


db = mysql.connect(
    user="st-onl",
    passwd="AVNS_tegPDkI5BlB2lW5eASC",
    host="db-mysql-fra1-09136-do-user-7651996-0.b.db.ondigitalocean.com",
    port=25060,
    database="st-onl",
)

cursor = db.cursor(dictionary=True)


# -- Создайте студента (student)
def generate_random_names(
    first_name: Optional[str] = None,
    last_names: Optional[str] = None,
) -> RandomName:
    random_first_names = [
        "Daria",
        "Eugene",
        "Alex",
        "Maria",
        "John",
    ]
    random_last_names = [
        "Summerduck",
        "Winterfox",
        "Springbreeze",
        "Autumnleaf",
        "Snowfall",
    ]

    name = first_name or random.choice(random_first_names)
    second_name = last_names or random.choice(random_last_names)

    return RandomName(first_name=name, last_name=second_name)


def create_student(
    name: str,
    second_name: str,
) -> str:
    insert_student_query = """
    INSERT INTO students (name, second_name, group_id)
    VALUES (%s, %s, NULL)
    """
    try:
        cursor.execute(insert_student_query, (name, second_name))
        print(f"Student {name} {second_name} created")
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error creating student: {error}")


def select_student_by_id(student_id: str) -> dict:
    select_student_by_id_query = """
    SELECT * from students where id = %s
    """
    try:
        cursor.execute(select_student_by_id_query, (student_id,))
        return cursor.fetchone()
    except Exception as error:
        raise ValueError(f"Error selecting student by id: {error}")


# -- Создайте несколько книг (books) и укажите, что ваш созданный студент взял их


def generate_random_book_title() -> str:
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

    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    connector = random.choice(connectors)
    second_noun = random.choice(nouns)

    return f"The {adjective} {noun} {connector} the {second_noun}"


def create_book(
    title: str,
):
    insert_books_query = """
    INSERT INTO books (title, taken_by_student_id)
    VALUES (%s, NULL)
    """
    try:
        cursor.execute(insert_books_query, (title,))
        print(f"Book '{title}' created")
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error creating book {title}: {error}")


def select_book_by_id(book_id: str) -> dict:
    select_book_by_id_query = """
    SELECT * from books where id = %s
    """
    try:
        cursor.execute(select_book_by_id_query, (book_id,))
        return cursor.fetchone()
    except Exception as error:
        raise ValueError(f"Error selecting book {book_id} by id: {error}")


def assigne_student_to_book(
    student_id: str,
    book_id: str,
) -> None:
    update_books_query = """
    UPDATE books
    SET taken_by_student_id=%s
    WHERE id=%s
    """
    try:
        cursor.execute(update_books_query, (student_id, book_id))
    except Exception as error:
        raise ValueError(
            f"Error assigning student {student_id} to book {book_id}: {error}"
        )


# -- Создайте группу (group) и определите своего студента туда
def generate_random_group_title() -> str:
    descriptors = [
        "Dynamic",
        "Innovative",
        "Creative",
        "Advanced",
        "Brilliant",
        "Elite",
    ]

    subjects = [
        "Developers",
        "Designers",
        "Engineers",
        "Thinkers",
        "Creators",
        "Strategists",
    ]

    themes = [
        "Alliance",
        "Collective",
        "Squad",
        "Team",
        "Network",
        "Circle",
    ]

    descriptor = random.choice(descriptors)
    subject = random.choice(subjects)
    theme = random.choice(themes)

    return f"{descriptor} {subject} {theme}"


@dataclass
class DateRange:
    start_date: str
    end_date: str


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


def create_group(
    title: str,
    start_date: str,
    end_date: str,
) -> str:
    insert_groups_query = """
    INSERT INTO `groups` (title, start_date, end_date)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(insert_groups_query, (title, start_date, end_date))
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error creating group {title}: {error}")


def select_group_by_id(group_id: str) -> dict:
    select_group_by_id_query = """
    SELECT * from `groups` where id = %s
    """
    try:
        cursor.execute(select_group_by_id_query, (group_id,))
        return cursor.fetchone()
    except Exception as error:
        raise ValueError(f"Error selecting group {group_id} by id: {error}")


def assigne_group_to_student(
    group_id: str,
    student_id: str,
):
    update_student_query = """
    UPDATE students SET group_id=%s
    WHERE id=%s
    """
    try:
        cursor.execute(update_student_query, (group_id, student_id))
    except Exception as error:
        raise ValueError(
            f"Error assigning group {group_id} to student {student_id}: {error}"
        )


# # -- Создайте несколько учебных предметов (subjects)
# def create_subject(
#     title: str | None = None,
# ):
#     insert_subjets_query = """
#     INSERT INTO subjets (title)
#     VALUES (%s);
#     """
#     title = title or f"Subjet_{random.randint(1, 100)}"
#     cursor.execute(insert_subjets_query, (title,))

#     subject_id = cursor.lastrowid

#     cursor.execute(f"SELECT * from subjets where id = {subject_id}")
#     print(f"Subjet created: \n{cursor.fetchone()}")

#     return subject_id


# subject_id = create_subject()


# # -- Создайте по два занятия для каждого предмета (lessons)
# def create_lesson(
#     subject_id: str,
#     title: str | None = None,
# ):
#     insert_lessons_query = """
#     INSERT INTO lessons (title, subject_id)
#     VALUES
#     (%s, %s)
#     """
#     title = title or f"Lesson_{random.randint(1, 5)}"

#     cursor.execute(insert_lessons_query, (title, subject_id))

#     lesson_id = cursor.lastrowid

#     cursor.execute(f"SELECT * from lessons where id = {lesson_id}")
#     print(f"Lesson {title} for subject {subject_id} created: \n{cursor.fetchone()}")

#     return lesson_id


# lesson_id = create_lesson(subject_id)


# # -- Поставьте своему студенту оценки (marks) для всех созданных вами занятий
# def add_mark_to_lesson(
#     lesson_id: str,
#     student_id: str,
#     value: str | None = None,
# ):
#     insert_marks_query = """
#     INSERT INTO marks (value, lesson_id, student_id)
#     VALUES (%s, %s, %s)
#     """
#     value = value or f"{random.randint(1, 10)}"

#     cursor.execute(insert_marks_query, (value, lesson_id, student_id))

#     mark_id = cursor.lastrowid

#     cursor.execute(f"SELECT * from marks where id = {mark_id}")
#     print(
#         f"Mark {value} added to lesson {lesson_id} and student {student_id}: \n{cursor.fetchone()}"
#     )

#     return mark_id


# mark_id = add_mark_to_lesson(lesson_id, student_id)

# # -- Все оценки студента


# def get_all_marks_for_student(student_id: str):
#     select_marks_query = """
#     SELECT * FROM marks WHERE student_id=%s ORDER BY id DESC
#     """
#     cursor.execute(select_marks_query, (student_id,))
#     return cursor.fetchall()


# # -- Все книги, которые находятся у студента


# def get_all_books_for_student(student_id: str):
#     select_books_query = """
#     SELECT * FROM books WHERE taken_by_student_id=%s ORDER BY id DESC
#     """
#     cursor.execute(select_books_query, (student_id,))
#     return cursor.fetchall()


# # -- Для вашего студента выведите всё, что о нем есть в базе:
# # группа, книги, оценки с названиями занятий и предметов
# # (всё одним запросом с использованием Join)


# def get_student_details(student_id: str):
#     select_student_details_query = """
#     SELECT
#         students.name,
#         students.second_name,
#         `groups`.title AS group_title,
#         books.title AS book_title,
#         marks.value AS mark_value,
#         lessons.title AS lesson_title,
#         subjets.title AS subject_title
#     FROM students
#     LEFT JOIN `groups` ON students.group_id = groups.id
#     LEFT JOIN books ON students.id = books.taken_by_student_id
#     LEFT JOIN marks ON students.id = marks.student_id
#     LEFT JOIN lessons ON marks.lesson_id = lessons.id
#     LEFT JOIN subjets ON lessons.subject_id = subjets.id
#     WHERE students.id = %s;
#     """
#     cursor.execute(select_student_details_query, (student_id,))
#     return cursor.fetchall()


# print(get_all_marks_for_student(student_id))
# print(get_all_books_for_student(student_id))
# print(get_student_details(student_id))

# Create a student
random_name = generate_random_names()

student_id = create_student(random_name.first_name, random_name.last_name)

# Verify the student is created
student_data = select_student_by_id(student_id)
print(student_data)


# Create a book
book_title = generate_random_book_title()

book_id = create_book(book_title)

book_data = select_book_by_id(book_id)

# Check if the book is not assigned to any student initially
assert (
    book_data["taken_by_student_id"] is None
), "Book should not be assigned to any student initially"

# Assign the book to the student
assigne_student_to_book(student_id, book_id)

# Verify the book is now assigned to the student
book_data = select_book_by_id(book_id)
assert (
    book_data["taken_by_student_id"] == student_id
), "Book should be assigned to the student now"

print(f"Book '{book_title}' assigned to student ID {student_id}: \n{book_data}")

group_title = generate_random_group_title()
print(f"Group title: {group_title}")
random_date = generate_random_dates()
print(f"Group start date: {random_date.start_date}")
print(f"Group end date: {random_date.end_date}")
group_id = create_group(group_title, random_date.start_date, random_date.end_date)
group_info = select_group_by_id(group_id)
print(f"Group '{group_title}' created: \n{group_info}")

assigne_group_to_student(group_id, student_id)

student_data = select_student_by_id(student_id)
print(student_data)

# db.commit()
db.close()
