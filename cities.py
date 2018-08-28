"""
Edward Milman - emilma01@dcs.bbk.ac.uk

Travelling Salesman - A program that will take input of lists of states and cities with their GPS coordinates and
calculate the distance between them. After shuffling the order of the items and calculating the total distances, the
best method is returned.
"""

from math import *
import random
from copy import deepcopy
import os


# reads in a list of cities data from a file and returns as a list of four tuples
# param: String file_name - the file name to be loaded
# return: road_map - list of four tuples of the data input
def read_cities(file_name):
    road_map = []
    stream = open(file_name, "r")
    data = stream.readlines()
    for line in data:
        state, city, lat, long = line.rstrip("\n").split("\t")
        road_map.append((state, city, float(lat), float(long)))
    return road_map


# prints a list of the cities and their locations. numbers formatted to 2 s.f.
# param: road_map - list of four tuple city data
def print_cities(road_map):
    print("{}{}{}{}".format("State".ljust(16), "City".ljust(16), "Lat".ljust(16), "Long".ljust(16)))
    for i in range(52):
        print("-", end="")
    print()
    for item in road_map:
        print("{}{}{}\t\t{}".format(item[0].ljust(16), item[1].ljust(16), round(item[2], 2), round(item[3], 2)))


# calculates the distance between 2 sets of positional coordinates
# param: float representations of GPS coordinates
# return: float - distance (in miles) between the input coordinates
def distance(lat1degrees, long1degrees, lat2degrees, long2degrees):
    earth_radius = 3956  # miles
    lat1 = radians(lat1degrees)
    long1 = radians(long1degrees)
    lat2 = radians(lat2degrees)
    long2 = radians(long2degrees)
    lat_difference = lat2 - lat1
    long_difference = long2 - long1
    sin_half_lat = sin(lat_difference / 2)
    sin_half_long = sin(long_difference / 2)
    a = sin_half_lat ** 2 + cos(lat1) * cos(lat2) * sin_half_long ** 2
    c = 2 * atan2(sqrt(a), sqrt(1.0 - a))
    return earth_radius * c


# returns as a floating point number the sum of all the distances between the cities in a cycle - the last
# city connects to the first city.
# param: road_map - a list of four tuple city position data
# return: float total - the total distance of the cycle
def compute_total_distance(road_map):
    total = 0
    length = len(road_map)
    for i in range(length):
        j = (i + 1) % length
        total += distance(road_map[i][2], road_map[i][3], road_map[j][2], road_map[j][3])
    return total


# given a roadmap and an index will swap the city at that index with the city at index + 1 - will 'wrap' around list
# to avoid illegal references
# param: road_map - a list of four tuple city position data
# param: index - integer giving an index within the roadmap
# return: tuple of the roadmap with the appropriate cities swapped, newly calculated total distance for the roadmap
def swap_adjacent_cities(road_map, index):
    to_swap = (index + 1) % len(road_map)
    road_map[index], road_map[to_swap] = road_map[to_swap], road_map[index]
    return road_map, compute_total_distance(road_map)


# given a roadmap and two indexes will swap the city at those indexes. if indexes are the same number, index2 has 1
# subtracted. will 'wrap' around list to avoid illegal references
# param: road_map - a list of four tuple city position data
# param: index - integer giving an index within the roadmap
# return: tuple of the roadmap with the appropriate cities swapped, newly calculated total distance for the roadmap
def swap_cities(road_map, index1, index2):
    # if indexes are the same, index2 is changed to the index before index1
    if index1 == index2:
        index2 = (index1 - 1) % len(road_map)
    road_map[index1], road_map[index2] = road_map[index2], road_map[index1]
    return road_map, compute_total_distance(road_map)


# given a roadmap will alternate between random swap_cities and swap_adjacent_cities 10000 times. each time the total
# distance is calculated and the combination with the shortest distance is saved
# param: road_map - a list of four tuple city position data
# return: list containing the 'best' ordering of cities found in the iterations
def find_best_cycle(road_map):
    swaps = 10000      # set to 8 to test
    length = len(road_map) - 1
    flip = True
    # random.seed(1)    # uncomment this line to test
    best = deepcopy(swap_adjacent_cities(road_map, random.randint(0, length)))
    for i in range(swaps):
        if flip:
            new = swap_adjacent_cities(road_map, random.randint(0, length))
        else:
            new = swap_cities(road_map, random.randint(0, length), random.randint(0, length))
        flip = not flip
        if new[1] < best[1]:
            best = deepcopy(new)
    return best


# Prints, in an easily understandable format, the cities and
# their connections, along with the cost for each connection
# and the total cost.
# param: road_map - a list of four tuple city position data
def print_map(road_map):
    print("{}{}".format("From:".rjust(16), "To:".rjust(25)))
    print("{}{}{}{}{}".format("State:".ljust(15), "City:".ljust(15), "State:".ljust(15), "City:".ljust(15), "Distance:"))
    total = 0
    for i in range(len(road_map)):
        nxt = (i + 1) % len(road_map)
        dist = distance(road_map[i][2], road_map[i][3], road_map[nxt][2], road_map[nxt][3])
        total += dist
        print("{}{}{}{}{}".format(road_map[i][0].ljust(15), road_map[i][1].ljust(15), road_map[nxt][0].ljust(15),
                                  road_map[nxt][1].ljust(15), round(dist, 2)))
    print("Total distance: {} miles".format(round(total, 2)))


# asks a yes or no question of the user and records the response
# param: question - string of the question to be asked
# return: boolean - true for yes, false otherwise
def ask_yes_or_no(question):
    while True:
        try:
            response = input("{}".format(question))
            if response[0] not in {"y", "Y", "n", "N"}:
                raise ValueError("Expecting char input Y or N")
        except ValueError:
            print("Please input Y for yes or N for no.")
        else:
            return response[0] in {"y", "Y"}


def main():
    # establish loop
    loop = True
    while loop:
        # read in data
        road_map = read_cities("city-data.txt")
        print("City data input:")
        # print start data
        print_cities(road_map)
        print("\nThe computer will now look for the most efficient route.")
        os.system("pause")
        # print best cycle from 10000 random shuffles
        print_map(find_best_cycle(road_map)[0])
        print("\nThat took a lot of thinking")
        # prompt to try again
        loop = ask_yes_or_no("Want to try again?")


if __name__ == "__main__":
    main()
