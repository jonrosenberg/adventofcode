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
    lines.pop() # remove last '' line 
    result = react_polymer(lines[0])
    print(result)
def react_polymer(polymer):
    """
    Reacts the polymer according to the specified rules:
    - Units of the same type and opposite polarity (represented by capitalization) react and are destroyed.
    """
    # Create a list to represent the polymer for easier manipulation
    polymer_list = list(polymer)

    # Initialize a variable to track the position in the polymer
    i = 0

    # Loop through the polymer to react units
    while i < len(polymer_list) - 1:
        # Check if adjacent units are of the same type but opposite polarity
        if polymer_list[i].lower() == polymer_list[i + 1].lower() and polymer_list[i] != polymer_list[i + 1]:
            # Units react: remove them from the list
            del polymer_list[i:i + 2]

            # Move back one position to check for new reactions
            i = max(i - 1, 0)
        else:
            # No reaction: move to the next unit
            i += 1

    # Return the length of the remaining polymer
    return len(polymer_list)



def runPart2(lines):
    # Part 2
    print("part 2 start")
    # lines.pop() # remove last '' line 
    best_unit, shortest_length = find_best_unit_to_remove(lines[0])

    print(f" removing {best_unit}, returns the best result of {shortest_length}")

def remove_and_react(polymer, unit_to_remove):
    """
    Removes all instances of a given unit (regardless of polarity) from the polymer,
    and then fully reacts the remaining polymer.
    """
    # Remove all instances of the unit and its opposite polarity
    polymer_removed = polymer.replace(unit_to_remove.lower(), "").replace(unit_to_remove.upper(), "")
    
    # React the polymer after removal
    return react_polymer(polymer_removed)

def find_best_unit_to_remove(polymer):
    """
    Finds the unit type whose removal results in the shortest fully-reacted polymer.
    """
    # Get a set of unique unit types in the polymer (ignoring polarity)
    unique_units = set(unit.lower() for unit in polymer)

    # Initialize a dictionary to store the lengths of the reacted polymers after each unit removal
    reacted_lengths = {}

    # Iterate over each unique unit type
    for unit in unique_units:
        # React the polymer after removing the current unit
        reacted_length = remove_and_react(polymer, unit)
        # Store the length
        reacted_lengths[unit] = reacted_length

    # Find the unit that results in the shortest polymer
    shortest_unit = min(reacted_lengths, key=reacted_lengths.get)

    return shortest_unit, reacted_lengths[shortest_unit]





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
