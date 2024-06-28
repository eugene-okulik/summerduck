"""
Даны два числа. Найти среднее арифметическое и среднее геометрическое этих чисел
"""


def average_arithmetic(a, b):
    return (a + b) / 2


def average_geometric(a, b):
    return (a * b) ** 0.5


assert average_arithmetic(3, 5) == 4
assert average_geometric(5, 5) == 5
