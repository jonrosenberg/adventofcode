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
elif part2:
    default_file = f"{dirPath}/test2.txt"

    



def runPart1(lines):
    # Part 1
    print("part 1 start")
    calibration = 0
    for line in lines:
        if len(line) == 0:
            continue
        digit_list = re.findall(r'\d', line)
        calibration += int(digit_list[0]+digit_list[-1])
    print(calibration)

def runPart2(lines):
    # Part 2
    print("part 2 start")
    # Define a regex pattern to match numeric digits and spelled-out numbers
    pattern = r'(?s:.*)(one|two|three|four|five|six|seven|eight|nine|\d)'
    calibration = 0
    # Dictionary mapping spelled-out numbers to integers
    spelled_out_to_int = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    count = 1
    for line in lines:
        if len(line) == 0:
            continue
        first = None
        last = None
        sub_line = ""
        for c in line:
            dig = None
            if c.isdigit():
                dig = c
            else:
                sub_line += c
                for k,v in spelled_out_to_int.items():
                    if sub_line.endswith(k):
                        # process as digit v
                        dig = str(v)
            if dig is not None:
                last = dig
                if first is None:
                    first = dig
        #pdb.set_trace()
        print(f"{count:4d}: {int(first+last)} = {first} {last} : {line}")
        calibration += int(first+last)
        count += 1
    print(calibration)

# Define a function to convert spelled-out numbers to integers
def replace_spelled_out(match):
    
    return str(spelled_out_to_int[match.group(0)])
    

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
        
        if not part2:
            runPart1(lines)
        if part2:
            getTime()
            runPart2(lines)
        
        
        

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
