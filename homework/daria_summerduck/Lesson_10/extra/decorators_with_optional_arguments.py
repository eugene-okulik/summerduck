def repeat_me(_func=None, *, count=2):
    def decorator_repeat_me(func):
        def wrapper(*args):
            for _ in range(count):
                func(*args)

        return wrapper

    if _func is None:
        return decorator_repeat_me
    else:
        return decorator_repeat_me(_func)


@repeat_me
def say_whee():
    print("Whee!")


@repeat_me(count=5)
def greet():
    print("Hello")


say_whee()
greet()
