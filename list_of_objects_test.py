import random


class PeopleLocs:
    def __init__(self, x, y):
        self.x = x
        self.y = y


people_list = []
for i in range(100):
    x = random.randint(0, 10)
    y = random.randint(0, 15)
    people_list.append(PeopleLocs(x, y))

print(len(people_list))
for person in people_list:
    if random.randint(0, 10) == 1:
        people_list.remove(person)

print(len(people_list))
