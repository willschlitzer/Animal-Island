from moose_controller import MooseCreator
from wolf_controller import WolfCreator
import random

def main():
    max_clockticks = 100
    max_x = 100
    max_y = 20
    moose_list, moose_locs = moose_populator(max_x = max_x, max_y=max_y)
    wolf_list, wolf_locs = wolf_populator(max_x= max_x, max_y= max_y, moose_locs=moose_locs)
    run_island(max_x=max_x, max_y=max_y,
               moose_list=moose_list, moose_locs=moose_locs,
               wolf_list=wolf_list, wolf_locs=wolf_locs,
               max_clockticks=max_clockticks)


def moose_populator(max_x, max_y):
    initial_moose_number = 50
    moose_list = []
    moose_locs = []
    for i in range(initial_moose_number):
        empty_space = False
        while empty_space == False:
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            moose_loc = (x, y)
            if moose_loc not in moose_locs:
                moose_locs.append(moose_loc)
                empty_space = True
        moose_list.append(MooseCreator(x=x, y=y))
    return moose_list, moose_locs

def wolf_populator(max_x, max_y, moose_locs):
    initial_wolf_number = 10
    wolf_list = []
    wolf_locs = []
    for i in range(initial_wolf_number):
        empty_space = False
        while empty_space == False:
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
    print('Clockticks: ' + str(clocktick))
    print('Wolf Population: ' + str(len(wolf_list)))
    print('Moose Population: ' + str(len(moose_list)))
    draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
    while clocktick < max_clockticks:
        clocktick += 1
        moose_list, moose_locs, wolf_list, wolf_locs = single_clocktick(max_x=max_x, max_y=max_y,
                                                                        moose_list=moose_list,
                                                                        wolf_list=wolf_list,)
        if clocktick % 10 == 0 and max_clockticks > clocktick:
            print('Clockticks: ' + str(clocktick))
            print('Wolf Population: ' + str(len(wolf_list)))
            print('Moose Population: ' + str(len(moose_list)))
            #draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)

    print('Final Population After ' + str(max_clockticks) + ' Clockticks')
    draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)

def single_clocktick(max_x, max_y, moose_list, wolf_list):
    moose_list, wolf_list = wolf_mover(max_x=max_x, max_y=max_y, moose_list=moose_list, wolf_list=wolf_list)

    wolf_locs = location_list(wolf_list)
    moose_locs = location_list(moose_locs)
    return moose_list, moose_locs, wolf_list, wolf_locs

def location_list(object_list):
    loc_list = []
    for object in object_list:
        loc = (object.x, object.y)
        loc_list.append(loc)
    return loc_list

def wolf_mover(max_x, max_y, moose_list, wolf_list):
    wolf_locs = []
    for wolf in wolf_list:
        wolf_loc = (wolf.x, wolf.y)
        wolf_locs.append(wolf_loc)
    moose_locs = []
    for moose in moose_list:
        moose_loc = (moose.x, moose.y)
        moose_locs.append(moose_loc)
    for wolf in wolf_list:
        wolf_loc = (wolf.x, wolf.y)
        wolf_locs.remove(wolf_loc)
        adjacent_moose = check_adjacency(wolf_loc, moose_locs)
        if len(adjacent_moose) > 0:
            feeding_location = get_feeding_location(adjacent_moose=adjacent_moose)
            for moose in moose_list:
                moose_loc = (moose.x, moose.y)
                if moose_loc == feeding_location:
                    wolf.x = moose.x
                    wolf.y = moose.y
                    moose_list.remove(moose)
                    moose_locs.remove(moose_loc)
        else:
            nearby_wolves = check_adjacency(wolf_loc, wolf_locs)
            moved = False
            while moved == False:
                x = wolf_loc[0]
                y = wolf_loc[1]
                x += random.randint(-1,2)
                y += random.randint(-1, 2)
                new_loc = (x,y)
                if (new_loc not in nearby_wolves) and (max_x >= x >= 0) and (max_y >= y >= 0):
                    wolf_locs.append(new_loc)
                    wolf.x = x
                    wolf.y = y
                    moved = True
    return moose_list, wolf_list

def get_feeding_location(adjacent_moose):
    if len(adjacent_moose) == 1:
        return adjacent_moose[0]
    else:
        moose_pick = random.randint(0, len(adjacent_moose)-1)
        return adjacent_moose[moose_pick]

def check_adjacency(loc, loc_list):
    x_loc = loc[0]
    y_loc = loc[1]
    adjacent_locs = []
    for dx in range(-1, 2):
        for dy in range(-1,2):
            test_loc = (x_loc+dx, y_loc + dy)
            if test_loc in loc_list:
                adjacent_locs.append(test_loc)
    return adjacent_locs

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