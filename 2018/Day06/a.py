import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

import itertools
import collections

start_time = time.time()
# get input file 
print("os.path.dirname(__file__)")
print(os.path.dirname(__file__))
dirPath = os.path.dirname(__file__)
testRun = False
part2 = True

printing = False

default_file = f"{dirPath}/test.txt"

if testRun == False:
    default_file = f"{dirPath}/input.txt"
# elif part2:
#     default_file = f"{dirPath}/test2.txt"


def runPart1(lines):
    # Part 1
    print("part 1 start")
    lines.pop() # remove last '' line in input

    # Example coordinates
    # coordinates = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]
    coordinates = [ tuple(int(coordinate) for coordinate in line.split(', ')) for line in lines ]

    # Find the size of the largest area that isn't infinite
    largest_area = find_largest_finite_area(coordinates)
    print(f"largest area {largest_area} ")

def manhattan_distance(coord1, coord2):
    """Calculate the Manhattan distance between two points."""
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def find_closest_coordinate(coord, coordinates):
    """Find the closest coordinate to a given point."""
    distances = [manhattan_distance(coord, point) for point in coordinates]
    min_distance = min(distances)
    if distances.count(min_distance) > 1:
        return None  # More than one closest point
    return distances.index(min_distance)

def find_largest_finite_area(coordinates):
    """Find the size of the largest area that isn't infinite."""
    # Determining the bounds of the grid
    max_x = max(coordinates, key=lambda x: x[0])[0]
    max_y = max(coordinates, key=lambda x: x[1])[1]

    # Initialize the area count for each coordinate
    areas = [0 for _ in coordinates]
    infinite_areas = set()

    # Iterate over each point in the grid
    for x, y in itertools.product(range(max_x + 1), range(max_y + 1)):
        closest = find_closest_coordinate((x, y), coordinates)
        if closest is not None:
            areas[closest] += 1
            # Mark areas as infinite if they touch the grid boundary
            if x == 0 or y == 0 or x == max_x or y == max_y:
                infinite_areas.add(closest)

    # Remove infinite areas from consideration
    for infinite_area in infinite_areas:
        areas[infinite_area] = 0

    return max(areas)



def runPart2(lines):
    # Part 2
    print("part 2 start")

    coordinates = [ tuple(int(coordinate) for coordinate in line.split(', ')) for line in lines ]

    # Find the size of the region with total distance to all coordinates less than 10000
    optimized_region_size = find_optimized_region_size(coordinates, 10000)
    print(f"region size {optimized_region_size} ")

def find_optimized_region_size(coordinates, max_total_distance):
    """Find the size of the optimized region where the total distance to all coordinates is less than a given value."""
    # Calculate the centroid of the given coordinates
    avg_x = sum(coord[0] for coord in coordinates) // len(coordinates)
    avg_y = sum(coord[1] for coord in coordinates) // len(coordinates)

    # Initialize the search area
    search_area = [(avg_x, avg_y)]
    visited = set(search_area)
    region_size = 0

    # Expand the search area until the total distance exceeds the limit
    while search_area:
        new_search_area = []
        for x, y in search_area:
            if total_distance_to_all_coordinates((x, y), coordinates) < max_total_distance:
                region_size += 1
                # Check the neighboring points
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_search_area.append(neighbor)
        search_area = new_search_area

    return region_size
def total_distance_to_all_coordinates(coord, coordinates):
    """Calculate the total Manhattan distance from a point to all given coordinates."""
    return sum(manhattan_distance(coord, point) for point in coordinates)


def main():
    global printing
    if len(sys.argv) < 2:
        filepath = default_file
    else:     
        filepath = sys.argv[1]
    s = ""
    if part2: s += " PART 2"
    if testRun: s += " TEST"
    print(f"~~~~~~~~~\n{filepath} {s}\n~~~~~~~~")
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    with open(filepath,'r') as file:
        data = file.read() # string
        lines = data.split('\n') # list of strings
        
        # if not part2:
        runPart1(lines)
        if part2:
            getTime()
            runPart2(lines)     

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
