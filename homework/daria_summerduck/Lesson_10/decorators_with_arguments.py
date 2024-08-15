def repeat_me(count):
    def decorator_repeat_me(func):
        def wrapper(*args):
            for i in range(count):
                func(*args)

        return wrapper

    return decorator_repeat_me


@repeat_me(count=2)
def example(text):
    print(text)


example("print me")
