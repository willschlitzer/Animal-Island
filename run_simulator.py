from moose_controller import MooseCreator
from wolf_controller import WolfCreator
from squirrel_controller import SquirrelCreator
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import math
import time


def main():
    max_clockticks = 500
    max_x = 100
    max_y = 100
    moose_list, moose_locs = moose_populator(max_x=max_x, max_y=max_y)
    wolf_list, wolf_locs = wolf_populator(
        max_x=max_x, max_y=max_y, moose_locs=moose_locs
    )
    squirrel_list = squirrel_populator(max_x=max_x, max_y=max_y)
    # print(squirrel_list)
    vegetation_dict = vegatation_populator(max_x=max_x, max_y=max_y)
    run_island(
        max_x=max_x,
        max_y=max_y,
        moose_list=moose_list,
        wolf_list=wolf_list,
        squirrel_list=squirrel_list,
        max_clockticks=max_clockticks,
        vegetation_dict=vegetation_dict,
    )


def squirrel_populator(max_x, max_y):
    initial_squirrel_number = 500
    squirrel_list = []
    for i in range(initial_squirrel_number):
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        squirrel_list.append(SquirrelCreator(x, y))
    for squirrel in squirrel_list:
        squirrel.age = random.randint(2, 8)
    return squirrel_list


def vegatation_populator(max_x, max_y):
    vegetation_dict = {}
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            plant_loc = (x, y)
            vegetation_randomizer = random.randint(1, 100)
            if vegetation_randomizer < 85:
                vegetation_dict[plant_loc] = [True, 25]
            else:
                vegetation_dict[plant_loc] = [False, 5]
    return vegetation_dict


def moose_populator(max_x, max_y):
    initial_moose_number = 200
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
        moose.age = moose.age = random.randint(1, 48)
        moose.calf_year = random.randint(1, 42)
    return moose_list, moose_locs


def wolf_populator(max_x, max_y, moose_locs):
    initial_wolf_number = 100
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
        wolf.age = random.randint(4, 12)
        wolf.pup_year = random.randint(1, 8)
    return wolf_list, wolf_locs


def run_island(
    max_x, max_y, moose_list, wolf_list, squirrel_list, max_clockticks, vegetation_dict
):
    area = max_x * max_y
    clocktick = 0
    data_list = []
    veg_sum = veg_sum_finder(vegetation_dict=vegetation_dict)
    veg_fraction = float(veg_sum / area)
    diagnostic_list=[]
    print("Clockticks: " + str(clocktick))
    print("Wolf Population: " + str(len(wolf_list)))
    print("Moose Population: " + str(len(moose_list)))
    print("Squirrel Population: " + str(len(squirrel_list)))
    print("Vegetation Percentage: " + str(round(float(veg_sum / area * 100), 3)))
    # draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
    data_list.append(
        [
            clocktick,
            len(wolf_list),
            len(moose_list),
            len(squirrel_list),
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            veg_fraction,
        ]
    )
    while clocktick < max_clockticks:
        start_time = time.time()
        clocktick += 1
        moose_list, moose_locs, wolf_list, wolf_locs, squirrel_list, wolf_births, wolf_starves, wolf_old_age, moose_eaten, moose_births, moose_starves, moose_old_age, squirrels_born, squirrels_eaten, squirrels_starved, squirrels_old_age, vegetation_dict, veg_sum = single_clocktick(
            max_x=max_x,
            max_y=max_y,
            moose_list=moose_list,
            wolf_list=wolf_list,
            squirrel_list=squirrel_list,
            vegetation_dict=vegetation_dict,
        )
        data_list.append(
            [
                clocktick,
                len(wolf_list),
                len(moose_list),
                len(squirrel_list),
                wolf_births,
                wolf_starves,
                wolf_old_age,
                moose_eaten,
                moose_births,
                moose_starves,
                moose_old_age,
                squirrels_born,
                squirrels_eaten,
                squirrels_starved,
                squirrels_old_age,
                float(veg_sum / area),
            ])

        diagnostic_list.append(
            [
                clocktick,
                round((time.time() - start_time), 4),
                len(wolf_list),
                len(moose_list),
                len(squirrel_list),
                area,
            ])

        if clocktick % 10 == 0 and max_clockticks > clocktick:
            print("Clockticks: " + str(clocktick))
            print(
                "Vegetation Percentage: " + str(round(float(veg_sum / area * 100), 3))
            )
            print("Wolf Population: " + str(len(wolf_list)))
            print("Moose Population: " + str(len(moose_list)))
            print("Squirrel Population: " + str(len(squirrel_list)))
            print("Wolf Births: " + str(wolf_births))
            print("Wolf Starves: " + str(wolf_starves))
            print("Wolf Old Age Death: " + str(wolf_old_age))
            print("Moose Eaten: " + str(moose_eaten))
            print("Moose Births: " + str(moose_births))
            print("Moose Starves: " + str(moose_starves))
            print("Moose Old Age Death: " + str(moose_old_age))
            print("Squirrels Born: " + str(squirrels_born))
            print("Squirrels Eaten: " + str(squirrels_eaten))
            print("Squirrels Starved: " + str(squirrels_starved))
            print("Squirrels Old Age Death: " + str(squirrels_old_age))
            # draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)

    print("Final Population After " + str(max_clockticks) + " Clockticks")
    print("Wolf Population: " + str(len(wolf_list)))
    print("Moose Population: " + str(len(moose_list)))
    print("Squirrels Population: " + str(len(squirrel_list)))
    # draw_island(max_x=max_x, max_y=max_y, moose_locs=moose_locs, wolf_locs=wolf_locs)
    # print(data_list)
    data_array = np.array(data_list)
    diagnostic_array = np.array(diagnostic_list)
    # print(data_array)
    wolf_moose_df = pd.DataFrame(
        data_array,
        columns=[
            "clockticks",
            "wolves",
            "moose",
            "squirrels",
            "wolf_births",
            "wolf_starved",
            "wolf_old_age",
            "moose_eaten",
            "moose_births",
            "moose_starved",
            "moose_old_age",
            "squirrels_born",
            "squirrels_eaten",
            "squirrels_starved",
            "squirrels_old_age",
            "vegetation_fraction",
        ],
    )
    diagnostic_df = pd.DataFrame(
        diagnostic_array,
        columns=[
            "clockticks",
            "one_tick_time",
            "wolves",
            "moose",
            "squirrels",
            "area",
        ]
    )
    csv_creator(wolf_moose_df, "island_data")
    csv_creator(diagnostic_df, "diagnostics")
    data_controller(wolf_moose_df)
    # print(wolf_moose_df)

