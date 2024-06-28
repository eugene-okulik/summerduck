"""
Даны 2 числа a и b. Получить их сумму, разность и произведение
"""


def summ(a, b):
    return a + b


def difference(a, b):
    return a - b


def product(a, b):
    return a * b


sum = summ(3, 5)
diff = difference(3, 5)
prod = product(3, 5)

assert sum == 8
assert diff == -2
assert prod == 15
