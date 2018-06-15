class WolfCreator():

    def __init__(self, x, y, max_x, max_y):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.age = 0
        self.pup_year = 0
        self.hunger = 0

    def wolf_age(self):
        self.age += 1
        self.pup_year += 1
        self.hunger += 1

    def wolf_eat(self):
        self.hunger = 0