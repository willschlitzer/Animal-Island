from moose_controller import MooseCreator
from wolf_controller import WolfCreator
from squirrel_controller import SquirrelCreator
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random


def main():
    max_clockticks = 500
    max_x = 25
    max_y = 25
    moose_list, moose_locs = moose_populator(max_x=max_x, max_y=max_y)
    wolf_list, wolf_locs = wolf_populator(
        max_x=max_x, max_y=max_y, moose_locs=moose_locs
    )
    squirrel_list = squirrel_populator(max_x=max_x, max_y=max_y)
    vegetation_dict = vegatation_populator(max_x=max_x, max_y=max_y)
    run_island(
        max_x=max_x,
        max_y=max_y,
        moose_list=moose_list,
        wolf_list=wolf_list,
        squirrel_list=squirrel_list,
        max_clockticks=max_clockticks,
        vegetation_dict=vegetation_dict
    )

def squirrel_populator(max_x, max_y):
    initial_squirrel_number = 100
    squirrel_list = []
    for i in range(initial_squirrel_number):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        squirrel_list.append(SquirrelCreator(x, y))


def vegatation_populator(max_x, max_y):
    vegetation_dict = {}
    for x in range(max_x):
        for y in range(max_y):
            plant_loc = (x, y)
            vegetation_dict[plant_loc] = [True, 0]
    return vegetation_dict

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
    for moose in moose_list:
        moose.age = 18
        moose.calf_year = 10
    return moose_list, moose_locs


def wolf_populator(max_x, max_y, moose_locs):
    initial_wolf_number = 35
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
    for wolf in wolf_list:
        wolf.age = 12
    return wolf_list, wolf_locs


def run_island(
    max_x, max_y, moose_list, wolf_list, squirrel_list, max_clockticks, vegetation_dict
):
    area = max_x * max_y
    clocktick = 0
    data_list = []
    print("Clockticks: " + str(clocktick))
    print("Wolf Population: " + str(len(wolf_list)))
    print("Moose Population: " + str(len(moose_list)))
    # draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
    data_list.append([clocktick, len(wolf_list), len(moose_list), 0, 0, 0, 0, 0, 0, 0, 1])
    while clocktick < max_clockticks:
        clocktick += 1
        moose_list, moose_locs, wolf_list, wolf_locs, squirrel_list, wolf_births, wolf_starves, wolf_old_age, moose_eaten, moose_births, moose_starves, moose_old_age, vegetation_dict, veg_sum = single_clocktick(
            max_x=max_x, max_y=max_y, moose_list=moose_list, wolf_list=wolf_list, squirrel_list=squirrel_list, vegetation_dict=vegetation_dict
        )
        data_list.append(
            [
                clocktick,
                len(wolf_list),
                len(moose_list),
                wolf_births,
                wolf_starves,
                wolf_old_age,
                moose_eaten,
                moose_births,
                moose_starves,
                moose_old_age,
                float(veg_sum/area)
            ]
        )
        if clocktick % 10 == 0 and max_clockticks > clocktick:
            print("Clockticks: " + str(clocktick))
            print("Vegetation Percentage: " + str(round(float(veg_sum/area * 100),3)))
            print("Wolf Population: " + str(len(wolf_list)))
            print("Moose Population: " + str(len(moose_list)))
            print("Wolf Births: " + str(wolf_births))
            print("Wolf Starves: " + str(wolf_starves))
            print("Wolf Old Age Death: " + str(wolf_old_age))
            print("Moose Eaten: " + str(moose_eaten))
            print("Moose Births: " + str(moose_births))
            print("Moose Starves: " + str(moose_starves))
            print("Moose Old Age Death: " + str(moose_old_age))
            # draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)

    print("Final Population After " + str(max_clockticks) + " Clockticks")
    print("Wolf Population: " + str(len(wolf_list)))
    print("Moose Population: " + str(len(moose_list)))
    # draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
    # print(data_list)
    data_array = np.array(data_list)
    # print(data_array)
    wolf_moose_df = pd.DataFrame(
        data_array,
        columns=[
            "clockticks",
            "wolves",
            "moose",
            "wolf_births",
            "wolf_starves",
            "wolf_old_age",
            "moose_eaten",
            "moose_births",
            "moose_starves",
            "moose_old_age",
            "vegetation_fraction"
        ],
    )
    wolf_moose_file = "run_data/wolf_moose.csv"
    wolf_moose_fig = "run_data/wolf_moose_chart.png"
    wolf_moose_df.to_csv(wolf_moose_file, sep=",")
    #print(wolf_moose_df)
    column_list = ["wolves", "moose"]
    wolf_moose_df[column_list].plot()
    plt.xlabel("Clock tick")
    plt.savefig(wolf_moose_fig)
    plt.show()


