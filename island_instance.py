import random
import numpy as np
from wildlife_instance import WildlifeCreator

class IslandCreator:

    def __init__(self, max_x, max_y, lake_num, moose_num, wolf_num, squirrel_num):
        self.max_x = max_x
        self.max_y = max_y
        self.lake_num = lake_num
        self.moose_num = moose_num
        self.wolf_num = wolf_num
        self.squirrel_num = squirrel_num
        self.location_dict_creator()
        self.lake_builder()
        self.animal_generator()

    def location_dict_creator(self):
        location_dict = {}
        for x in range(0, self.max_x):
            for y in range(0, self.max_y):
                if random.randint(0, 100) < 85:
                    veg = True
                    growth = random.randint(10, 45)
                else:
                    veg = False
                    growth = random.randint(1, 9)
                location_dict[(x, y)] = {
                    'water':False,
                    'veg':veg,
                    'growth':growth,
                    'occupied':False,
                    'occupying_animal': None,
                    'moose':False,
                    'wolf':False,
                    'squirrel_count':0,
                    'occupying_squirrels':[]
                }
        self.location_dict = location_dict

    def lake_builder(self):
        water_locs = []
        for i in range(self.lake_num):
            lake_center_x = random.randint(0, self.max_x-1)
            lake_center_y = random.randint(0, self.max_y-1)
            size = abs(int(np.random.normal(3, .75)))
            for x in range(lake_center_x-size, lake_center_x+size):
                for y in range(lake_center_y-size, lake_center_y+size):
                    if (0 <= x < self.max_x) & (0 <= y < self.max_y):
                        water_locs.append((x,y))
        for loc in water_locs:
            self.location_dict[loc]['water'] = True
            self.location_dict[loc]['veg'] = False
            self.location_dict[loc]['growth'] = False


    def animal_generator(self):
        self.moose_list = []
        self.wolf_list = []
        for i in range(self.moose_num):
            loc_searching = True
            while loc_searching == True:
                x = random.randint(0, self.max_x-1)
                y = random.randint(0, self.max_y-1)
                if (self.location_dict[(x,y)]['occupied'] == False) & (self.location_dict[(x,y)]['water'] == False):
                    loc_searching = False
            moose = WildlifeCreator(type='moose', x=x, y=y)
            self.location_dict[(x, y)]['occupied'] = True
            self.location_dict[(x, y)]['moose'] = True
            self.location_dict[(x, y)]['occupying_animal'] = moose
            self.moose_list.append(moose)
        for i in range(self.wolf_num):
            loc_searching = True
            while loc_searching == True:
                x = random.randint(0, self.max_x-1)
                y = random.randint(0, self.max_y-1)
                if (self.location_dict[(x, y)]['occupied'] == False) & (self.location_dict[(x, y)]['water'] == False):
                    loc_searching = False
            wolf = WildlifeCreator(type='wolf', x=x, y=y)
            self.location_dict[(x, y)]['occupied'] = True
            self.location_dict[(x, y)]['occupying_animal'] = wolf
            self.location_dict[(x, y)]['wolf'] = True
            self.wolf_list.append(wolf)
        for i in range(self.squirrel_num):
            loc_searching = True
            while loc_searching == True:
                x = random.randint(0, self.max_x-1)
                y = random.randint(0, self.max_y-1)
                if self.location_dict[(x, y)]['water'] == False:
                    loc_searching = False
            squirrel = WildlifeCreator(type='squirrel', x=x, y=y)
            self.location_dict[(x, y)]['squirrel_count'] += 1
            self.location_dict[(x, y)]['occupying_squirrels'].append(squirrel)


