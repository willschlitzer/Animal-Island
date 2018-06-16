import random

rando_list = []
for i in range(1000):
    rando_list.append(random.randint(-1, 1))

print('-1: ' + str(rando_list.count(-1)))
print('0: ' + str(rando_list.count(0)))
print('1: ' + str(rando_list.count(1)))