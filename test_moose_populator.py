from moose_controller import MooseCreator
import random

def moose_main1():
    moose_num = 10
    max_x = 50
    max_y = 75
    moose_dict = {}
    moose_locs = []
    for i in range(moose_num):
        empty_space = False
        while empty_space == False:
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            moose_loc = (x, y)
            if moose_loc not in moose_locs:
                moose_locs.append(moose_loc)
                empty_space = True
        moose_dict[str(i)] = MooseCreator(x, y)

    print(moose_locs)

def moose_main2():
    moose_num = 10
    max_x = 50
    max_y = 75
    moose_list = []
    moose_locs = []
    for i in range(moose_num):
        empty_space = False
        while empty_space == False:
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            moose_loc = (x, y)
            if moose_loc not in moose_locs:
                moose_locs.append(moose_loc)
                empty_space = True
        moose_list.append(MooseCreator(x=x, y=y, max_x=max_x, max_y=max_y))
    for moose in moose_list:
        print(moose.x, moose.y)


moose_main2()