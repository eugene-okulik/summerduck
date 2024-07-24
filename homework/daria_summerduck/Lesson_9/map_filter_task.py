"""
Map, filter
Есть такой список:

temperatures = [20, 15, 32, 34, 21, 19, 25, 27, 30, 32, 34, 30, 29, 25, 27, 22, 22, 23, 25, 29, 29,
31, 33, 31, 30, 32, 30, 28, 24, 23]
С помощью функции map или filter создайте из этого списка новый список с жаркими днями.
Будем считать жарким всё, что выше 28.

Распечатайте из нового списка самую высокую температуру самую низкую и среднюю.
"""


def convert_to_fahrenheit(celsius: int):
    return int(celsius * 9 / 5 + 32)


def count_average_temperature(temperatures: list):
    return sum(temperatures) / len(temperatures)


raw_temperatures = [
    20,
    15,
    32,
    34,
    21,
    19,
    25,
    27,
    30,
    32,
    34,
    30,
    29,
    25,
    27,
    22,
    22,
    23,
    25,
    29,
    29,
    31,
    33,
    31,
    30,
    32,
    30,
    28,
    24,
    23,
]

# v1 filter
hot_days = list(filter(lambda x: x > 28, raw_temperatures))

# v2 filter + map
hot_days_from_map_and_filter = list(
    map(lambda x: x if x > 28 else None, raw_temperatures)
)
hot_days_from_map_and_filter = list(filter(lambda x: x, hot_days_from_map_and_filter))

# compare to make sure the results are the same
assert hot_days == hot_days_from_map_and_filter

# map
hot_days_fahrenheit = list(map(convert_to_fahrenheit, hot_days))

# calculate average temperature
average_temperature = count_average_temperature(hot_days)
average_temperature_fahrenheit = count_average_temperature(hot_days_fahrenheit)

# print results
print(f"Температуры: {raw_temperatures}")
print(f"Температуры жарких дней: {hot_days}")
print(f"Температуры жарких дней в Фаренгейтах: {hot_days_fahrenheit}")
print(f"Самая высокая температура: {max(hot_days)} °C / {max(hot_days_fahrenheit)} °F")
print(f"Самая низкая температура: {min(hot_days)} °C / {min(hot_days_fahrenheit)} °F")
print(
    f"Средняя температура: {average_temperature:.1f} °C / {average_temperature_fahrenheit:.1f} °F"
)
