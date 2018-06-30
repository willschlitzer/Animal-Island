import random
import numpy as np
from island_instance import IslandCreator
from wildlife_instance import WildlifeCreator

def main():
    max_clockticks = 10
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


def run_island(island, max_clockticks):
    veg_pct = veg_pct_calc(island=island)
    island.run_data.append({
        'clocktick':island.clocktick,
        'veg_pct':veg_pct
        'wolves':len(island.wolf_list),
        'moose':len(island.moose_list),
        'squirrels':len(island.squirrel_list),
        'wolf_births':0,
        'wolf_starves':0,
        'wolf_old_age':0,
        'moose_eaten':0,
        'moose_births':0,
        'moose_starved':0,
        'moose_old_age'0,

    })
    while self.clocktick <= max_clocktick:
        self.clocktick += 1
        single_clocktick(island=island)

def single_clocktick(island):
    island.run_data.append({

    })
    wolf_mover(island=island)

def wolf_mover(island):
    for wolf in island.wolf_list:
        x = wolf.x
        y = wolf.y
        if (wolf.age > wolf.death_age) or (wolf.hunger > wolf.starve):




if __name__ == '__main__':
    main()