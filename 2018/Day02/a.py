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
    twos = 0
    threes = 0
    for line in lines:
        count_char = {}
        for c in line:
            if c in count_char:
                count_char[c] += 1
            else:
                count_char[c] = 1
        if 2 in count_char.values():
            twos += 1
        if 3 in count_char.values():
            threes += 1
    print(twos*threes)

def runPart2(lines):
    # Part 2
    print("part 2 start")
    
    for y1 in range(len(lines)-1):
        for y2 in range(y1+1,len(lines)-1):
            diff_count = 0
            fabric_id = ''
            for ci in range(len(lines[0])):
                if lines[y1][ci] != lines[y2][ci]:
                    diff_count += 1
                else:
                    fabric_id += lines[y1][ci]
                if diff_count > 1:
                    break
            if diff_count == 1:
                print(fabric_id)
                return True
            
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
