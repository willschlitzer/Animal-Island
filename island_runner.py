import random
import numpy as np
from island_instance import IslandCreator
from wildlife_instance import WildlifeCreator

def main():
    max_x = 100
    max_y = 100
    lake_num = 5
    moose_num = 100
    wolf_num = 25
    squirrel_num = 100
    island = IslandCreator(
        max_x = max_x,
        max_y = max_y,
        lake_num= lake_num,
        moose_num= moose_num,
        wolf_num = wolf_num,
        squirrel_num = squirrel_num
    )
    for key in island.location_dict.keys():
        if island.location_dict[key]['occupied'] == True:
            print(island.location_dict[key])
    for key in island.location_dict.keys():
        if island.location_dict[key]['water'] == True:
            print(island.location_dict[key])


if __name__ == '__main__':
    main()