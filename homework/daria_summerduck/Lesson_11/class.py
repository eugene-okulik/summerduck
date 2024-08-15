"""
Библиотека

** Первый класс **
Создайте класс `Book` с атрибутами:
- материал страниц
- наличие текста
- название книги
- автор
- кол-во страниц
- ISBN
- флаг зарезервирована ли книга или нет (True/False).

Какие-то из атрибутов будут общими для всех книг (материал, наличие текста), какие-то индивидуальными.

** Tasks **
1. Создайте несколько (штук 5) экземпляров разных книг.
2. После создания пометьте одну книгу как зарезервированную.
3. Распечатайте детали о каждой книге в таком виде:
    - Если книга зарезервирована:
      Название: Идиот, Автор: Достоевский, страниц: 500, материал: бумага, зарезервирована
    - Если не зарезервирована:
      Название: Идиот, Автор: Достоевский, страниц: 500, материал: бумага


** Второй класс **
Создайте дочерний класс для первого. Это будет класс для школьных учебников. В нем будут дополнительные атрибуты:
- предмет (типа математика, история, география)
- класс (школьный класс, для которого этот учебник)
    (осторожно с названием переменной. `class` - зарезервированное слово)
- наличие заданий (bool)

** Tasks **
1. Создайте несколько экземпляров учебников.
2. После создания пометьте один учебник как зарезервированный.
3. Распечатайте детали о каждом учебнике в таком виде:
    - Если учебник зарезервирован:
      Название: Алгебра, Автор: Иванов, страниц: 200, предмет: Математика, класс: 9, зарезервирована
    - Если не зарезервирован:
      Название: Алгебра, Автор: Иванов, страниц: 200, предмет: Математика, класс: 9
"""


class Book:
    material = "бумага"
    has_text = True

    def __init__(self, title, author, pages, isbn, reserved: bool = False):
        self.title = title
        self.author = author
        self.pages = pages
        self.isbn = isbn
        self.reserved = reserved

    def __str__(self):
        reserved_status = "зарезервирована" if self.reserved else ""
        return (
            f"Название: {self.title}, "
            f"Автор: {self.author}, "
            f"страниц: {self.pages}, "
            f"материал: {self.material} {reserved_status}".strip()
        )


class Textbook(Book):
    def __init__(
        self,
        title,
        author,
        pages,
        isbn,
        subject,
        grade,
        has_exercises: bool,
        reserved: bool = False,
    ):
        super().__init__(title, author, pages, isbn, reserved)
        self.subject = subject
        self.grade = grade
        self.has_exercises = has_exercises

    def __str__(self):
        reserved_status = "зарезервирована" if self.reserved else ""
        return (
            f"Название: {self.title}, "
            f"Автор: {self.author}, "
            f"страниц: {self.pages}, "
            f"предмет: {self.subject}, "
            f"класс: {self.grade} {reserved_status}".strip()
        )


# Создание экземпляров книг
book1 = Book(
    title="Идиот",
    author="Фёдор Достоевский",
    pages=500,
    isbn="1234567890",
)
book2 = Book(
    title="Война и мир",
    author="Лев Толстой",
    pages=1225,
    isbn="0987654321",
)
book3 = Book(
    title="Преступление и наказание",
    author="Фёдор Достоевский",
    pages=671,
    isbn="1122334455",
)
book4 = Book(
    title="Анна Каренина",
    author="Лев Толстой",
    pages=864,
    isbn="2233445566",
)
book5 = Book(
    title="Мастер и Маргарита",
    author="Михаил Булгаков",
    pages=470,
    isbn="3344556677",
)

# Пометка одной книгм как зарезервированной
book5.reserved = True

# Печать деталей о книгах
books = [book1, book2, book3, book4, book5]
for book in books:
    print(book)

print("\n")

# Создание экземпляров учебников
textbook1 = Textbook(
    title="Алгебра",
    author="Иванов Иван",
    pages=200,
    isbn="4455667788",
    subject="Математика",
    grade=9,
    has_exercises=True,
)
textbook2 = Textbook(
    title="История",
    author="Петров Петр",
    pages=300,
    isbn="5566778899",
    subject="История",
    grade=10,
    has_exercises=False,
)
textbook3 = Textbook(
    title="География",
    author="Сидоров Сидор",
    pages=250,
    isbn="6677889900",
    subject="География",
    grade=8,
    has_exercises=True,
)
textbook4 = Textbook(
    title="Физика",
    author="Кузнецов Кузьма",
    pages=400,
    isbn="7788990011",
    subject="Физика",
    grade=11,
    has_exercises=True,
)
textbook5 = Textbook(
    title="Химия",
    author="Лебедев Леонид",
    pages=350,
    isbn="8899001122",
    subject="Химия",
    grade=10,
    has_exercises=False,
)

# Пометка одного учебника как зарезервированного
textbook5.reserved = True

# Печать деталей о учебниках
textbooks = [textbook1, textbook2, textbook3, textbook4, textbook5]
for textbook in textbooks:
    print(textbook)
