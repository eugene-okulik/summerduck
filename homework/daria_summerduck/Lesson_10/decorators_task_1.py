"""
Создайте универсальный декоратор, который можно будет применить к любой функции.
Декоратор должен делать следующее:
он должен распечатывать слово "finished" после выполнения декорированной функции.

"""


def finish_me(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print("finished")

    return wrapper


@finish_me
def example(text):
    print(text)


example("print me")
