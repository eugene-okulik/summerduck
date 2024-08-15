PRICE_LIST = """тетрадь 50р
книга 200р
ручка 100р
карандаш 70р
альбом 120р
пенал 300р
рюкзак 500р"""

a = {
    "тетрадь": 50,
    "книга": 200,
    "ручка": 100,
    "карандаш": 70,
    "альбом": 120,
    "пенал": 300,
    "рюкзак": 500,
}

# v1
price_dict = {}
items = PRICE_LIST.splitlines()
for item in items:
    item_name_and_price = item.split()
    item_name = item_name_and_price[0]
    item_price = item_name_and_price[1][:-1]
    price_dict[item_name] = int(item_price)

assert a == price_dict

# v2
for item in PRICE_LIST.splitlines():
    price_dict[item.split()[0]] = int(item.split()[1][:-1])

assert a == price_dict

# v3
price_dict = {
    item.split()[0]: int(item.split()[1][:-1]) for item in PRICE_LIST.splitlines()
}

assert a == price_dict