def single_clocktick(max_x, max_y, moose_list, wolf_list, squirrel_list, vegetation_dict):
    moose_list, wolf_list, wolf_births, wolf_starves, wolf_old_age, moose_eaten, squirrel_list = wolf_mover(
        max_x=max_x, max_y=max_y, moose_list=moose_list, wolf_list=wolf_list, squirrel_list=squirrel_list
    )
    moose_list, moose_births, moose_starves, moose_old_age, vegetation_dict = moose_mover(
        max_x=max_x, max_y=max_y, moose_list=moose_list, wolf_list=wolf_list, vegetation_dict=vegetation_dict
    )
    squirrel_list, vegetation_dict = squirrel_mover(max_x=max_x, max_y=max_y, squirrel_list=squirrel_list, vegetation_dict=vegetation_dict)
    vegetation_dict, veg_sum = vegetation_growing(vegetation_dict)

    wolf_locs = location_list(wolf_list)
    moose_locs = location_list(moose_list)
    return (
        moose_list,
        moose_locs,
        wolf_list,
        wolf_locs,
        squirrel_list,
        wolf_births,
        wolf_starves,
        wolf_old_age,
        moose_eaten,
        moose_births,
        moose_starves,
        moose_old_age,
        vegetation_dict,
        veg_sum
    )

def vegetation_growing(vegetation_dict):
    # Add a vegetation total sum
    veg_sum = 0
    for key in vegetation_dict.keys():
        if vegetation_dict[key][0] == True:
            veg_sum += 1
        if (vegetation_dict[key][0] == False) and (vegetation_dict[key][1] >= 25):
            vegetation_dict[key][0] = True
        vegetation_dict[key][1] += 1
    return vegetation_dict, veg_sum

def location_list(animal_list):
    loc_list = []
    for animal in animal_list:
        loc = (animal.x, animal.y)
        loc_list.append(loc)
    return loc_list

def squirrel_mover(max_x, max_y, squirrel_list, vegetation_dict):
    birth_age = 4
    for squirrel in squirrel_list:
        if squirrel.age > squirrel.death_age:
            squirrel_list.remove(squirrel)
    babies = 0
    for squirrel in squirrel_list:
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        squirrel.x = x
        squirrel.y = y
        squirrel_loc = (x, y)
        if (vegetation_dict[squirrel_loc][0] == True) and (vegetation_dict[squirrel_loc][1] < 15):
            vegetation_dict[squirrel_loc][0] = False
            vegetation_dict[squirrel_loc][1] -= 5
        elif (vegetation_dict[squirrel_loc][0] == True) and (vegetation_dict[squirrel_loc][1] > 15):
            vegetation_dict[squirrel_loc][1] -= 5
        elif vegetation_dict[squirrel_loc][0] == False:
            vegetation_dict[squirrel_loc][1] -= 5
        if squirrel.baby_age > random.randint(birth_age-1, birth_age+1) and squirrel.age > 8:
            babies += 1
            squirrel.baby_age = 0
    for i in range(babies):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        squirrel_list.append(SquirrelCreator(x, y))
    return squirrel_list, vegetation_dict




def wolf_mover(max_x, max_y, moose_list, wolf_list, squirrel_list):
    birth_age = 8
    wolf_births = 0
    wolf_starves = 0
    moose_eaten = 0
    wolf_old_age = 0
    for wolf in wolf_list:
        if wolf.age > wolf.death_age:
            wolf_list.remove(wolf)
            wolf_old_age += 1
        elif wolf.hunger >= 13:
            wolf_list.remove(wolf)
            wolf_starves += 1
    for wolf in wolf_list:
        wolf.hunger += 1
        wolf.age += 1
        wolf.pup_year += 1
        wolf_locs = location_list(wolf_list)
        moose_locs = location_list(moose_list)
        wolf_loc = (wolf.x, wolf.y)
        wolf_locs.remove((wolf.x, wolf.y))
        for squirrel in squirrel_list:
            squirrel_loc = (squirrel.x, squirrel.y)
            if squirrel_loc == wolf_loc:
                if wolf.hunger > 5:
                    squirrel_list.remove(squirrel)
                    wolf.hunger -= 5
                else:
                    squirrel_list.remove(squirrel)
                    wolf.hunger = 0
        adjacent_moose, empty_locs = check_adjacency(
            wolf_loc, moose_locs, max_x=max_x, max_y=max_y
        )
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
                    moose_eaten += 1
        else:
            nearby_wolves, empty_locs = check_adjacency(
                wolf_loc, wolf_locs, max_x=max_x, max_y=max_y
            )
            moved = False
            while not moved:
                if empty_locs == []:
                    moved = True
                else:
                    new_loc = location_selector(loc_list=empty_locs)
                    wolf_locs.append(new_loc)
                    wolf.x = new_loc[0]
                    wolf.y = new_loc[1]
                    moved = True
        if (
            wolf.pup_year >= random.randint(birth_age - 2, birth_age + 2)
            and wolf.hunger < 9
            and wolf.age >= 15
        ):
            wolf.pup_year = 0
            animal_locs = wolf_locs + moose_locs
            birthed = False
            while not birthed:
                x = wolf.x
                y = wolf.y
                mom_loc = (x, y)
                nearby_animals = check_adjacency(
                    mom_loc, animal_locs, max_x=max_x, max_y=max_y
                )
                x += random.randint(-1, 1)
                y += random.randint(-1, 1)
                pup_loc = (x, y)
                if (
                    (pup_loc not in nearby_animals)
                    and (max_x > x >= 0)
                    and (max_y > y >= 0)
                    and (pup_loc != mom_loc)
                ):
                    wolf_locs.append(pup_loc)
                    wolf_list.append(WolfCreator(x, y))
                    wolf_births += 1
                    birthed = True
                else:
                    birthed = True
    return moose_list, wolf_list, wolf_births, wolf_starves, wolf_old_age, moose_eaten, squirrel_list


