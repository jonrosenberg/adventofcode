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
    # Example race data
    # races = [
    #     (7, 9),   # (Time, Record)
    #     (15, 40),
    #     (30, 200)
    # ]
    times = lines[0].split() 
    distances = lines[1].split() 
    races = [ (int(times[i+1]),int(distances[i+1])) for i in range(len(times)-1)]
    # Calculate the number of ways to win for each race
    ways_to_win_each_race = [calculate_ways_to_win(time, record) for time, record in races]

    # Calculate the total number of ways to win across all races
    total_ways_to_win = 1
    for ways in ways_to_win_each_race:
        total_ways_to_win *= ways

    print(total_ways_to_win) 
    print(ways_to_win_each_race)

def calculate_ways_to_win(time, record):
    """Calculate the number of ways to win the race."""
    ways_to_win = 0
    for hold_time in range(time):
        travel_time = time - hold_time
        distance = hold_time * travel_time
        if distance > record:
            ways_to_win += 1
    return ways_to_win

def runPart2(lines):
    # Part 2
    print("part 2 start")
    # New race data for the single race
    # single_race_time = 71530
    # single_race_record = 940200
    single_race_time = int(''.join(lines[0].split()[1:]))
    single_race_record = int(''.join(lines[1].split()[1:]))
    # Calculate the number of ways to win this single race
    ways_to_win_single_race = calculate_ways_to_win_single_race(single_race_time, single_race_record)
    print(ways_to_win_single_race)

def calculate_ways_to_win_single_race(time, record):
    """Calculate the number of ways to win the single race."""
    ways_to_win = 0
    for hold_time in range(1, time):  # starting from 1 since holding for 0 won't move the boat
        travel_time = time - hold_time
        distance = hold_time * travel_time
        if distance > record:
            ways_to_win += 1
    return ways_to_win










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
