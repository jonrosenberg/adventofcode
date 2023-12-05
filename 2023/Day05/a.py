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

    



def runPart1(data):
    # Part 1
    print("part 1 start")
    almanac = data.split('\n\n')
    seeds = [int(id) for id in almanac[0].split(': ')[1].split(' ')]
    seed_to_soil = [tuple(int(id) for id in line.split(' ')) for line in almanac[1].split('\n') if line[0].isdigit() ]
    soil_to_fertilizer = [tuple(int(id) for id in line.split(' ')) for line in almanac[2].split('\n') if line[0].isdigit() ]
    fertilizer_to_water = [tuple(int(id) for id in line.split(' ')) for line in almanac[3].split('\n') if line[0].isdigit() ]
    water_to_light = [tuple(int(id) for id in line.split(' ')) for line in almanac[4].split('\n') if line[0].isdigit() ]
    light_to_temperature = [tuple(int(id) for id in line.split(' ')) for line in almanac[5].split('\n') if line[0].isdigit() ]
    temperature_to_humidity = [tuple(int(id) for id in line.split(' ')) for line in almanac[6].split('\n') if line[0].isdigit() ]
    humidity_to_location = [tuple(int(id) for id in line.split(' ')) for line in almanac[7].split('\n') if len(line) != 0 and line[0].isdigit() ]
    
    # Process each seed through the mappings
    final_locations = []
    for seed in seeds:
        soil = apply_map(seed, seed_to_soil)
        fertilizer = apply_map(soil, soil_to_fertilizer)
        water = apply_map(fertilizer, fertilizer_to_water)
        light = apply_map(water, water_to_light)
        temperature = apply_map(light, light_to_temperature)
        humidity = apply_map(temperature, temperature_to_humidity)
        location = apply_map(humidity, humidity_to_location)
        final_locations.append(location)

    # Find the lowest location number
    lowest_location = min(final_locations)
    print("Lowest location number:", lowest_location)

# Function to apply the conversion map
def apply_map(source_number, conversion_map):
    for dest_start, source_start, length in conversion_map:
        if source_start <= source_number < source_start + length:
            return dest_start + (source_number - source_start)
    return source_number  # If not found in map, return the same number

    
def runPart2(data):
    # Part 2
    print("part 2 start")
    almanac = data.split('\n\n')
    seeds = [int(id) for id in almanac[0].split(': ')[1].split(' ')]
    # Initialize an empty list to store the tuples
    seed_ranges = []

    # Iterate through the list in pairs and create tuples
    for i in range(0, len(seeds), 2):
        if i + 1 < len(seeds):
            seed_ranges.append((seeds[i], seeds[i + 1]))

    # Generate all seed numbers from the ranges
    # all_seeds = []
    # for start, length in seed_ranges:
    #     all_seeds.extend(range(start, start + length))


    seed_to_soil = [tuple(int(id) for id in line.split(' ')) for line in almanac[1].split('\n') if line[0].isdigit() ]
    soil_to_fertilizer = [tuple(int(id) for id in line.split(' ')) for line in almanac[2].split('\n') if line[0].isdigit() ]
    fertilizer_to_water = [tuple(int(id) for id in line.split(' ')) for line in almanac[3].split('\n') if line[0].isdigit() ]
    water_to_light = [tuple(int(id) for id in line.split(' ')) for line in almanac[4].split('\n') if line[0].isdigit() ]
    light_to_temperature = [tuple(int(id) for id in line.split(' ')) for line in almanac[5].split('\n') if line[0].isdigit() ]
    temperature_to_humidity = [tuple(int(id) for id in line.split(' ')) for line in almanac[6].split('\n') if line[0].isdigit() ]
    humidity_to_location = [tuple(int(id) for id in line.split(' ')) for line in almanac[7].split('\n') if len(line) != 0 and line[0].isdigit() ]
    
    # Convert the mappings to dictionaries
    seed_to_soil_map = create_map(seed_to_soil)
    soil_to_fertilizer_map = create_map(soil_to_fertilizer)
    fertilizer_to_water_map = create_map(fertilizer_to_water)
    water_to_light_map = create_map(water_to_light)
    light_to_temperature_map = create_map(light_to_temperature)
    temperature_to_humidity_map = create_map(temperature_to_humidity)
    humidity_to_location_map = create_map(humidity_to_location)
 
    final_locations = []

        
    # for seed in all_seeds:
    # lowest_location = 99999999999999
    final_locations_ranges = set()
    for start, length in seed_ranges:
        soil_range = apply_map_to_range(start, length, seed_to_soil_map)
        fertilizer_range = apply_map_to_range(soil_range[0], soil_range[1], soil_to_fertilizer_map)
        water_range = apply_map_to_range(fertilizer_range[0], fertilizer_range[1], fertilizer_to_water_map)
        light_range = apply_map_to_range(water_range[0], water_range[1], water_to_light_map)
        temperature_range = apply_map_to_range(light_range[0], light_range[1], light_to_temperature_map)
        humidity_range = apply_map_to_range(temperature_range[0], temperature_range[1], temperature_to_humidity_map)
        location_range = apply_map_to_range(humidity_range[0], humidity_range[1], humidity_to_location_map)
        final_locations_ranges.add(location_range[0])
        # if location < lowest_location:
        #         lowest_location = location

    # Find the lowest location number
    # lowest_location = min(final_locations)
    print("Lowest location number:", lowest_location)

def create_map(mapping_data):
    mapping_dict = {}
    for dest_start, source_start, length in mapping_data:
        for i in range(length):
            mapping_dict[source_start + i] = dest_start + i
    return mapping_dict

def apply_map_to_range(start, length, conversion_map):
    min_val = float('inf')
    max_val = start + length - 1

    for i in range(start, min(start + 1000, max_val + 1)):  # Limit the range to handle large datasets
        mapped_value = conversion_map.get(i, i)
        if mapped_value < min_val:
            min_val = mapped_value
    return (min_val, max_val - start + 1)

def apply_map_optimized(source_number, conversion_map):
    return conversion_map.get(source_number, source_number)  # Return the same number if not found in map


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
        
        # if not part2:
        runPart1(data)
        if part2:
            getTime()
            runPart2(data)
        
        
        

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
