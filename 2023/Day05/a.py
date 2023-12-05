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
    seed_to_soil_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[1].split('\n') if line[0].isdigit() ]
    soil_to_fertilizer_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[2].split('\n') if line[0].isdigit() ]
    fertilizer_to_water_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[3].split('\n') if line[0].isdigit() ]
    water_to_light_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[4].split('\n') if line[0].isdigit() ]
    light_to_temperature_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[5].split('\n') if line[0].isdigit() ]
    temperature_to_humidity_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[6].split('\n') if line[0].isdigit() ]
    humidity_to_location_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[7].split('\n') if len(line) != 0 and line[0].isdigit() ]
    
    # Process each seed through the mappings
    final_locations = []
    for seed in seeds:
        soil = apply_map(seed, seed_to_soil_data)
        fertilizer = apply_map(soil, soil_to_fertilizer_data)
        water = apply_map(fertilizer, fertilizer_to_water_data)
        light = apply_map(water, water_to_light_data)
        temperature = apply_map(light, light_to_temperature_data)
        humidity = apply_map(temperature, temperature_to_humidity_data)
        location = apply_map(humidity, humidity_to_location_data)
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

    seed_to_soil_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[1].split('\n') if line[0].isdigit() ]
    soil_to_fertilizer_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[2].split('\n') if line[0].isdigit() ]
    fertilizer_to_water_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[3].split('\n') if line[0].isdigit() ]
    water_to_light_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[4].split('\n') if line[0].isdigit() ]
    light_to_temperature_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[5].split('\n') if line[0].isdigit() ]
    temperature_to_humidity_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[6].split('\n') if line[0].isdigit() ]
    humidity_to_location_data = [tuple(int(id) for id in line.split(' ')) for line in almanac[7].split('\n') if len(line) != 0 and line[0].isdigit() ]
    
    # Create the actual mappings
    seed_to_soil_map = create_mapping(seed_to_soil_data)
    soil_to_fertilizer_map = create_mapping(soil_to_fertilizer_data)
    fertilizer_to_water_map = create_mapping(fertilizer_to_water_data)
    water_to_light_map = create_mapping(water_to_light_data)
    light_to_temperature_map = create_mapping(light_to_temperature_data)
    temperature_to_humidity_map = create_mapping(temperature_to_humidity_data)
    humidity_to_location_map = create_mapping(humidity_to_location_data)
    
    
    # Process each seed range through the mappings
    final_locations = set()
    for seed_start, seed_length in seed_ranges:
        seed_end = seed_start + seed_length - 1
        current_ranges = [(seed_start, seed_end)]

        for mapping in [seed_to_soil_map, 
                        soil_to_fertilizer_map, 
                        fertilizer_to_water_map, 
                        water_to_light_map, 
                        light_to_temperature_map, 
                        temperature_to_humidity_map, 
                        humidity_to_location_map]:  # continue with other mappings
            new_ranges = []
            for r in current_ranges:
                new_ranges.extend(apply_map_range(r, mapping))
            current_ranges = new_ranges

        for r in current_ranges:
            final_locations.add(r[0])
            final_locations.add(r[1])
            #final_locations.update(range(r[0], r[1] + 1))

    # Find the lowest location number
    lowest_location = min(final_locations)
    print(lowest_location)

# Function to create mappings with handling overlapping ranges
def create_mapping(mapping_data):
    mapping_dict = {}
    for dest_start, source_start, length in mapping_data:
        source_range = (source_start, source_start + length - 1)
        dest_range = (dest_start, dest_start + length - 1)
        mapping_dict[source_range] = dest_range
    return mapping_dict

# Function to apply the conversion map using range mappings with overlapping handling
def apply_map_range(source_range, conversion_map):
    result_ranges = []
    source_start, source_end = source_range

    for map_source_range in conversion_map:
        map_source_start, map_source_end = map_source_range
        if map_source_end >= source_start and map_source_start <= source_end:
            overlap_start = max(map_source_start, source_start)
            overlap_end = min(map_source_end, source_end)
            offset = overlap_start - map_source_start
            dest_start, dest_end = conversion_map[map_source_range]
            result_ranges.append((dest_start + offset, dest_start + offset + (overlap_end - overlap_start)))
    
    return result_ranges if result_ranges else [source_range]

def apply_map_optimized(source1_start, source1_length, destination_ranges):
    final_desination_ranges = set()
    source1_end = source1_start + source1_length
    for dest_start, source2_start, length in destination_ranges:
        source2_end = source2_start + length
        # Check if overlap (either range is entirely to the left or right of the other)
        # get overlaping data
        if not (source1_end < source2_start or source2_end < source1_start):
            overlap_start = max(source1_start, source2_start)
            overlap_end = min(source1_end, source2_end)
            overlap_range.add(tuple(overlap_start, overlap_end)) 
        
        overlap_range = conversion_map.get(source_number, source_number) # Return the same number if not found in map
        # TODO: get non-overlapping ranges
        # TODO: 
        # Return the same number if not found in map (dest_range) 
        


    return overlap_range 


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
