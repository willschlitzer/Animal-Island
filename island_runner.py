import random
import numpy as np
from island_instance import IslandCreator
from wildlife_instance import WildlifeCreator

def main():
    max_clockticks = 1000
    max_x = 100
    max_y = 100
    lake_num = 5
    moose_num = 100
    wolf_num = 25
    squirrel_num = 3000
    island = IslandCreator(
        max_x = max_x,
        max_y = max_y,
        lake_num= lake_num,
        moose_num= moose_num,
        wolf_num = wolf_num,
        squirrel_num = squirrel_num
    )
    run_island(island=island, max_clockticks=max_clockticks)


def run_island(island, max_clockticks):
    island.run_data.append(island.tick_data)
    while island.clocktick <= max_clockticks:
        island.clocktick += 1
        island.empty_tick_data()
        single_clocktick(island=island)
        island.tick_data_generator()
        island.run_data.append(island.tick_data)
    #print(island.run_data)

def single_clocktick(island):
    wolf_mover(island=island)

def wolf_mover(island):
    for wolf in island.wolf_list:
        x = wolf.x
        y = wolf.y
        old_loc = (x,y)
        if (wolf.age > wolf.death_age) or (wolf.hunger > wolf.starve):
            island.location_dict[(x,y)]['occupied'] = False
            island.location_dict[(x, y)]['wolf'] = False
            island.location_dict[(x, y)]['occupying_animal'] = None
            if wolf.age > wolf.death_age:
                wolf.old_age += 1
            else:
                wolf.starve += 1
            island.wolf_list.remove(wolf)
            continue
        wolf.age += 1
        wolf.baby_age += 1
        wolf.hunger += 1
        moose_locs = check_adjacency(island=island, x = x, y=y, moose_hunting=True)
        if len(moose_locs) > 0:
            hunting_loc = random.choice(moose_locs)
            moose_meal = island.location_dict[hunting_loc]['occupying_animal']
            island.moose_list.remove(moose_meal)
            island.moose_eaten += 1
            wolf.hunger = 0
            island.location_dict[old_loc]['occupying_animal'] = None
            island.location_dict[old_loc]['wolf'] = False
            island.location_dict[hunting_loc]['occupying_animal'] = wolf
            island.location_dict[hunting_loc]['moose'] = False
            island.location_dict[hunting_loc]['wolf'] = True
            wolf.x, wolf.y = hunting_loc[0], hunting_loc[1]

        else:
            empty_locs = check_adjacency(island=island, x=x, y=y)
            if empty_locs == []:
                continue
            else:
                new_loc = random.choice(empty_locs)
                island.location_dict[old_loc]['occupying_animal'] = None
                island.location_dict[old_loc]['wolf'] = False
                island.location_dict[new_loc]['occupying_animal'] = wolf
                island.location_dict[new_loc]['wolf'] = True
                wolf.x, wolf.y = new_loc[0], new_loc[1]


def check_adjacency(island, x, y, moose_hunting=False, squirrel=False):
    adjacent_squares = []
    for a in range(x-1, x+2):
        for b in range(y-1, y+2):
            if (0 <= a < island.max_x) & (0 <= b < island.max_y):
                adjacent_squares.append((a,b))
    if moose_hunting == True:
        moose_locs = []
        for square in adjacent_squares:
            if (island.location_dict[square]['occupied'] == True) & (island.location_dict[square]['moose'] == True):
                moose_locs.append(square)
        return moose_locs
    else:
        empty_locs = []
        for square in adjacent_squares:
            if (island.location_dict[square]['occupied'] == False) & (island.location_dict[square]['water'] == False):
                empty_locs.append(square)
        return empty_locs


if __name__ == '__main__':
    main()