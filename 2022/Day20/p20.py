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
problemNum = 20
testRun = False
part2 = True


printing = False

default_file = f"Day{problemNum}/test.txt"

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"


class Data:
    def __init__(self,lines,decryptKey:int = 1) -> None:
        
        self.order: list[int] = [int(line.strip())*decryptKey for line in lines]
        self.dataSize: int = len(self.order) 
        self.hash: list[int] = [ k for k in range(self.dataSize)]
                

    def getData(self) -> list[int]:
        for i in range(self.dataSize):
            self.hash[i]
        return [self.order[i] for i in self.hash]

    '''
    hash:data
-   1, 2, -3, 3, -2, 0, 4
    0:1, 1:2, 2:-3, 3:3, 4:-2, 5:0, 6:4
    0:1 i0->1  
    0:1 moves between 1:2 and 2:-3
-   2, 1, -3, 3, -2, 0, 4
    1:2, 0:1, 2:-3, 3:3, 4:-2, 5:0, 6:4
    1:2 i0->2 
    1:2 moves between 2:-3 and 3:3
-   1, -3, 2, 3, -2, 0, 4
    0:1, 2:-3, 1:2, 3:3, 4:-2, 5:0, 6:4
    2:-3 i1->4 => 1>0>5>4
    -3 moves between -2 and 0:
-   1, 2, 3, -2, -3, 0, 4
    3:3 i2->5
    3 moves between 0 and 4:
-   1, 2, -2, -3, 0, 3, 4
    4:-2 i2->0
    -2 moves between 4 and 1:
-   1, 2, -3, 0, 3, 4, -2

    0 does not move:
-   1, 2, -3, 0, 3, 4, -2

    4 moves between -3 and 0:
-   1, 2, -3, 4, 0, 3, -2
    '''
    def reorderItem(self, hashItem:int) -> None:
        # Find the index of the item you want to rearrange
        index = self.hash.index(hashItem)
        # get item value
        move = self.order[hashItem]
        # Remove the item from the array
        hashItem = self.hash.pop(index)
        # move index to correct spot based on item value
        moveIndex = (index + move) % (self.dataSize-1)
        if moveIndex == 0:
            moveIndex = (self.dataSize-1)
        # Insert the item into the desired position
        self.hash.insert(moveIndex, hashItem)
        if printing:
            print(f" {move} moves between ?{(index) % self.dataSize}:{self.order[self.hash[(index) % self.dataSize]]} and ?{(index+2) % self.dataSize}:{self.order[self.hash[(index+2) % self.dataSize]]} ")
            print(f" {hashItem}:{move} i{index}->{moveIndex}")
        
    # mix up hash
    def mix(self) -> None:
        for i in range(self.dataSize):
            self.reorderItem(i)
            if printing: print(self.getData())

    def find_grove_coordinates(self):
        mixed = self.getData()
        # Find the position of the first 0 in the list
        zero_pos = mixed.index(0)
        
        # Extract the 1000th, 2000th, and 3000th numbers after the 0
        coord1 = mixed[(zero_pos + 1000) % len(mixed)]
        coord2 = mixed[(zero_pos + 2000) % len(mixed)]
        coord3 = mixed[(zero_pos + 3000) % len(mixed)]
        
        return coord1 + coord2 + coord3


def runPart1(lines):
    # Part 1
    d = Data(lines)
    print("initial Order")
    if printing: print(d.getData())
    d.mix()
    if printing: print(d.getData())
    print("part 1 results")
    print( d.find_grove_coordinates() )


def runPart2(lines):
    # Part 2
    print("part 2 start")
    d = Data(lines,811589153)
    print("initial Order")
    if printing: print(d.getData())
    mix =0
    while mix < 10:
        # mix Data 
        d.mix()
        mix += 1
    
    if printing: print(d.getData())
    print("part 2 results")
    print( d.find_grove_coordinates() )
    

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
        
        runPart1(lines)
        if part2:
            getTime()
            runPart2(lines)
        
        
        

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
