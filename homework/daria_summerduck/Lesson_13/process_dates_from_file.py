"""
Нужно прочитать файлик, который лежит в репозитории в моей папке.
Здесь: homework/eugene_okulik/hw_13/data.txt

Файлик не копируйте и никуда не переносите.
Напишите программу, которая читает этот файл, находит в нём даты
и делает с этими датами то, что после них написано.

Опирайтесь на то, что структура каждой строки одинакова:
сначала идет номер,
потом дата,
потом дефис
и после него текст.

У вас должен получиться код,
который находит даты и для даты под номером один
в коде должно быть реализовано то действие,
которое написано в файле после этой даты.

Ну и так далее для каждой даты.
"""

from datetime import datetime, timedelta


file_path = r"homework/eugene_okulik/hw_13/data.txt"


def process_dates_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file.readlines():
            number, date_task = line.split(". ", 1)
            date, action = date_task.split(" - ", 1)
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")

            print(f"\nСтрока {number} \n" f"{line}", end="")
            if "распечатать эту дату, но на неделю позже" in action:
                new_date = date + timedelta(weeks=1)
                print(f"Дата на неделю позже: {new_date}")
            elif "распечатать какой это будет день недели" in action:
                weekday = date.strftime("%A")
                print(f"День недели: {weekday}")
            elif "распечатать сколько дней назад была эта дата" in action:
                days_ago = (datetime.now() - date).days
                print(f"\nЭта дата была {days_ago} дней назад")


process_dates_from_file(file_path)
