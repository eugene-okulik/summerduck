def calc(x, y):
    try:
        return int(x) / int(y)
    except (ZeroDivisionError, ValueError) as err:
        print(x, y)
        raise err
        # print(err)
        # print('Ошибка ввода данных')
    # except ZeroDivisionError:
    #     print('а ноль делить нельзя')
    # except ValueError:
    #     print('Нужно было ввести числа')


print(calc(input('number'), input('number')))
print('hello!')
