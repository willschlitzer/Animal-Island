import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from island_instance import IslandCreator
from wildlife_instance import WildlifeCreator


def main():
    max_clockticks = 500
    max_x = 250
    max_y = 250
    lake_num = 25
    moose_num = 3000
    wolf_num = 1000
    squirrel_num = 10000
    island = IslandCreator(
        max_x=max_x,
        max_y=max_y,
        lake_num=lake_num,
        moose_num=moose_num,
        wolf_num=wolf_num,
        squirrel_num=squirrel_num,
    )
    run_island(island=island, max_clockticks=max_clockticks)
    data_collector(island=island)


def run_island(island, max_clockticks):
    island.run_data.append(island.tick_data)
    while island.clocktick < max_clockticks:
        island.clocktick += 1
        island.empty_tick_data()
        single_clocktick(island=island)
        island.tick_data_generator()
        island.data_appender()
        if island.clocktick % 25 == 0:
            status_printer(island=island)


def single_clocktick(island):
    wolf_mover(island=island)
    moose_mover(island=island)
    squirrel_mover(island=island)
    veg_grower(island=island)
    locust_attack(island=island)


def wolf_mover(island):
    for wolf in island.wolf_list:
        x, y = wolf.x, wolf.y
        old_loc = (x, y)
        if (wolf.age > wolf.death_age) or (wolf.hunger > wolf.starve):
            island.location_dict[old_loc]["occupied"] = False
            island.location_dict[old_loc]["wolf"] = False
            island.location_dict[old_loc]["occupying_animal"] = None
            if wolf.age > wolf.death_age:
                island.wolf_old_age += 1
            else:
                island.wolf_starve += 1
            island.wolf_list.remove(wolf)
            continue
        if (
            (wolf.baby_age > wolf.birth_age)
            & (wolf.hunger < wolf.starve - 1)
            & (wolf.female == True)
        ):
            empty_locs = check_adjacency(island=island, x=x, y=y)
            if len(empty_locs) > 0:
                cub_loc = random.choice(empty_locs)
                cub_x, cub_y = cub_loc[0], cub_loc[1]
                cub = WildlifeCreator("wolf", cub_x, cub_y)
                island.location_dict[cub_loc]["occupied"] = True
                island.location_dict[cub_loc]["wolf"] = True
                island.location_dict[cub_loc]["occupying_animal"] = cub
                island.wolf_list.append(cub)
                island.wolf_birth += 1
                wolf.baby_age = 0
        wolf.age += 1
        wolf.baby_age += 1
        wolf.hunger += 1
        i = 0
        while i <= 2:
            moose_locs = check_adjacency(island=island, x=x, y=y, moose_hunting=True)
            if len(moose_locs) > 0:
                hunting_loc = random.choice(moose_locs)
                moose_meal = island.location_dict[hunting_loc]["occupying_animal"]
                island.moose_list.remove(moose_meal)
                island.moose_eaten += 1
                wolf.hunger = 0
                island.location_dict[old_loc]["occupying_animal"] = None
                island.location_dict[old_loc]["wolf"] = False
                island.location_dict[hunting_loc]["occupying_animal"] = wolf
                island.location_dict[hunting_loc]["moose"] = False
                island.location_dict[hunting_loc]["wolf"] = True
                wolf.x, wolf.y = hunting_loc[0], hunting_loc[1]
                new_loc = hunting_loc
            else:
                empty_locs = check_adjacency(island=island, x=x, y=y)
                if empty_locs == []:
                    new_loc = old_loc
                else:
                    new_loc = random.choice(empty_locs)
                    island.location_dict[old_loc]["occupied"] = False
                    island.location_dict[old_loc]["occupying_animal"] = None
                    island.location_dict[old_loc]["wolf"] = False
                    island.location_dict[new_loc]["occupied"] = True
                    island.location_dict[new_loc]["occupying_animal"] = wolf
                    island.location_dict[new_loc]["wolf"] = True
                    wolf.x, wolf.y = new_loc[0], new_loc[1]
            if (island.location_dict[new_loc]["squirrel_count"] > 0) & (wolf.hunger > 0):
                eating_total = 2 * island.location_dict[new_loc]["squirrel_count"]
                if wolf.hunger > eating_total:
                    wolf.hunger -= eating_total
                else:
                    wolf.hunger = 0
                island.squirrel_eaten += island.location_dict[new_loc]["squirrel_count"]
                island.location_dict[new_loc]["squirrel_count"] = 0
                for squirrel in island.location_dict[new_loc]["occupying_squirrels"]:
                    island.squirrel_list.remove(squirrel)
                island.location_dict[new_loc]["occupying_squirrels"] = []
            i += 1


