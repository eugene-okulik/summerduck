"""
Напишите программу:
Есть функция которая делает одну из арифметических операций
с переданными ей числами (числа и операция передаются в аргументы функции).

Функция выглядит примерно так:

def calc(first, second, operation):
    if operation == '+':
        return first + second
    elif .....

Программа спрашивает у пользователя 2 числа (вне функции)

Создайте декоратор, который декорирует функцию calc и управляет тем какая операция будет произведена:

если числа равны, то функция calc вызывается с операцией сложения этих чисел
если первое больше второго, то происходит вычитание второго из певрого
если второе больше первого - деление первого на второе
если одно из чисел отрицательное - умножение
"""


def decorator(func):

    def wrapper(first, second):
        if first == second:
            operation = "+"
        elif first < 0 or second < 0:
            operation = "*"
        elif first > second:
            operation = "-"
        elif first < second:
            operation = "/"
        else:
            operation = None

        return func(first, second, operation)

    return wrapper


@decorator
def calc(first, second, operation=None):
    if operation == "+":
        result = first + second
    if operation == "-":
        result = first - second
    if operation == "/":
        result = first / second
    if operation == "*":
        result = first * second
    if operation is None:
        raise ValueError("No operation specified")

    return result


first = float(input("Input first number: "))
second = float(input("Input second number: "))
print(calc(first, second))
