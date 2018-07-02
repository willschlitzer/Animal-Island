import random
import numpy as np
from wildlife_instance import WildlifeCreator, LocustAttack


class IslandCreator:
    def __init__(self, max_x, max_y, lake_num, moose_num, wolf_num, squirrel_num):
        self.max_x = max_x
        self.max_y = max_y
        self.lake_num = lake_num
        self.moose_num = moose_num
        self.wolf_num = wolf_num
        self.squirrel_num = squirrel_num
        self.clocktick = 0
        self.run_data = []
        self.cumulative_run_data = []
        self.locust_list = []
        self.location_dict_creator()
        self.lake_builder()
        self.animal_generator()
        self.age_randomizer()
        self.empty_tick_data()
        self.tick_data_generator()
        self.initiate_cumulative_run_data()

    def empty_tick_data(self):
        self.wolf_birth = 0
        self.wolf_starve = 0
        self.wolf_old_age = 0
        self.moose_eaten = 0
        self.moose_birth = 0
        self.moose_starve = 0
        self.moose_old_age = 0
        self.squirrel_birth = 0
        self.squirrel_starve = 0
        self.squirrel_old_age = 0
        self.squirrel_eaten = 0

    def tick_data_generator(self):
        self.wolf_count = len(self.wolf_list)
        self.moose_count = len(self.moose_list)
        self.squirrel_count = len(self.squirrel_list)
        self.veg_pct_calc()
        self.tick_data = [
            self.clocktick,
            self.wolf_count,
            self.moose_count,
            self.squirrel_count,
            self.wolf_birth,
            self.wolf_starve,
            self.wolf_old_age,
            self.moose_eaten,
            self.moose_birth,
            self.moose_starve,
            self.moose_old_age,
            self.squirrel_birth,
            self.squirrel_starve,
            self.squirrel_old_age,
            self.squirrel_eaten,
            self.veg_pct,
        ]

    def initiate_cumulative_run_data(self):
        self.cumulative_wolf_birth = 0
        self.cumulative_wolf_starve = 0
        self.cumulative_wolf_old_age = 0
        self.cumulative_moose_eaten = 0
        self.cumulative_moose_birth = 0
        self.cumulative_moose_old_age = 0
        self.cumulative_squirrel_birth = 0
        self.cumulative_squirrel_eaten = 0

    def data_appender(self):
        self.run_data.append(self.tick_data)
        # self.cumulative_wolf_birth += self.wolf_birth
        # self.cumulative_wolf_starve += self.wolf_starve
        # self.cumulative_wolf_old_age += self.wolf_old_age

    def veg_pct_calc(self):
        area = self.max_x * self.max_y
        veg_count = 0
        for a in self.location_dict.keys():
            if self.location_dict[a]["veg"] == True:
                veg_count += 1
        self.veg_pct = round(veg_count / area * 100, 2)

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
                    "water": False,
                    "veg": veg,
                    "growth": growth,
                    "occupied": False,
                    "occupying_animal": None,
                    "moose": False,
                    "wolf": False,
                    "squirrel_count": 0,
                    "occupying_squirrels": [],
                }
        self.location_dict = location_dict

    def lake_builder(self):
        water_locs = []
        for i in range(self.lake_num):
            lake_center_x = random.randint(0, self.max_x - 1)
            lake_center_y = random.randint(0, self.max_y - 1)
            size = abs(int(np.random.normal(3, .75)))
            for x in range(lake_center_x - size, lake_center_x + size):
                for y in range(lake_center_y - size, lake_center_y + size):
                    if (0 <= x < self.max_x) & (0 <= y < self.max_y):
                        water_locs.append((x, y))
        for loc in water_locs:
            self.location_dict[loc]["water"] = True
            self.location_dict[loc]["veg"] = False
            self.location_dict[loc]["growth"] = False

    def animal_generator(self):
        self.moose_list = []
        self.wolf_list = []
        self.squirrel_list = []
        for i in range(self.moose_num):
            loc_searching = True
            while loc_searching == True:
                x = random.randint(0, self.max_x - 1)
                y = random.randint(0, self.max_y - 1)
                if (self.location_dict[(x, y)]["occupied"] == False) & (
                    self.location_dict[(x, y)]["water"] == False
                ):
                    loc_searching = False
            moose = WildlifeCreator(type="moose", x=x, y=y)
            self.location_dict[(x, y)]["occupied"] = True
            self.location_dict[(x, y)]["moose"] = True
            self.location_dict[(x, y)]["occupying_animal"] = moose
            self.moose_list.append(moose)
        for i in range(self.wolf_num):
            loc_searching = True
            while loc_searching == True:
                x = random.randint(0, self.max_x - 1)
                y = random.randint(0, self.max_y - 1)
                if (self.location_dict[(x, y)]["occupied"] == False) & (
                    self.location_dict[(x, y)]["water"] == False
                ):
                    loc_searching = False
            wolf = WildlifeCreator(type="wolf", x=x, y=y)
            self.location_dict[(x, y)]["occupied"] = True
            self.location_dict[(x, y)]["occupying_animal"] = wolf
            self.location_dict[(x, y)]["wolf"] = True
            self.wolf_list.append(wolf)
        for i in range(self.squirrel_num):
            loc_searching = True
            while loc_searching == True:
                x = random.randint(0, self.max_x - 1)
                y = random.randint(0, self.max_y - 1)
                if self.location_dict[(x, y)]["water"] == False:
                    loc_searching = False
            squirrel = WildlifeCreator(type="squirrel", x=x, y=y)
            self.location_dict[(x, y)]["squirrel_count"] += 1
            self.location_dict[(x, y)]["occupying_squirrels"].append(squirrel)
            self.squirrel_list.append(squirrel)

    def age_randomizer(self):
        for animal_list in [self.wolf_list, self.moose_list, self.squirrel_list]:
            for animal in animal_list:
                animal.age = random.randint(0, animal.death_age)
                animal.baby_age = random.randint(0, int(1.2*animal.birth_age))

    def create_swarm(self):
        swarm_x = random.randint(0, self.max_x-1)
        swarm_y = random.randint(0, self.max_y-1)
        swarm = LocustAttack(swarm_x, swarm_y)
        self.locust_list.append(swarm)

