import json
import logging
import os
import csv
import mysql.connector as mysql
from dotenv import load_dotenv
from utilities import utils
from faker import Faker

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG, DEBUG, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        # logging.FileHandler("app.log"),  # Write logs to a file
        logging.StreamHandler(),  # Output logs to the console
    ],
)


# Connect to the database
def connect_to_db():
    load_dotenv()
    try:
        db = mysql.connect(
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSW"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
        )
        logging.info("Successfully connected to the database.")
        return db
    except mysql.Error as e:
        logging.error(f"Error connecting to the database: {e}")
        raise


# Create a cursor
def create_cursor():
    return db.cursor(dictionary=True)


db = connect_to_db()
cursor = create_cursor()


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
    except mysql.Error as e:
        logging.error(f"Error committing changes: {e}")
        db.rollback()
        raise


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_student(
    name: str,
    second_name: str,
):
    # Parameterized query
    INSERT_STUDENT_QUERY = """
    INSERT INTO students (name, second_name, group_id)
    VALUES (%s, %s, NULL)
    """

    cursor.execute(INSERT_STUDENT_QUERY, (name, second_name))
    commit_changes()
    student_id = cursor.lastrowid
    logging.debug(f"Student '{name} {second_name}' created")
    logging.debug(f"Student ID {student_id}")
    return student_id


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_student_by_id(student_id: int):
    # Parameterized query
    SELECT_STUDENT_BY_ID_QUERY = """
    SELECT * from students where id = %s
    """
    cursor.execute(SELECT_STUDENT_BY_ID_QUERY, (student_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_book(
    title: str,
):
    # Parameterized query
    INSERT_BOOKS_QUERY = """
    INSERT INTO books (title, taken_by_student_id)
    VALUES (%s, NULL)
    """
    cursor.execute(INSERT_BOOKS_QUERY, (title,))
    commit_changes()
    logging.debug(f"Book '{title}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_book_by_id(book_id: int):
    # Parameterized query
    SELECT_BOOK_BY_ID_QUERY = """
    SELECT * from books where id = %s
    """
    cursor.execute(SELECT_BOOK_BY_ID_QUERY, (book_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def assign_student_to_book(
    student_id: int,
    book_id: int,
) -> None:
    # Parameterized query
    UPDATE_BOOKS_QUERY = """
    UPDATE books
    SET taken_by_student_id=%s
    WHERE id=%s
    """
    cursor.execute(UPDATE_BOOKS_QUERY, (student_id, book_id))
    commit_changes()
    logging.debug(f"Student '{student_id}' assigned to book '{book_id}'")


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_group(
    title: str,
    start_date: str,
    end_date: str,
):
    # Parameterized query
    INSERT_GROUPS_QUERY = """
    INSERT INTO `groups` (title, start_date, end_date)
    VALUES (%s, %s, %s)
    """

    cursor.execute(INSERT_GROUPS_QUERY, (title, start_date, end_date))
    commit_changes()
    group_id = cursor.lastrowid
    logging.debug(f"Group '{title}' created")
    logging.debug(f"Group ID {group_id}")
    return group_id


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_group_by_id(group_id: int):
    # Parameterized query
    SELECT_GROUP_BY_ID_QUERY = """
    SELECT * from `groups` where id = %s
    """

    cursor.execute(SELECT_GROUP_BY_ID_QUERY, (group_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def assign_group_to_student(
    group_id: int,
    student_id: int,
):
    # Parameterized query
    UPDATE_STUDENT_QUERY = """
    UPDATE students SET group_id=%s
    WHERE id=%s
    """

    cursor.execute(UPDATE_STUDENT_QUERY, (group_id, student_id))
    commit_changes()
    logging.debug(f"Student {student_id} assigned to group '{group_id}'")


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_subject(
    title: str,
):
    # Parameterized query
    INSERT_SUBJECTS_QUERY = """
    INSERT INTO subjets (title)
    VALUES (%s);
    """

    cursor.execute(INSERT_SUBJECTS_QUERY, (title,))
    commit_changes()
    logging.debug(f"Subject '{title}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_subject_by_id(subject_id: int):
    # Parameterized query
    SELECT_SUBJECT_BY_ID_QUERY = """
    SELECT * from subjets where id = %s
    """

    cursor.execute(SELECT_SUBJECT_BY_ID_QUERY, (subject_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def create_lesson(
    subject_id: int,
    title: str,
):
    # Parameterized query
    INSERT_LESSONS_QUERY = """
    INSERT INTO lessons (title, subject_id)
    VALUES
    (%s, %s)
    """

    cursor.execute(INSERT_LESSONS_QUERY, (title, subject_id))
    commit_changes()
    logging.debug(f"Lesson '{title}' created")
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def select_lesson_by_id(lesson_id: int):
    # Parameterized query
    SELECT_LESSON_BY_ID_QUERY = """
    SELECT * from lessons where id = %s
    """

    cursor.execute(SELECT_LESSON_BY_ID_QUERY, (lesson_id,))
    return cursor.fetchone()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def add_mark_to_lesson(
    lesson_id: int,
    student_id: int,
    value: str,
):
    # Parameterized query
    INSERT_MARKS_QUERY = """
    INSERT INTO marks (value, lesson_id, student_id)
    VALUES (%s, %s, %s)
    """

    cursor.execute(INSERT_MARKS_QUERY, (value, lesson_id, student_id))
    commit_changes()
    logging.debug(
        f"Mark '{value}' added to lesson '{lesson_id}' and student '{student_id}'"
    )
    return cursor.lastrowid


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def get_all_marks_for_student(student_id: int) -> list:
    # Parameterized query
    SELECT_MARKS_QUERY = """
    SELECT * FROM marks WHERE student_id=%s ORDER BY id DESC
    """

    cursor.execute(SELECT_MARKS_QUERY, (student_id,))
    return cursor.fetchall()


@utils.validate_and_sanitize_params
@utils.handle_db_exceptions
def get_all_books_for_student(student_id: int) -> list:
    # Parameterized query
    SELECT_BOOKS_QUERY = """
    SELECT * FROM books WHERE taken_by_student_id=%s ORDER BY id DESC
    """

    cursor.execute(SELECT_BOOKS_QUERY, (student_id,))
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
    SELECT_STUDENT_DETAILS_QUERY = """
    SELECT
        students.name,
        students.second_name,
        students.id,
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

    cursor.execute(SELECT_STUDENT_DETAILS_QUERY, (student_id,))
    return cursor.fetchall()


def check_csv_data_in_db(csv_file_path: str):
    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                student_name = row["name"]
                student_second_name = row["second_name"]
                book_title = row["book_title"]
                subject_title = row["subject_title"]
                lesson_title = row["lesson_title"]
                mark_value = row["mark_value"]
            except KeyError as e:
                raise ValueError(f"Missing key in CSV: {e}")

            # Check if student exists
            student_query = """
            SELECT * FROM students WHERE name=%s AND second_name=%s
            """
            cursor.execute(student_query, (student_name, student_second_name))
            student = cursor.fetchone()
            if not student:
                logging.warning(
                    f"Student {student_name} {student_second_name} not found in the database."
                )
                continue

            student_id = student["id"]

            # Check if book exists
            book_query = """
            SELECT * FROM books WHERE title=%s AND taken_by_student_id=%s
            """
            cursor.execute(book_query, (book_title, student_id))
            book = cursor.fetchone()
            if not book:
                logging.warning(
                    f"Book {book_title} not found for student {student_name} {student_second_name}."
                )
                continue

            # Check if subject exists
            subject_query = """
            SELECT * FROM subjets WHERE title=%s
            """
            cursor.execute(subject_query, (subject_title,))
            subject = cursor.fetchone()
            if not subject:
                logging.warning(f"Subject {subject_title} not found in the database.")
                continue

            subject_id = subject["id"]

            # Check if lesson exists
            lesson_query = """
            SELECT * FROM lessons WHERE title=%s AND subject_id=%s
            """
            cursor.execute(lesson_query, (lesson_title, subject_id))
            lesson = cursor.fetchone()
            if not lesson:
                logging.warning(
                    f"Lesson {lesson_title} not found for subject {subject_title}."
                )
                continue

            lesson_id = lesson["id"]

            # Check if mark exists
            mark_query = """
            SELECT * FROM marks WHERE value=%s AND lesson_id=%s AND student_id=%s
            """
            cursor.execute(mark_query, (mark_value, lesson_id, student_id))
            mark = cursor.fetchone()
            if not mark:
                logging.warning(
                    f"Mark {mark_value} not found for lesson {lesson_title} "
                    f"and student {student_name} {student_second_name}."
                )
                continue

            logging.info(
                f"All data for student {student_name} {student_second_name} is present in the database."
            )


# Constants for the script
BOOK_NUMBER = 2
SUBJECT_NUMBER = 2
LESSONS_PER_SUBJECT = 3


def main():

    try:
        lesson_number = input("Select lesson 15 or 16 and press Enter: ")
        match lesson_number:
            case "15":
                # Generate fake data
                fake = Faker()
                first_name = fake.first_name()
                last_name = fake.last_name()
                group_title = fake.word()
                start_date = fake.past_date()
                end_date = fake.future_date()
                subject_titles = [fake.word() for _ in range(SUBJECT_NUMBER)]

                # Create a student
                student_id = create_student(first_name, last_name)

                # Get the student data
                student_data = select_student_by_id(student_id)
                print(student_data)

                # Check if the student is not assigned to any group initially
                assert (
                    student_data["group_id"] is None
                ), "Student should not be assigned to any group initially"

                # Create a group
                group_id = create_group(group_title, start_date, end_date)

                # Assign the student to the group
                assign_group_to_student(group_id, student_id)

                # Check if the student is assigned to the group
                student_data = select_student_by_id(student_id)
                assert (
                    student_data["group_id"] == group_id
                ), "Student should be assigned to the group now"
                logging.debug(
                    f"PASSED: Student '{student_id}' is assigned to the group '{group_id}'"
                )

                # Create and assign books to the student

                for _ in range(BOOK_NUMBER):
                    # Create a book
                    book_title = f"{fake.sentence(nb_words=3).strip('.')} of {fake.word().capitalize()}"
                    book_id = create_book(book_title)

                    # Assign the book to the student
                    assign_student_to_book(student_id, book_id)

                    # Verify the book is assigned to the student
                    book_data = select_book_by_id(book_id)
                    assert (
                        book_data["taken_by_student_id"] == student_id
                    ), "Book should be assigned to the student"
                    logging.debug(
                        f"PASSED: Book '{book_id}' is assigned to the student '{student_id}'"
                    )

                # Create multiple subjects
                subject_ids = [create_subject(title) for title in subject_titles]

                # Create two lessons for each subject and add marks for the student
                for subject_id, subject_title in zip(subject_ids, subject_titles):
                    for _ in range(LESSONS_PER_SUBJECT):
                        # Generate random data
                        lesson_title = f"{fake.sentence(nb_words=3).strip('.')} of {fake.word().capitalize()}"
                        mark_value = fake.random_int(min=1, max=10)

                        # Create a lesson and add a mark to it
                        lesson_id = create_lesson(subject_id, lesson_title)
                        add_mark_to_lesson(lesson_id, student_id, mark_value)

                # Get all marks for the student
                marks = get_all_marks_for_student(student_id)
                assert (
                    len(marks) == LESSONS_PER_SUBJECT * SUBJECT_NUMBER
                ), "There should be marks for all lessons"
                logging.debug(
                    f"PASSED: {len(marks)} marks are added to the student '{student_id}'"
                )

                # Get all books for the student
                books = get_all_books_for_student(student_id)
                assert (
                    len(books) == BOOK_NUMBER
                ), f"There should be only {BOOK_NUMBER} books for the student"
                logging.debug(
                    f"PASSED: {len(books)} books is assigned to the student '{student_id}'"
                )

                # Get all details for the student
                student_details = get_student_details(student_id)
                assert student_details, "Student details should not be empty"
                # logging.debug(f"Student full details: \n{student_details}")
                # logging.debug("PASSED: Student details are retrieved successfully")

                # Organize the student details and print them
                organized_student_details = utils.organize_student_details(
                    student_details
                )
                logging.info(
                    f"Organized student details: \n{json.dumps(organized_student_details, indent=4)}"
                )

                # Commit the changes
                commit_changes()

            case "16":
                # Check CSV data in the database
                csv_file_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    "eugene_okulik",
                    "Lesson_16",
                    "hw_data",
                    "data.csv",
                )
                check_csv_data_in_db(csv_file_path)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        db.rollback()
        raise

    finally:
        # Close the database connection
        close_connection()


if __name__ == "__main__":
    main()
