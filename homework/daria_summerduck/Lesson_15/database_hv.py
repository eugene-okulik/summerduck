import mysql.connector as mysql
import random
from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from test_data import RandomData


# Dataclasses for storing random data
@dataclass
class RandomName:
    first_name: str
    last_name: str


@dataclass
class DateRange:
    start_date: str
    end_date: str


# Connect to the database
db = mysql.connect(
    user="st-onl",
    passwd="AVNS_tegPDkI5BlB2lW5eASC",
    host="db-mysql-fra1-09136-do-user-7651996-0.b.db.ondigitalocean.com",
    port=25060,
    database="st-onl",
)

# Create a cursor
cursor = db.cursor(dictionary=True)


def generate_random_names(
    first_name: Optional[str] = None,
    last_names: Optional[str] = None,
) -> RandomName:
    name = first_name or random.choice(RandomData.random_first_names)
    second_name = last_names or random.choice(RandomData.random_last_names)

    return RandomName(first_name=name, last_name=second_name)


def create_student(
    name: str,
    second_name: str,
):
    insert_student_query = """
    INSERT INTO students (name, second_name, group_id)
    VALUES (%s, %s, NULL)
    """
    try:
        cursor.execute(insert_student_query, (name, second_name))
        print(f"Student '{name} {second_name}' created")
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error creating student: {error}")


def select_student_by_id(student_id: str):
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
    adjective = random.choice(RandomData.adjectives)
    noun = random.choice(RandomData.nouns)
    connector = random.choice(RandomData.connectors)
    second_noun = random.choice(RandomData.nouns)

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


def select_book_by_id(book_id: str):
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

        print(f"Student '{student_id}' assigned to book '{book_id}'")
    except Exception as error:
        raise ValueError(
            f"Error assigning student {student_id} to book {book_id}: {error}"
        )


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


def create_group(
    title: str,
    start_date: str,
    end_date: str,
):
    insert_groups_query = """
    INSERT INTO `groups` (title, start_date, end_date)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(insert_groups_query, (title, start_date, end_date))

        print(f"Group '{title}' created")
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error creating group {title}: {error}")


def select_group_by_id(group_id: str):
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

        print(f"Student {student_id} assigned to group '{group_id}'")
    except Exception as error:
        raise ValueError(
            f"Error assigning group {group_id} to student {student_id}: {error}"
        )


def generate_random_subject_title() -> str:

    subject = random.choice(RandomData.subjects)
    theme = random.choice(RandomData.themes)

    return f"{theme} of {subject}"


def create_subject(
    title: str,
):
    insert_subjects_query = """
    INSERT INTO subjets (title)
    VALUES (%s);
    """
    try:
        cursor.execute(insert_subjects_query, (title,))

        print(f"Subject '{title}' created")
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error creating subject {title}: {error}")


def select_subject_by_id(subject_id: str):
    select_subject_by_id_query = """
    SELECT * from subjets where id = %s
    """
    try:
        cursor.execute(select_subject_by_id_query, (subject_id,))

        return cursor.fetchone()
    except Exception as error:
        raise ValueError(f"Error selecting subject {subject_id} by id: {error}")


def generate_random_lesson_title(subject: str) -> str:
    lesson_topic = random.choice(RandomData.lesson_themes)

    return f"{lesson_topic} in {subject}"


def create_lesson(
    subject_id: str,
    title: str,
):
    insert_lessons_query = """
    INSERT INTO lessons (title, subject_id)
    VALUES
    (%s, %s)
    """
    try:
        cursor.execute(insert_lessons_query, (title, subject_id))
        print(f"Lesson '{title}' created")
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error creating lesson {title}: {error}")


def select_lesson_by_id(lesson_id: str):
    try:
        cursor.execute(f"SELECT * from lessons where id = {lesson_id}")

        return cursor.fetchone()
    except Exception as error:
        raise ValueError(f"Error selecting lesson {lesson_id} by id: {error}")


def generate_random_mark() -> str:
    return random.choice(RandomData.marks)


def add_mark_to_lesson(
    lesson_id: str,
    student_id: str,
    value: str,
):
    insert_marks_query = """
    INSERT INTO marks (value, lesson_id, student_id)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(insert_marks_query, (value, lesson_id, student_id))

        print(
            f"Mark '{value}' added to lesson '{lesson_id}' and student '{student_id}'"
        )
        return cursor.lastrowid
    except Exception as error:
        raise ValueError(f"Error adding mark {value} to lesson {lesson_id}: {error}")


