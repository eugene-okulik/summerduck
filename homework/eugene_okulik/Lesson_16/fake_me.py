from faker import Faker

fake = Faker(locale='ru_RU')

for _ in range(5):
    print(fake.name())
    print(fake.address())
