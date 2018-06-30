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
        if type == 'wolf':
            self.type = 'wolf'
            self.birth_age = 15
            self.death_age = abs(int(np.random.normal(180, 25)))
            self.starve = 6
        elif type == 'moose':
            self.type= 'moose'
            self.birth_age = 20
            self.death_age = abs(int(np.random.normal(250, 30)))
            self.starve = 12
        elif type == 'squirrel':
            self.type = 'squirrel'
            self.death_age = abs(int(np.random.normal(30, 6)))
            self.starve = 3
