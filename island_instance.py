class IslandCreator:
    def __init__(self, max_x, max_y, lake_num, moose_start):
        import random
        self.max_x = max_x
        self.max_y = max_y
        self.lake_num = lake_num
        self.moose_start = moose_start


    def vegetation_begin(self):
        veg_dict = {}
        for x in range(max_x):
            for y in range(max_y):
                if random.randint(0, 100) <= 85:
                    veg_dict[(x,y)] = [True, random.randint(10, 100)]
                else:
                    veg_dict[(x,y)] = [False, random.randint(0,9)]
        self.veg_dict = veg_dict

