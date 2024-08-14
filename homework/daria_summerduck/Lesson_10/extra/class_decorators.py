from decorators import timer

@timer
class TimeWaster:
    def __init__(self, max_num):
        self.max_num = max_num

    def waste_time(self, num_times):
        for _ in range(num_times):
            sum([i**2 for i in range(self.max_num)])

"""
>>> tw = TimeWaster(1000)
Finished TimeWaster() in 0.0000 secs

>>> tw.waste_time(999)
"""