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
    game_id = 0
    id_sum = 0
    max_colors = {
        'red':12,
        'green':13,
        'blue':14
                  }
    for line in lines:
        if len(line) == 0: continue
        game_id += 1
        possible = True
        for cube_set in line.split(':')[1].split(";"):
            for cubes in cube_set.split(','):
                cube = cubes.split(' ')
                if max_colors[cube[2]] < int(cube[1]):
                    possible = False
                    break
            if not possible:
                break
        if possible:
            id_sum += game_id
    print(id_sum)                
                

def runPart2(lines):
    # Part 2
    print("part 2 start")
    sum_power = 0
    for line in lines:
        if len(line) == 0: continue
        min_colors = {
            'red':0,
            'green':0,
            'blue':0
                    }
        for cube_set in line.split(':')[1].split(";"):
            for cubes in cube_set.split(','):
                cube = cubes.split(' ')
                if min_colors[cube[2]] < int(cube[1]):
                    min_colors[cube[2]] = int(cube[1])
        power = 1
        for val in min_colors.values():
            power *= val
        sum_power += power

    print(sum_power)

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