def get_all_marks_for_student(student_id: str) -> list:
    select_marks_query = """
    SELECT * FROM marks WHERE student_id=%s ORDER BY id DESC
    """
    try:
        cursor.execute(select_marks_query, (student_id,))

        return cursor.fetchall()
    except Exception as error:
        raise ValueError(f"Error selecting marks for student {student_id}: {error}")


def get_all_books_for_student(student_id: str) -> list:
    select_books_query = """
    SELECT * FROM books WHERE taken_by_student_id=%s ORDER BY id DESC
    """
    try:
        cursor.execute(select_books_query, (student_id,))

        return cursor.fetchall()
    except Exception as error:
        raise ValueError(f"Error selecting books for student {student_id}: {error}")


def get_student_details(student_id: str):
    """
    Retrieve all available information about a student from the database:
    group, books, grades with the names of lessons and subjects
    (all in one query using JOIN).
    """
    select_student_details_query = """
    SELECT
        students.name,
        students.second_name,
        `groups`.title AS group_title,
        books.title AS book_title,
        marks.value AS mark_value,
        lessons.title AS lesson_title,
        subjets.title AS subject_title
    FROM students
    LEFT JOIN `groups` ON students.group_id = groups.id
    LEFT JOIN books ON students.id = books.taken_by_student_id
    LEFT JOIN marks ON students.id = marks.student_id
    LEFT JOIN lessons ON marks.lesson_id = lessons.id
    LEFT JOIN subjets ON lessons.subject_id = subjets.id
    WHERE students.id = %s;
    """
    try:
        cursor.execute(select_student_details_query, (student_id,))

        return cursor.fetchall()
    except Exception as error:
        raise ValueError(
            f"Error selecting student details for student {student_id}: {error}"
        )


# Create a student
random_name = generate_random_names()
student_id = create_student(random_name.first_name, random_name.last_name)

# Verify the student is created
student_data = select_student_by_id(student_id)

# Check if the student is not assigned to any group initially
assert (
    student_data["group_id"] is None
), "Student should not be assigned to any group initially"

# Create a book
book_title = generate_random_book_title()
book_id = create_book(book_title)

# Verify the book is created
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

# Create a group
group_title = generate_random_group_title()
random_date = generate_random_dates()
group_id = create_group(group_title, random_date.start_date, random_date.end_date)

# Verify the group is created
group_info = select_group_by_id(group_id)

# Assign the student to the group
assigne_group_to_student(group_id, student_id)

# Check if the student is assigned to the group
student_data = select_student_by_id(student_id)
assert (
    student_data["group_id"] == group_id
), "Student should be assigned to the group now"

# Create a subject
subject_title = generate_random_subject_title()
subject_id = create_subject(subject_title)

# Verify the subject is created
subject_info = select_subject_by_id(subject_id)

# Create lessons for the subject
lesson_title = generate_random_lesson_title(subject_title)
lesson_id = create_lesson(subject_id, lesson_title)

# Verify the lesson is created
lesson_info = select_lesson_by_id(lesson_id)

# Add a mark to the lesson
mark_value = generate_random_mark()
add_mark_to_lesson(lesson_id, student_id, mark_value)

# Verify the mark is added to the lesson
marks = get_all_marks_for_student(student_id)
assert len(marks) == 1, "There should be only one mark for the student"
assert marks[0]["value"] == mark_value, "Mark value should be the same"

# Get all books for the student
books = get_all_books_for_student(student_id)
assert len(books) == 1, "There should be only one book for the student"
assert books[0]["title"] == book_title, "Book title should be the same"

# Get all details for the student
student_details = get_student_details(student_id)
assert len(student_details) == 1, "There should be only one student details"
assert student_details[0]["name"] == random_name.first_name, "Name should be the same"
assert (
    student_details[0]["second_name"] == random_name.last_name
), "Second name should be the same"
assert (
    student_details[0]["group_title"] == group_title
), "Group title should be the same"
assert student_details[0]["book_title"] == book_title, "Book title should be the same"
assert student_details[0]["mark_value"] == mark_value, "Mark value should be the same"
assert (
    student_details[0]["lesson_title"] == lesson_title
), "Lesson title should be the same"
assert (
    student_details[0]["subject_title"] == subject_title
), "Subject title should be the same"


# Close the database connection
db.close()
