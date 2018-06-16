from moose_controller import MooseCreator
from wolf_controller import WolfCreator
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random


def main():
    max_clockticks = 100
    max_x = 30
    max_y = 30
    moose_list, moose_locs = moose_populator(max_x = max_x, max_y=max_y)
    wolf_list, wolf_locs = wolf_populator(max_x= max_x, max_y= max_y, moose_locs=moose_locs)
    run_island(max_x=max_x, max_y=max_y,
               moose_list=moose_list, moose_locs=moose_locs,
               wolf_list=wolf_list, wolf_locs=wolf_locs,
               max_clockticks=max_clockticks)

def moose_populator(max_x, max_y):
    initial_moose_number = 100
    moose_list = []
    moose_locs = []
    for i in range(initial_moose_number):
        empty_space = False
        while not empty_space:
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            moose_loc = (x, y)
            if moose_loc not in moose_locs:
                moose_locs.append(moose_loc)
                empty_space = True
        moose_list.append(MooseCreator(x=x, y=y))
    return moose_list, moose_locs

def wolf_populator(max_x, max_y, moose_locs):
    initial_wolf_number = 15
    wolf_list = []
    wolf_locs = []
    for i in range(initial_wolf_number):
        empty_space = False
        while not empty_space:
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            wolf_loc = (x, y)
            if wolf_loc not in moose_locs and wolf_loc not in wolf_locs:
                wolf_locs.append(wolf_loc)
                empty_space = True
        wolf_list.append(WolfCreator(x=x, y=y))
    return wolf_list, wolf_locs

def run_island(max_x, max_y, moose_list, moose_locs, wolf_list, wolf_locs, max_clockticks):
    clocktick = 0
    data_list = []
    print('Clockticks: ' + str(clocktick))
    print('Wolf Population: ' + str(len(wolf_list)))
    print('Moose Population: ' + str(len(moose_list)))
    #draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
    data_list.append([clocktick, len(wolf_list), len(moose_list)])
    while clocktick < max_clockticks:
        clocktick += 1
        moose_list, moose_locs, wolf_list, wolf_locs = single_clocktick(max_x=max_x, max_y=max_y,
                                                                        moose_list=moose_list,
                                                                        wolf_list=wolf_list,)
        data_list.append([clocktick, len(wolf_list), len(moose_list)])
        if clocktick % 1 == 0 and max_clockticks > clocktick:
            print('Clockticks: ' + str(clocktick))
            print('Wolf Population: ' + str(len(wolf_list)))
            print('Moose Population: ' + str(len(moose_list)))
            #draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)

    print('Final Population After ' + str(max_clockticks) + ' Clockticks')
    print('Wolf Population: ' + str(len(wolf_list)))
    print('Moose Population: ' + str(len(moose_list)))
    #draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
    #print(data_list)
    data_array = np.array(data_list)
    print(data_array)
    wolf_moose_df = pd.DataFrame(data_array, columns=['clockticks', 'wolves', 'moose'])
    wolf_moose_file = 'run_data/wolf_moose.csv'
    wolf_moose_fig = 'run_data/wolf_moose_chart.png'
    wolf_moose_df.to_csv(wolf_moose_file, sep=',')
    print(wolf_moose_df.head())
    column_list = ['wolves', 'moose']
    wolf_moose_df[column_list].plot()
    plt.xlabel('Clock tick')
    plt.savefig(wolf_moose_fig)
    plt.show()


def single_clocktick(max_x, max_y, moose_list, wolf_list):
    moose_list, wolf_list = wolf_mover(max_x=max_x, max_y=max_y, moose_list=moose_list, wolf_list=wolf_list)
    moose_list = moose_mover(max_x=max_x, max_y=max_y, moose_list=moose_list, wolf_list=wolf_list)

    wolf_locs = location_list(wolf_list)
    moose_locs = location_list(moose_list)
    return moose_list, moose_locs, wolf_list, wolf_locs

def location_list(animal_list):
    """This should be fixed to list unavailable and available spots"""
    loc_list = []
    for animal in animal_list:
        loc = (animal.x, animal.y)
        loc_list.append(loc)
    return loc_list

