from decorators import CountCalls


@CountCalls
def say_whee():
    print("Whee!")


say_whee()
say_whee()

say_whee.num_calls
