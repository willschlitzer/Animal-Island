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
            self.death_age = abs(int(np.random.normal(180, 25)))
        elif type == 'moose':
            self.type= 'moose'
            self.death_age = abs(int(np.random.normal(250, 30)))
        elif type == 'squirrel':
            self.type = 'squirrel'
            self.death_age = abs(int(np.random.normal(30, 6)))