def moose_mover(island):
    for moose in island.moose_list:
        x, y = moose.x, moose.y
        old_loc = (x, y)
        if (moose.age > moose.death_age) or (moose.hunger > moose.starve):
            island.location_dict[old_loc]["occupied"] = False
            island.location_dict[old_loc]["moose"] = False
            island.location_dict[old_loc]["occupying_animal"] = None
            if moose.age > moose.death_age:
                island.moose_old_age += 1
            else:
                island.moose_starve += 1
            island.moose_list.remove(moose)
            continue
        if (moose.baby_age > moose.birth_age) & (moose.hunger < moose.starve - 1) * (
            moose.female == True
        ):
            empty_locs = check_adjacency(island=island, x=x, y=y)
            if len(empty_locs) > 0:
                cub_loc = random.choice(empty_locs)
                cub_x, cub_y = cub_loc[0], cub_loc[1]
                cub = WildlifeCreator("moose", cub_x, cub_y)
                island.location_dict[cub_loc]["occupied"] = True
                island.location_dict[cub_loc]["moose"] = True
                island.location_dict[cub_loc]["occupying_animal"] = cub
                island.moose_list.append(cub)
                island.moose_birth += 1
                moose.baby_age = 0
        moose.age += 1
        moose.baby_age += 1
        moose.hunger += 1
        empty_locs = check_adjacency(island, x, y)
        if empty_locs == []:
            new_loc = old_loc
        else:
            new_loc = random.choice(empty_locs)
            island.location_dict[old_loc]["occupied"] = False
            island.location_dict[old_loc]["occupying_animal"] = None
            island.location_dict[old_loc]["moose"] = False
            island.location_dict[new_loc]["occupied"] = True
            island.location_dict[new_loc]["occupying_animal"] = moose
            island.location_dict[new_loc]["moose"] = True
            moose.x, moose.y = new_loc[0], new_loc[1]
        if island.location_dict[new_loc]["growth"] >= 10:
            island.location_dict[new_loc]["growth"] -= 10
            if moose.hunger > 2:
                moose.hunger -= 2
            else:
                moose.hunger = 0




def squirrel_mover(island):
    for squirrel in island.squirrel_list:
        x, y = squirrel.x, squirrel.y
        old_loc = (x, y)
        if (squirrel.age > squirrel.death_age) or (squirrel.hunger > squirrel.starve):
            island.location_dict[old_loc]["squirrel_count"] -= 1
            island.location_dict[old_loc]["occupying_squirrels"].remove(squirrel)
            if squirrel.age > squirrel.death_age:
                island.squirrel_old_age += 1
            else:
                island.squirrel_starve += 1
            island.squirrel_list.remove(squirrel)
            continue
        squirrel.age += 1
        squirrel.baby_age += 1
        squirrel.hunger += 1
        available_squares = check_adjacency(island=island, x=x, y=y, squirrel=True)
        if (
            (squirrel.baby_age > squirrel.birth_age)
            & (squirrel.hunger < squirrel.starve)
            & (squirrel.female == True)
        ):
            cub_loc = random.choice(available_squares)
            cub_loc_x, cub_loc_y = cub_loc[0], cub_loc[1]
            cub = WildlifeCreator("squirrel", cub_loc_x, cub_loc_y)
            island.location_dict[cub_loc]["squirrel_count"] += 1
            island.location_dict[cub_loc]["occupying_squirrels"].append(cub)
            island.squirrel_list.append(cub)
            island.squirrel_birth += 1
            squirrel.baby_age = 0
        new_loc = random.choice(available_squares)
        squirrel.x, squirrel.y = new_loc[0], new_loc[1]
        island.location_dict[old_loc]["squirrel_count"] -= 1
        island.location_dict[old_loc]["occupying_squirrels"].remove(squirrel)
        island.location_dict[new_loc]["squirrel_count"] += 1
        island.location_dict[new_loc]["occupying_squirrels"].append(squirrel)
        if island.location_dict[new_loc]["growth"] > 3 and squirrel.hunger > 0:
            island.location_dict[new_loc]["growth"] -= 3
            squirrel.hunger -= 1


