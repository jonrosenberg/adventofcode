import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

from datetime import datetime
from collections import defaultdict

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
    lines.pop()
    result = solve_guard_puzzle(lines)
    print(result)

def solve_guard_puzzle(records):
    # Sort the records by timestamp
    records.sort(key=lambda record: datetime.strptime(record[1:17], "%Y-%m-%d %H:%M"))

    # Initialize variables to track the current guard and sleep times
    current_guard = None
    asleep_time = None
    guard_sleep_minutes = defaultdict(int)
    guard_minute_count = defaultdict(lambda: defaultdict(int))

    # Process each record
    for record in records:
        time, action = record[1:17], record[19:]
        minute = int(time[-2:])

        if 'Guard' in action:
            current_guard = int(re.findall(r'\d+', action)[0])
        elif 'falls asleep' in action:
            asleep_time = minute
        elif 'wakes up' in action:
            for m in range(asleep_time, minute):
                guard_sleep_minutes[current_guard] += 1
                guard_minute_count[current_guard][m] += 1

    # Find the guard with the most minutes asleep
    sleepiest_guard = max(guard_sleep_minutes, key=guard_sleep_minutes.get)
    sleepiest_minute = max(guard_minute_count[sleepiest_guard], key=guard_minute_count[sleepiest_guard].get)

    return sleepiest_guard * sleepiest_minute

def runPart2(lines):
    # Part 2
    print("part 2 start")
    lines.pop()
    result = solve_guard_puzzle_strategy2(lines)
    print(result)

def solve_guard_puzzle_strategy2(records):
    # Sort the records by timestamp
    records.sort(key=lambda record: datetime.strptime(record[1:17], "%Y-%m-%d %H:%M"))

    # Initialize variables to track the current guard and sleep times
    current_guard = None
    asleep_time = None
    guard_minute_count = defaultdict(lambda: defaultdict(int))

    # Process each record
    for record in records:
        time, action = record[1:17], record[19:]
        minute = int(time[-2:])

        if 'Guard' in action:
            current_guard = int(re.findall(r'\d+', action)[0])
        elif 'falls asleep' in action:
            asleep_time = minute
        elif 'wakes up' in action:
            for m in range(asleep_time, minute):
                guard_minute_count[current_guard][m] += 1

    # Find the guard most frequently asleep on the same minute
    max_sleep = 0
    max_guard = None
    max_minute = None

    for guard, minutes in guard_minute_count.items():
        for minute, count in minutes.items():
            if count > max_sleep:
                max_sleep = count
                max_guard = guard
                max_minute = minute

    return max_guard * max_minute

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
