import numpy as np
import random


class WildlifeCreator:
    def __init__(self, type, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.hunger = 0
        self.baby_age = 0
        self.female = random.choice([True, False])
        if type == "wolf":
            self.type = "wolf"
            self.birth_age = abs(int(np.random.normal(15, 2)))
            self.death_age = abs(int(np.random.normal(180, 25)))
            self.starve = 18
        elif type == "moose":
            self.type = "moose"
            self.birth_age = abs(int(np.random.normal(20, 1)))
            self.death_age = abs(int(np.random.normal(250, 30)))
            self.starve = 30
        elif type == "squirrel":
            self.type = "squirrel"
            self.birth_age = abs(int(np.random.normal(9, 2)))
            self.death_age = abs(int(np.random.normal(25, 3)))
            self.starve = 3

class LocustAttack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = abs(int(np.random.normal(6, 2)))
        self.fed = 0
        self.age = 0
        self.death_age = random.randint(0,6)
        self.population = abs(int(np.random.normal(250, 50)))