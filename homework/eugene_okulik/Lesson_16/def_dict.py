import collections

with open('shops.txt') as shops_file:
    shops = list(map(lambda x: x.replace('\n', ''), shops_file.readlines()))

city_shops = collections.defaultdict(list)
# city_shops = {}
for line in shops:
    shop, city = line.split(':')
    # if city not in city_shops:
    #     city_shops[city] = []
    city_shops[city].append(shop)

print(city_shops)

# {'Минск': ['маг1', 'молоко'], 'Москва': ['спорт'], 'Брест': ['хлеб','товары']}
