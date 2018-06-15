from moose_controller import MooseCreator
from wolf_controller import WolfCreator
import random

def main():
    max_clockticks = 30
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
        moose_list.append(MooseCreator(x=x, y=y, max_x=max_x, max_y=max_y))
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
        wolf_list.append(WolfCreator(x=x, y=y, max_x=max_x, max_y=max_y))
    return wolf_list, wolf_locs

def run_island(max_x, max_y, moose_list, moose_locs, wolf_list, wolf_locs, max_clockticks):
    clocktick = 0
    while clocktick < max_clockticks:

        if clocktick % 10 == 0 and max_clockticks > clocktick > 0:
            print('Clockticks: ' + str(clocktick))
            draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
        clocktick += 1
    print('Final Population After ' + str(max_clockticks) + ' Clockticks')
    draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)

def single_clocktick(moose_list, moose_locs, wolf_list, wolf_locs):
    return

def wolf_mover(moose_list, moose_locs, wolf_list, wolf_locs):
    for wolf in wolf_list:
        wolf_loc = (wolf.x, wolf.y)
        wolf_locs.remove(wolf_loc)

def check_adjacency

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