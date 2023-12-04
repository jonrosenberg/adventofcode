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
    total_wins = 0
    for line in lines:
        if len(line) == 0:
            continue
        win_str, num_str = line.split(': ')[1].split(' | ')
        wins = [int(n) for n in win_str.split(" ") if len(n) > 0]
        nums = [int(n) for n in num_str.split(" ") if len(n) > 0]
        win_count = 0
        for n in nums:
            if n in wins:
                if win_count:
                    win_count *= 2
                else: 
                    win_count = 1
        total_wins += win_count
    print(total_wins)

def runPart2(lines):
    # Part 2
    print("part 2 start")
    cards = {}
    for line in lines:
        if len(line) == 0:
            continue
        card_id, card_nums = line.split(': ')
        card_id = int(card_id.split(' ')[-1])
        win_str, num_str = card_nums.split(' | ')
        wins = [int(n) for n in win_str.split(" ") if len(n) > 0]
        nums = [int(n) for n in num_str.split(" ") if len(n) > 0]
        win_count = 0
        for n in nums:
            if n in wins:
                if win_count:
                    win_count += 1
                else: 
                    win_count = 1
        cards[card_id] = win_count
    total_c = 0
    for id in cards.keys():
        total_c += add_copies(cards,id,1)
    print(total_c)
    print("8172507 part 2 correct answer")
        
        
def add_copies(cards,id,total_c):
    # total_c += 1
    for i in range(id, id+cards[id]):
        total_c += 1
        total_c = add_copies(cards,i+1,total_c)
    return total_c
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
