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
    total_freq = 0
    for line in lines:
        if len(line) == 0: 
            continue
        num = int(line[1:])
        if line[0] == '-':
            total_freq -= num
        else:
            total_freq += num
    print(total_freq)
            
    

def runPart2(lines):
    # Part 2
    print("part 2 start")
    total_freq = 0
    prev_freq = [total_freq]
    found_twice = False
    i = 0
    while not found_twice:
        if len(lines[i]) == 0: 
            i = (i+1) % len(lines)
        num = int(lines[i][1:])
        if lines[i][0] == '-':
            total_freq -= num
        else:
            total_freq += num
        if total_freq in prev_freq:
            found_twice = True
        prev_freq.append(total_freq)
        i = (i+1) % len(lines)
    print(total_freq)


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