def wolf_mover(max_x, max_y, moose_list, wolf_list):
    birth_age = 8
    for wolf in wolf_list:
        wolf.age += 1
        wolf.pup_year += 1
        wolf_locs = location_list(wolf_list)
        moose_locs = location_list(moose_list)
        wolf_loc = (wolf.x, wolf.y)
        wolf_locs.remove((wolf.x, wolf.y))
        adjacent_moose, empty_locs = check_adjacency(wolf_loc, moose_locs)
        if len(adjacent_moose) > 0:
            feeding_location = location_selector(loc_list=adjacent_moose)
            for moose in moose_list:
                moose_loc = (moose.x, moose.y)
                if moose_loc == feeding_location:
                    wolf.hunger = 0
                    wolf.x = moose.x
                    wolf.y = moose.y
                    moose_list.remove(moose)
                    moose_locs.remove(moose_loc)
        else:
            wolf.hunger += 1
            nearby_wolves, empty_locs = check_adjacency(wolf_loc, wolf_locs)
            moved = False
            while not moved:
                x = wolf.x
                y = wolf.y
                x += random.randint(-1,1)
                y += random.randint(-1, 1)
                new_loc = (x,y)
                if (new_loc not in nearby_wolves) and (max_x > x >= 0) and (max_y > y >= 0):
                    wolf_locs.append(new_loc)
                    wolf.x = x
                    wolf.y = y
                    moved = True
                elif (new_loc == (wolf.x, wolf.y)) and (max_x > x >= 0) and (max_y > y >= 0):
                    wolf_locs.append(new_loc)
                    wolf.x = x
                    wolf.y = y
                    moved = True
        if wolf.age > wolf.death_age:
            wolf_list.remove(wolf)
        if wolf.hunger >= 7:
            wolf_list.remove(wolf)
        if wolf.pup_year >= random.randint(birth_age-3, birth_age+3):
            wolf.pup_year = 0
            animal_locs = wolf_locs + moose_locs
            birthed = False
            while not birthed:
                x = wolf.x
                y = wolf.y
                mom_loc = (x,y)
                nearby_animals = check_adjacency(mom_loc, animal_locs)
                x += random.randint(-1,1)
                y += random.randint(-1, 1)
                pup_loc = (x,y)
                if (pup_loc not in nearby_animals) and (max_x > x >= 0) and (max_y > y >= 0) and (pup_loc != mom_loc):
                    wolf_locs.append(pup_loc)
                    wolf_list.append(WolfCreator(x, y))
                    birthed = True
                else:
                    birthed = True
    return moose_list, wolf_list

def moose_mover(max_x, max_y, moose_list, wolf_list):
    birth_age = 25
    for moose in moose_list:
        moose.age += 1
        moose.calf_year += 1
        wolf_locs = location_list(wolf_list)
        moose_locs = location_list(moose_list)
        animal_locs = moose_locs + wolf_locs
        moved = False
        while not moved:
            x = moose.x
            y = moose.y
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)
            new_loc = (x, y)
            nearby_animals = check_adjacency(new_loc, animal_locs)
            if (new_loc not in nearby_animals) and (max_x > x >= 0) and (max_y > y >= 0):
                moose_locs.append(new_loc)
                moose.x = x
                moose.y = y
                moved = True
            elif (new_loc == (moose.x, moose.y)) and (max_x > x >= 0) and (max_y > y >= 0):
                moose_locs.append(new_loc)
                moose.x = x
                moose.y = y
                moved = True
        if moose.age > moose.death_age:
            moose_list.remove(moose)
        if moose.calf_year >= random.randint(birth_age-10, birth_age+5):
            moose.calf_year = 0
            animal_locs = wolf_locs + moose_locs
            birthed = False
            while not birthed:
                x = moose.x
                y = moose.y
                mom_loc = (x,y)
                nearby_animals = check_adjacency(mom_loc, animal_locs)
                x += random.randint(-1,1)
                y += random.randint(-1, 1)
                calf_loc = (x,y)
                if (calf_loc not in nearby_animals) and (max_x > x >= 0) and (max_y > y >= 0) and (calf_loc != mom_loc):
                    moose_locs.append(calf_loc)
                    moose_list.append(MooseCreator(x, y))
                    birthed = True
                else:
                    birthed = True
    return moose_list



def location_selector(loc_list):
    if len(loc_list) == 1:
        return loc_list[0]
    else:
        moose_pick = random.randint(0, len(loc_list) - 1)
        return loc_list[moose_pick]

def check_adjacency(loc, loc_list):
    x_loc = loc[0]
    y_loc = loc[1]
    adjacent_locs = []
    empty_locs = []
    for dx in range(-1, 2):
        for dy in range(-1,2):
            test_loc = (x_loc+dx, y_loc + dy)
            if test_loc in loc_list:
                adjacent_locs.append(test_loc)
            else:
                empty_locs.append(test_loc)
    return adjacent_locs, empty_locs

def draw_island(max_x, max_y, moose_locs, wolf_locs):
    for row in range(max_y):
        column_string = ''
        for column in range(max_x):
            location = (column, row)
            if location in moose_locs:
                column_string += 'M'
            elif location in wolf_locs:
                column_string += 'W'
            else:
                column_string += '-'
        print(column_string)

if __name__ == '__main__':
    main()