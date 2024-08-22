"""
Создать классы цветов: общий класс для всех цветов и классы для нескольких видов.

Создать экземпляры (объекты) цветов разных видов.

Собрать букет (букет - еще один класс) с определением его стоимости.

В букете цветы пусть хранятся в списке. Это будет список объектов.

Для букета создать метод, который определяет время его увядания по среднему времени жизни всех цветов в букете.

Позволить сортировку цветов в букете на основе различных параметров
(свежесть/цвет/длина стебля/стоимость)(это тоже методы)

Реализовать поиск цветов в букете по каким-нибудь параметрам
(например, по среднему времени жизни) (и это тоже метод).
"""


class Flower:
    def __init__(self, name, color, stem_length, freshness, cost, lifespan):
        self.name = name
        self.color = color
        self.stem_length = stem_length
        self.freshness = freshness  # 0 to 100
        self.cost = cost
        self.lifespan = int(int(self.freshness) * 0.01 * lifespan)

    def __repr__(self):
        return (
            f"\n{self.name}(Color: {self.color}, Stem Length: {self.stem_length}cm, "
            f"Freshness: {self.freshness}%, Cost: {self.cost}$, Lifespan: {self.lifespan} days)"
        )


class Rose(Flower):
    def __init__(self, color, stem_length, freshness, cost, lifespan=7):
        super().__init__("Rose", color, stem_length, freshness, cost, lifespan)


class Tulip(Flower):
    def __init__(self, color, stem_length, freshness, cost, lifespan=5):
        super().__init__("Tulip", color, stem_length, freshness, cost, lifespan)


class Lily(Flower):
    def __init__(self, color, stem_length, freshness, cost, lifespan=10):
        super().__init__("Lily", color, stem_length, freshness, cost, lifespan)


class Bouquet:
    def __init__(self, name):
        self.flowers = []
        self.name = name

    def add_flower(self, flower):
        self.flowers.append(flower)

    def total_cost(self):
        return sum(flower.cost for flower in self.flowers)

    def average_lifespan(self):
        if not self.flowers:
            return 0
        return int(sum(flower.lifespan for flower in self.flowers) / len(self.flowers))

    def sort_by(self, attribute):
        self.flowers.sort(key=lambda flower: getattr(flower, attribute))

    def find_flowers_by(self, **kwargs):
        found_flowers = []
        for flower in self.flowers:
            match = True
            for key, value in kwargs.items():
                if getattr(flower, key) != value:
                    match = False
                    break
            if match:
                found_flowers.append(flower)
        return found_flowers

    def __repr__(self):
        return f"\nBouquet name: {self.name} \nBouquet contains: {self.flowers}"


# Create flowers
rose_red = Rose(color="Red", stem_length=10, cost=5.99, freshness=90)
rose_white = Rose(color="White", stem_length=10, cost=9.99, freshness=94)
lily_white = Lily(color="White", stem_length=12, cost=3.99, freshness=98)
tulip_yellow = Tulip(color="Yellow", stem_length=8, cost=2.49, freshness=95)
tulip_orange = Tulip(color="Orange", stem_length=8, cost=3.49, freshness=93)
tulip_red = Tulip(color="Red", stem_length=8, cost=3.49, freshness=80)

# Create bouquets
bouquet_first = Bouquet("First")
bouquet_first.add_flower(rose_red)
bouquet_first.add_flower(rose_white)
bouquet_first.add_flower(rose_red)

# Print bouquet cost and lifespan
print(bouquet_first)
print(f"Total cost of bouquet: {bouquet_first.total_cost()}$ \n")
print(f"Average lifespan of bouquet: {bouquet_first.average_lifespan()} days \n")

# Sort flowers in bouquet by cost
bouquet_first.sort_by("cost")
print(f"Bouquet after sorting by cost: {bouquet_first} \n")

# Find flowers in  bouquet by collor
found_flowers = bouquet_first.find_flowers_by(color="Red")
print(f"Found flowers by color: {found_flowers} \n")

# Find flowers in  bouquet by collor and stem length
found_flowers = bouquet_first.find_flowers_by(color="White", stem_length=10)
print(f"Found flowers by colors and stem length: {found_flowers} \n")
