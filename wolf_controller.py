import random


class WolfCreator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.pup_year = 0
        self.hunger = 0
        self.death_age = random.randint(120, 240)
        self.female = random.choice([True, False])

    def wolf_age(self):
        self.age += 1
        self.pup_year += 1
        self.hunger += 1

    def wolf_eat(self):
        self.hunger = 0