def csv_creator(df, file_name):
    folder_file = "run_data/" + file_name + ".csv"
    df.to_csv(folder_file, sep=',')

def data_controller(df):
    data_plotter(
        df,
        file_name="wolf_moose_squirrel_pop_chart",
        column_list=["wolves", "moose", "squirrels"],
        x_label="Clockticks",
        y_label="Population",
        title="Animal Populations",
    )
    data_plotter(
        df,
        file_name="wolf_moose_pop_chart",
        column_list=["wolves", "moose"],
        x_label="Clockticks",
        y_label="Population",
        title="Animal Populations",
    )
    data_plotter(
        df,
        file_name="wolf_moose_birth_chart",
        column_list=["wolf_births", "moose_births"],
        x_label="Clockticks",
        y_label="Birth Rate",
        title="Moose and Wolf Birth Rates",
    )
    data_plotter(
        df,
        file_name="moose_data",
        column_list=["moose_eaten", "moose_births", "moose_starved"],
        x_label="Clockticks",
        y_label="Moose",
        title="Moose Data",
    )
    data_plotter(
        df,
        file_name="starvation_data",
        column_list=["moose_starved", "wolf_starved", "squirrels_starved"],
        x_label="Clockticks",
        y_label="Number Starved",
        title="Animal Starvation",
    )
    data_plotter(
        df,
        file_name="vegetation_data",
        column_list=["vegetation_fraction"],
        x_label="Clockticks",
        y_label="Fraction",
        title="Vegetation Fraction",
    )
    # plt.show()


def data_plotter(df, file_name, column_list, x_label, y_label, title):
    folder_file = "run_data/" + file_name + ".png"
    df[column_list].plot()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(folder_file)


def single_clocktick(
    max_x, max_y, moose_list, wolf_list, squirrel_list, vegetation_dict
):
    moose_list, wolf_list, wolf_births, wolf_starves, wolf_old_age, moose_eaten, squirrel_list, squirrels_eaten = wolf_mover(
        max_x=max_x,
        max_y=max_y,
        moose_list=moose_list,
        wolf_list=wolf_list,
        squirrel_list=squirrel_list,
    )
    moose_list, moose_births, moose_starves, moose_old_age, vegetation_dict = moose_mover(
        max_x=max_x,
        max_y=max_y,
        moose_list=moose_list,
        wolf_list=wolf_list,
        vegetation_dict=vegetation_dict,
    )
    squirrel_list, squirrels_born, squirrels_starved, squirrels_old_age, vegetation_dict = squirrel_mover(
        max_x=max_x,
        max_y=max_y,
        squirrel_list=squirrel_list,
        vegetation_dict=vegetation_dict,
    )
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
        squirrels_born,
        squirrels_eaten,
        squirrels_starved,
        squirrels_old_age,
        vegetation_dict,
        veg_sum,
    )


def vegetation_growing(vegetation_dict):
    # Add a vegetation total sum
    veg_sum = veg_sum_finder(vegetation_dict=vegetation_dict)
    for key in vegetation_dict.keys():
        if (vegetation_dict[key][0] == False) and (vegetation_dict[key][1] >= 10):
            vegetation_dict[key][0] = True
        elif (vegetation_dict[key][0] == True) and (vegetation_dict[key][1] < 10):
            vegetation_dict[key][0] = False
        vegetation_dict[key][1] += 1

    return vegetation_dict, veg_sum


