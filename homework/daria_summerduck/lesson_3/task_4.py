"""
Даны катеты прямоугольного треугольника. Найти его гипотенузу и площадь
"""


def hypotenuse(a, b):
    assert a > 0 and b > 0, "Катеты должны быть положительными числами"
    return (a**2 + b**2) ** 0.5


def area(a, b):
    assert a > 0 and b > 0, "Катеты должны быть положительными числами"
    return 0.5 * a * b


assert hypotenuse(3, 4) == 5
assert area(3, 4) == 6
try:
    hypotenuse(-3, 4)
except AssertionError:
    pass
