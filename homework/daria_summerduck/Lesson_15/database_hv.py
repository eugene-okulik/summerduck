import logging
import mysql.connector as mysql
from utilities import utils
from test_data import RandomData as Random

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log level, can be DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("app.log"),  # Write logs to a file
        logging.StreamHandler(),  # Output logs to the console
    ],
)

# Connect to the database
try:
    db = mysql.connect(
        user="st-onl",
        passwd="AVNS_tegPDkI5BlB2lW5eASC",
        host="db-mysql-fra1-09136-do-user-7651996-0.b.db.ondigitalocean.com",
        port=25060,
        database="st-onl",
    )
    logging.info("Successfully connected to the database.")
except mysql.Error as e:
    logging.error(f"Error connecting to the database: {e}")
    raise

# Create a cursor
cursor = db.cursor(dictionary=True)


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_student(
    name: str,
    second_name: str,
):
    # Parameterized query
    insert_student_query = """
    INSERT INTO students (name, second_name, group_id)
    VALUES (%s, %s, NULL)
    """

    cursor.execute(insert_student_query, (name, second_name))
    logging.info(f"Student '{name} {second_name}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_student_by_id(student_id: int):
    # Parameterized query
    select_student_by_id_query = """
    SELECT * from students where id = %s
    """
    cursor.execute(select_student_by_id_query, (student_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_book(
    title: str,
):
    # Parameterized query
    insert_books_query = """
    INSERT INTO books (title, taken_by_student_id)
    VALUES (%s, NULL)
    """
    cursor.execute(insert_books_query, (title,))
    logging.info(f"Book '{title}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_book_by_id(book_id: int):
    # Parameterized query
    select_book_by_id_query = """
    SELECT * from books where id = %s
    """
    cursor.execute(select_book_by_id_query, (book_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def assigne_student_to_book(
    student_id: int,
    book_id: int,
) -> None:
    # Parameterized query
    update_books_query = """
    UPDATE books
    SET taken_by_student_id=%s
    WHERE id=%s
    """
    cursor.execute(update_books_query, (student_id, book_id))
    logging.info(f"Student '{student_id}' assigned to book '{book_id}'")


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_group(
    title: str,
    start_date: str,
    end_date: str,
):
    # Parameterized query
    insert_groups_query = """
    INSERT INTO `groups` (title, start_date, end_date)
    VALUES (%s, %s, %s)
    """

    cursor.execute(insert_groups_query, (title, start_date, end_date))
    logging.info(f"Group '{title}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_group_by_id(group_id: int):
    # Parameterized query
    select_group_by_id_query = """
    SELECT * from `groups` where id = %s
    """

    cursor.execute(select_group_by_id_query, (group_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def assigne_group_to_student(
    group_id: int,
    student_id: int,
):
    # Parameterized query
    update_student_query = """
    UPDATE students SET group_id=%s
    WHERE id=%s
    """

    cursor.execute(update_student_query, (group_id, student_id))
    logging.info(f"Student {student_id} assigned to group '{group_id}'")


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_subject(
    title: str,
):
    # Parameterized query
    insert_subjects_query = """
    INSERT INTO subjets (title)
    VALUES (%s);
    """

    cursor.execute(insert_subjects_query, (title,))
    logging.info(f"Subject '{title}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_subject_by_id(subject_id: int):
    # Parameterized query
    select_subject_by_id_query = """
    SELECT * from subjets where id = %s
    """

    cursor.execute(select_subject_by_id_query, (subject_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_lesson(
    subject_id: int,
    title: str,
):
    # Parameterized query
    insert_lessons_query = """
    INSERT INTO lessons (title, subject_id)
    VALUES
    (%s, %s)
    """

    cursor.execute(insert_lessons_query, (title, subject_id))
    logging.info(f"Lesson '{title}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_lesson_by_id(lesson_id: int):
    # Parameterized query
    select_lesson_by_id_query = """
    SELECT * from lessons where id = %s
    """

    cursor.execute(select_lesson_by_id_query, (lesson_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def add_mark_to_lesson(
    lesson_id: int,
    student_id: int,
    value: str,
):
    # Parameterized query
    insert_marks_query = """
    INSERT INTO marks (value, lesson_id, student_id)
    VALUES (%s, %s, %s)
    """

    cursor.execute(insert_marks_query, (value, lesson_id, student_id))
    logging.info(
        f"Mark '{value}' added to lesson '{lesson_id}' and student '{student_id}'"
    )
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def get_all_marks_for_student(student_id: int) -> list:
    # Parameterized query
    select_marks_query = """
    SELECT * FROM marks WHERE student_id=%s ORDER BY id DESC
    """

    cursor.execute(select_marks_query, (student_id,))
    return cursor.fetchall()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def get_all_books_for_student(student_id: int) -> list:
    # Parameterized query
    select_books_query = """
    SELECT * FROM books WHERE taken_by_student_id=%s ORDER BY id DESC
    """

    cursor.execute(select_books_query, (student_id,))
    return cursor.fetchall()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def get_student_details(student_id: int):
    """
    Retrieve all available information about a student from the database:
    group, books, grades with the names of lessons and subjects
    (all in one query using JOIN).
    """
    # Parameterized query
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

    cursor.execute(select_student_details_query, (student_id,))
    return cursor.fetchall()


# Close the database connection properly at the end of the script
def close_connection():
    if db.is_connected():
        cursor.close()
        db.close()
        logging.info("Database connection closed.")


# Commit the changes
def commit_changes():
    try:
        db.commit()
        logging.info("Changes committed successfully")
    except mysql.Error as e:
        logging.error(f"Error committing changes: {e}")
        db.rollback()
        raise
    finally:
        close_connection()


# Create a student
first_name = Random.first_name()
last_name = Random.last_name()
student_id = create_student(first_name, last_name)
logging.info(f"Student ID {student_id}")

# Verify the student is created
student_data = select_student_by_id(student_id)

# Check if the student is not assigned to any group initially
assert (
    student_data["group_id"] is None
), "Student should not be assigned to any group initially"

# Create a book
book_title = Random.book_title()
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
group_title = Random.group_title()
date = Random.start_and_end_dates()
group_id = create_group(group_title, date.start_date, date.end_date)

# Verify the group is created
group_info = select_group_by_id(group_id)

# Assign the student to the group
assigne_group_to_student(group_id, student_id)

# Check if the student is assigned to the group
student_data = select_student_by_id(student_id)
assert (
    student_data["group_id"] == group_id
), "Student should be assigned to the group now"
logging.info(f"PASSED: Student '{student_id}' is assigned to the group '{group_id}'")

# Create a subject
subject_title = Random.subject_title()
subject_id = create_subject(subject_title)

# Verify the subject is created
subject_info = select_subject_by_id(subject_id)

# Create lessons for the subject
lesson_title = Random.lesson_title(subject_title)
lesson_id = create_lesson(subject_id, lesson_title)

# Verify the lesson is created
lesson_info = select_lesson_by_id(lesson_id)

# Add a mark to the lesson
mark_value = Random.mark()
add_mark_to_lesson(lesson_id, student_id, mark_value)

# Verify the mark is added to the lesson
marks = get_all_marks_for_student(student_id)
assert len(marks) == 1, "There should be only one mark for the student"
assert marks[0]["value"] == mark_value, "Mark value should be the same"
logging.info(f"PASSED: Mark '{mark_value}' is added to the lesson '{lesson_id}'")

# Get all books for the student
books = get_all_books_for_student(student_id)
assert len(books) == 1, "There should be only one book for the student"
assert books[0]["title"] == book_title, "Book title should be the same"
logging.info(f"PASSED: Book '{book_title}' is assigned to the student '{student_id}'")

# Get all details for the student
student_details = get_student_details(student_id)
assert len(student_details) == 1, "There should be only one student details"
assert student_details[0]["name"] == first_name, "Name should be the same"
assert student_details[0]["second_name"] == last_name, "Second name should be the same"
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
logging.info("PASSED: Student details are retrieved successfully")

# Commit the changes
commit_changes()

# Close the database connection
close_connection()
