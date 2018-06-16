import random

class SquirrelCreator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.baby_age = 0
        self.death_age = random.randint(18,30)