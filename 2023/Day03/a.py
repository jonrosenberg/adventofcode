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
    part_nums = 0
    y_max = len(lines)-1
    x_max = len(lines[0])
    y = 0
    while y < y_max:
        x = 0
        x1 = None
        while x < x_max:
            c = lines[y][x]
            # check if num
            if c.isdigit():
                if x1 == None:
                    x1 = x
                x2 = x
            # check if end of num           
            if x1 != None and (x2 == x_max-1 or not c.isdigit()):
                if printing: print(f"end of num {''.join([lines[y][xi] for xi in range(x1,x2+1)])}")
                part_nums += get_part_num_p1(lines,y,x1,x2)
            # reset if not num
            if not c.isdigit():
                x1 = None
            x += 1
        y += 1
    print(part_nums)

def get_part_num_p1(lines,y,x1,x2):
    part_num = False
    y_max = len(lines)-1
    x_max = len(lines[0])
    # get all the numbers next to num
    check = [ (ry,rx) for rx in range(x1-1,x2+2) for ry in range(y-1,y+2) 
             if (ry != y or not x1 <= rx <= x2)
             and 0 <= rx < x_max and 0 <= ry < y_max ]
    for iy,ix in check:
        c = lines[iy][ix]
        if printing: print(f"{iy}{ix}{c}",end=' ')
        if not c.isdigit() and c != '.':
            part_num = True
            break
    if part_num:
        num_str = ''
        for xi in range(x1,x2+1):
            num_str += lines[y][xi]
        if printing: print(f"\nadd part_num {num_str}")
        return int(num_str)
    else:
        return 0

def runPart2(lines):
    # Part 2
    print("part 2 start")
    gears = {}
    y_max = len(lines)-1
    x_max = len(lines[0])
    y = 0
    while y < y_max:
        x = 0
        x1 = None
        while x < x_max:
            c = lines[y][x]
            # check if num
            if c.isdigit():
                if x1 == None:
                    x1 = x
                x2 = x
            # check if end of num           
            if x1 != None and (x2 == x_max-1 or not c.isdigit()):
                if printing: print(f"end of num {''.join([lines[y][xi] for xi in range(x1,x2+1)])}")
                gears = get_part_num_p2(lines,gears,y,x1,x2)
            # reset if not num
            if not c.isdigit():
                x1 = None
            x += 1
        y += 1
    
    gear_ratios = sum( gr[0]*gr[1] for gr in gears.values() if len(gr) == 2 )

    print(gear_ratios)

def get_part_num_p2(lines,g,y,x1,x2):
    part_num = False
    y_max = len(lines)-1
    x_max = len(lines[0])
    # get all the numbers next to num
    check = [ (ry,rx) for rx in range(x1-1,x2+2) for ry in range(y-1,y+2) 
             if (ry != y or not x1 <= rx <= x2)
             and 0 <= rx < x_max and 0 <= ry < y_max ]
    for iy,ix in check:
        c = lines[iy][ix]
        if printing: print(f"{iy}{ix}{c}",end=' ')
        if c=='*':
            num_str = ''
            for xi in range(x1,x2+1):
                num_str += lines[y][xi]
            if printing: print(f"\nadd part_num {num_str}")
            if (iy,ix) in g:
                g[(iy,ix)].append(int(num_str))
            else:
                g[(iy,ix)] = [int(num_str)]
            return g
            
    return g


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
