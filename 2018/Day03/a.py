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

fabric_size = 1000

if testRun == False:
    fabric_size = 10
    default_file = f"{dirPath}/input.txt"
# elif part2:
#     default_file = f"{dirPath}/test2.txt"

def runPart1(lines):
    # Part 1
    print("part 1 start")
    results = count_overlapping_inches(lines)
    print(results)
  
def runPart2(lines):
    # Part 2
    print("part 2 start")

def parse_claim(claim):
    # Parse the claim string to extract coordinates and dimensions
    parts = claim.split()
    claim_id = int(parts[0][1:])
    left_edge, top_edge = map(int, parts[2][:-1].split(','))
    width, height = map(int, parts[3].split('x'))
    return claim_id, left_edge, top_edge, width, height

def mark_fabric(fabric, claim_id, left_edge, top_edge, width, height):
    # Mark the fabric claimed by a specific claim ID
    for i in range(left_edge, left_edge + width):
        for j in range(top_edge, top_edge + height):
            if fabric[i][j] == 0:
                fabric[i][j] = claim_id
            else:
                fabric[i][j] = -1  # Overlapping claim

def count_overlapping_inches(claims):
    fabric_size = 1000  # Assuming a fabric size of at least 1000 inches on each side
    fabric = [[0 for _ in range(fabric_size)] for _ in range(fabric_size)]
    overlapping_inches = 0

    for claim in claims:
        if len(claim) == 0: 
            continue
        claim_id, left_edge, top_edge, width, height = parse_claim(claim)
        mark_fabric(fabric, claim_id, left_edge, top_edge, width, height)

    for i in range(fabric_size):
        for j in range(fabric_size):
            if fabric[i][j] == -1:
                overlapping_inches += 1

    return overlapping_inches


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