def moose_mover(max_x, max_y, moose_list, wolf_list, vegetation_dict):
    birth_age = 30
    moose_births = 0
    moose_starves = 0
    moose_old_age = 0
    for moose in moose_list:
        if moose.age > moose.death_age:
            moose_list.remove(moose)
            moose_old_age += 1
        elif moose.hunger > 10:
            moose_list.remove(moose)
            moose_starves += 1
    for moose in moose_list:
        moose.age += 1
        moose.hunger += 1
        moose.calf_year += 1
        wolf_locs = location_list(wolf_list)
        moose_locs = location_list(moose_list)
        animal_locs = moose_locs + wolf_locs
        moose_loc = (moose.x, moose.y)
        moved = False
        while not moved:
            nearby_animals, empty_locs = check_adjacency(
                moose_loc, animal_locs, max_x=max_x, max_y=max_y
            )
            if empty_locs == []:
                moved = True
            else:
                new_loc = location_selector(loc_list=empty_locs)
                moose_locs.append(new_loc)
                moose.x = new_loc[0]
                moose.y = new_loc[1]
                moved = True
        moose_loc = (moose.x, moose.y)
        moose_food = vegetation_dict[moose_loc]
        if moose_food[0] == True and moose.hunger>0:
            vegetation_dict[moose_loc][0] = False
            vegetation_dict[moose_loc][1] = 0
            moose.hunger -= 2
        if (moose.calf_year >= random.randint(birth_age - 5, birth_age + 5)) and (
            moose.age >= 36
        ):
            moose.calf_year = 0
            animal_locs = wolf_locs + moose_locs
            birthed = False
            while not birthed:
                x = moose.x
                y = moose.y
                mom_loc = (x, y)
                nearby_animals = check_adjacency(
                    mom_loc, animal_locs, max_x=max_x, max_y=max_y
                )
                x += random.randint(-1, 1)
                y += random.randint(-1, 1)
                calf_loc = (x, y)
                if (
                    (calf_loc not in nearby_animals)
                    and (max_x > x >= 0)
                    and (max_y > y >= 0)
                    and (calf_loc != mom_loc)
                ):
                    moose_locs.append(calf_loc)
                    moose_list.append(MooseCreator(x, y))
                    moose_births += 1
                    birthed = True
                else:
                    birthed = True
    return moose_list, moose_births, moose_starves, moose_old_age, vegetation_dict


def location_selector(loc_list):
    if len(loc_list) == 1:
        return loc_list[0]
    else:
        loc_pick = random.randint(0, len(loc_list) - 1)
        return loc_list[loc_pick]


def check_adjacency(loc, loc_list, max_x, max_y):
    x_loc = loc[0]
    y_loc = loc[1]
    adjacent_locs = []
    empty_locs = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            test_x = x_loc + dx
            test_y = y_loc + dy
            test_loc = (test_x, test_y)
            if test_loc in loc_list:
                adjacent_locs.append(test_loc)
            elif (
                (test_loc not in loc_list)
                and (max_x > test_x >= 0)
                and (max_y > test_y >= 0)
            ):
                empty_locs.append(test_loc)
    return adjacent_locs, empty_locs


def draw_island(max_x, max_y, moose_locs, wolf_locs):
    for row in range(max_y):
        column_string = ""
        for column in range(max_x):
            location = (column, row)
            if location in moose_locs:
                column_string += "M"
            elif location in wolf_locs:
                column_string += "W"
            else:
                column_string += "-"
        print(column_string)


if __name__ == "__main__":
    main()
