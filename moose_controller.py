import random

class MooseCreator:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.calf_year = 0
        self.death_age = random.randint(180, 300)

    def moose_age(self):
        self.age +=1
        self.calf_year += 1