"""
Даны числа x и y. Получить x − y / 1 + xy
"""


def get_result(x, y):
    return x - y / 1 + x * y

assert get_result(5, 3) == 17
