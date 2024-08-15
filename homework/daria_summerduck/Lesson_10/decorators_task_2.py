"""
Создайте универсальный декоратор,
который будет управлять тем, сколько раз запускается декорируемая функция

"""


def repeat_me(func):
    def wrapper(*args, **kwargs):
        count = kwargs.get("count", 1)
        for i in range(count):
            func(*args, **kwargs)

    return wrapper


@repeat_me
def example(text):
    print(text)


example("print me")