def veg_grower(island):
    for loc in island.location_dict.keys():
        island.location_dict[loc]["growth"] += 1
        if (island.location_dict[loc]["growth"] >= 15) & (
            island.location_dict[loc]["veg"] == False
        ):
            island.location_dict[loc]["veg"] = True
        elif (island.location_dict[loc]["growth"] < 15) & (
            island.location_dict[loc]["veg"] == True
        ):
            island.location_dict[loc]["veg"] = False


def check_adjacency(island, x, y, moose_hunting=False, squirrel=False):
    adjacent_squares = []
    for a in range(x - 1, x + 2):
        for b in range(y - 1, y + 2):
            if (0 <= a < island.max_x) & (0 <= b < island.max_y):
                if island.location_dict[(a, b)]["water"] == False:
                    adjacent_squares.append((a, b))
    if moose_hunting == True:
        moose_locs = []
        for square in adjacent_squares:
            if (island.location_dict[square]["occupied"] == True) & (
                island.location_dict[square]["moose"] == True
            ):
                moose_locs.append(square)
        return moose_locs
    elif squirrel == True:
        return adjacent_squares
    else:
        empty_locs = []
        for square in adjacent_squares:
            if island.location_dict[square]["occupied"] == False:
                empty_locs.append(square)
        return empty_locs

def locust_attack(island):
    if random.randint(0, 100) <= 5:
        island.create_swarm()
    for swarm in island.locust_list:
        if swarm.age > swarm.death_age:
            island.locust_list.remove(swarm)
            continue
        swarm_targets = []
        for x in range(swarm.x-swarm.size, swarm.x+swarm.size + 1):
            for y in range(swarm.y - swarm.size, swarm.y + swarm.size + 1):
                if (0 <= x < island.max_x) & (0 <= y < island.max_y):
                    swarm_targets.append((x,y))
        for locust in range(swarm.population):
            target = random.choice(swarm_targets)
            if island.location_dict[target]["growth"] >= 1:
                island.location_dict[target]["growth"] -= 1
                swarm.fed += 1
        swarm.age += 1
        if swarm.fed >= .1 * swarm.population:
            swarm.population = int(swarm.population * 1.2)
            swarm.size += 1
        else:
            swarm.population = int(swarm.population * .8)
            swarm.size += 3


def status_printer(island):
    print("Clocktick: " + str(island.clocktick))
    print("Wolves: " + str(island.wolf_count))
    print("Moose: " + str(island.moose_count))
    print("Squirrels: " + str(island.squirrel_count))
    print("Wolf Births: " + str(island.wolf_birth))
    print("Wolf Starves: " + str(island.wolf_starve))
    print("Wolf Old Age Death: " + str(island.wolf_old_age))
    print("Moose Eaten: " + str(island.moose_eaten))
    print("Moose Births: " + str(island.moose_birth))
    print("Moose Starves: " + str(island.moose_starve))
    print("Moose Old Age Deaths: " + str(island.moose_old_age))
    print("Squirrel Births: " + str(island.squirrel_birth))
    print("Squirrel Starves: " + str(island.squirrel_starve))
    print("Squirrel Old Age Deaths: " + str(island.squirrel_old_age))
    print("Squirrels Eaten: " + str(island.squirrel_eaten))
    print("Vegetation Percentage: " + str(island.veg_pct))

def data_collector(island):
    data_array = np.array(island.run_data)
    df = pd.DataFrame(data_array,
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
    df = df.set_index('clockticks')
    csv_creator(df, 'run_data')
    data_controller((df))

def csv_creator(df, file_name):
    folder_file = "run_data/" + file_name + ".csv"
    df.to_csv(folder_file, sep=",")

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

if __name__ == "__main__":
    main()