def veg_sum_finder(vegetation_dict):
    veg_sum = 0
    for key in vegetation_dict.keys():
        if vegetation_dict[key][0] == True:
            veg_sum += 1
    return veg_sum


def location_list(animal_list):
    loc_list = []
    for animal in animal_list:
        loc = (animal.x, animal.y)
        loc_list.append(loc)
    return loc_list


def squirrel_mover(max_x, max_y, squirrel_list, vegetation_dict):
    squirrels_born = 0
    squirrels_starved = 0
    squirrels_old_age = 0
    squirrels_hungry = 0
    for squirrel in squirrel_list:
        if squirrel.age > squirrel.death_age:
            squirrel_list.remove(squirrel)
            squirrels_old_age += 1
    for squirrel in squirrel_list:
        if squirrel.hunger >= 2:
            squirrel_list.remove(squirrel)
            squirrels_starved += 1
        elif squirrel.hunger >= 1:
            squirrels_hungry += 1
    if len(squirrel_list) > 0:
        potential_babies = random.randint(
            int(.01 * len(squirrel_list)), int(.1 * len(squirrel_list))
        )
        actual_babies = int(
            math.floor(potential_babies * (1 - (squirrels_hungry / len(squirrel_list))))
        )
    else:
        actual_babies = 0
    for squirrel in squirrel_list:
        squirrel.hunger += 1
        squirrel.age += 1
        squirrel.baby_age += 1
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)
        squirrel.x = x
        squirrel.y = y
        squirrel_loc = (x, y)
        if vegetation_dict[squirrel_loc][0] == True:
            vegetation_dict[squirrel_loc][0] = False
            vegetation_dict[squirrel_loc][1] -= 5
            squirrel.hunger = 0
        elif (vegetation_dict[squirrel_loc][0] == False) and (
            vegetation_dict[squirrel_loc][1] > 5
        ):
            vegetation_dict[squirrel_loc][1] -= 5
            squirrel.hunger = 0
    for i in range(actual_babies):
        squirrels_born += 1
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        squirrel_list.append(SquirrelCreator(x, y))
    return (
        squirrel_list,
        squirrels_born,
        squirrels_starved,
        squirrels_old_age,
        vegetation_dict,
    )


def wolf_mover(max_x, max_y, moose_list, wolf_list, squirrel_list):
    birth_age = 8
    wolf_births = 0
    wolf_starves = 0
    moose_eaten = 0
    squirrels_eaten = 0
    wolf_old_age = 0
    for wolf in wolf_list:
        if wolf.age > wolf.death_age:
            wolf_list.remove(wolf)
            wolf_old_age += 1
        elif wolf.hunger >= 11:
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
                if wolf.hunger > 0:
                    squirrels_eaten += 1
                    if squirrel.hunger == 0 and wolf.hunger >= 3:
                        wolf.hunger -= 3
                    elif squirrel.hunger < 2 and wolf.hunger >= 2:
                        wolf.hunger -= 2
                    elif squirrel.hunger < 2 and wolf.hunger < 2:
                        wolf.hunger = 0
                    else:
                        wolf.hunger -= 1
                    squirrel_list.remove(squirrel)
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
                    nearby_locs = []
                    for z in range(wolf.x - 3, wolf.x + 3):
                        for n in range(wolf.y - 3, wolf.y + 3):
                            nearby_loc = (z, n)
                            nearby_locs.append(nearby_loc)
                    for nearby_wolf in wolf_list:
                        nearby_wolf_loc = (nearby_wolf.x, nearby_wolf.y)
                        if nearby_wolf_loc in nearby_locs:
                            nearby_wolf.hunger = 0
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
            wolf.pup_year >= random.randint(birth_age - 4, birth_age + 2)
            and wolf.hunger < 7
            and wolf.age >= 15
            and (wolf.female == True)
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
    return (
        moose_list,
        wolf_list,
        wolf_births,
        wolf_starves,
        wolf_old_age,
        moose_eaten,
        squirrel_list,
        squirrels_eaten,
    )


def moose_mover(max_x, max_y, moose_list, wolf_list, vegetation_dict):
    birth_age = 15
    moose_births = 0
    moose_starves = 0
    moose_old_age = 0
    for moose in moose_list:
        if moose.age > moose.death_age:
            moose_list.remove(moose)
            moose_old_age += 1
        elif moose.hunger > 15:
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
        if moose_food[0] == True and moose.hunger > 0:
            vegetation_dict[moose_loc][0] = False
            vegetation_dict[moose_loc][1] = 0
            moose.hunger -= 4
        if (
            (moose.calf_year >= random.randint(birth_age - 10, birth_age + 5))
            and (moose.age >= 24)
            and (moose.hunger < 6)
            and (moose.female == True)
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
