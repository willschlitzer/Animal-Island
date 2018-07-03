class Animals:
    def __init__(self, wolf, moose):
        self.wolf = wolf
        self.moose = moose


my_animals = Animals(wolf=10, moose=50)


def moose_adder(animals):
    animals.moose += 3


def wolf_adder(animals):
    animals.wolf += 5


for i in range(10):
    moose_adder(animals=my_animals)
    wolf_adder(animals=my_animals)
    print(my_animals.moose)
    print(my_animals.wolf)
