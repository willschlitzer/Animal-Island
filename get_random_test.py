import random
import time

def main():
    bit_list = []
    bit_start = time.time()
    for i in range(1000):
        bit_list.append(random.getrandbits(1))
    print("Time for Bits:")
    print(time.time()-bit_start)
    print(bit_list)
    choice_list = []
    choice_start = time.time()
    for i in range(1000):
        choice_list.append(random.choice([True, False]))
    print("Time for Choice:")
    print(time.time()-choice_start)
    print(choice_list)


main()