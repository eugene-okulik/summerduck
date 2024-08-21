import unittest
from i_can_buy_myself_flowers import *


class TestFlower(unittest.TestCase):
    def test_flower_creation(self):
        flower = Flower("Rose", "Red", 10, 90, 5.99, 7)
        self.assertEqual(flower.name, "Rose")
        self.assertEqual(flower.color, "Red")
        self.assertEqual(flower.stem_length, 10)
        self.assertEqual(flower.freshness, 90)
        self.assertEqual(flower.cost, 5.99)
        self.assertEqual(flower.lifespan, 6)  # 90% of 7


class TestBouquet(unittest.TestCase):
    def setUp(self):
        self.bouquet = Bouquet("First")
        self.rose_red = Rose(color="Red", stem_length=10, cost=5.99, freshness=90)
        self.rose_white = Rose(color="White", stem_length=10, cost=9.99, freshness=94)
        self.lily_white = Lily(color="White", stem_length=20, cost=4.99, freshness=95)
        self.bouquet.add_flower(self.rose_red)
        self.bouquet.add_flower(self.rose_white)
        self.bouquet.add_flower(self.lily_white)

    def test_add_flower(self):
        self.bouquet.add_flower(self.rose_red)
        self.assertEqual(len(self.bouquet.flowers), 4)
        self.assertEqual(self.bouquet.flowers[3], self.rose_red)

    def test_total_cost(self):
        self.assertEqual(self.bouquet.total_cost(), 20.97)

    def test_average_lifespan(self):
        self.assertEqual(self.bouquet.average_lifespan(), 7)

    def test_sort_by(self):
        self.bouquet.sort_by("cost")
        self.assertEqual(
            self.bouquet.flowers, [self.lily_white, self.rose_red, self.rose_white]
        )

    def test_find_flowers_by(self):
        found_flowers = self.bouquet.find_flowers_by(color="Red")
        self.assertEqual(found_flowers, [self.rose_red])

        found_flowers = self.bouquet.find_flowers_by(color="White", stem_length=10)
        self.assertEqual(found_flowers, [self.rose_white])


if __name__ == "__main__":
    unittest.main()
