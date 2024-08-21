import json


class CountryData:
    def __init__(self, filename):
        self.__filename = filename
        self.__data = self.__read_file()
        self.__country = self.__data['Country']
        self.__avg_temp = self.__data['avg_temp']
        self._comfort = self.__is_comfort()

    @property
    def data(self):
        return self.__data

    @property
    def country(self):
        return self.__country

    @property
    def avg_temp(self):
        return self.__avg_temp

    @property
    def comfort(self):
        return self._comfort

    @comfort.setter
    def comfort(self, value):
        self._comfort = value

    def __read_file(self):
        file_data = open(self.__filename, 'r')
        data = json.load(file_data)
        file_data.close()
        return data

    def __is_comfort(self):
        return self.__avg_temp > 25


data1 = CountryData('data1.txt')
data1.comfort = False
print(data1.comfort)
# data1.data = 'skdfjhskdjf'
print(data1.data)
# data1.__data = {'1': 5}
print(data1.data)
print(data1.country)
# print(data1.avg_temp)
data2 = CountryData('data2.txt')
print(data2.country)
data1.__avg_temp = 2342342
print(data1.avg_temp)
