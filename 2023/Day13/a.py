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

def runPart1(notes):
    # Part 1

    """
    Calculates the summary based on the reflection patterns in the notes.

    Args:
    notes (list of list of str): The patterns to analyze.

    Returns:
    int: The calculated summary.
    """
    print("part 1 start")
    summary = 0
    for i, note in enumerate(notes):
        horizontal_reflection, top = find_reflection(note)
        summary += top*100
        
        if not horizontal_reflection:
            transposed_note = transpose_list_of_characters(note)
            vertical_reflection, left = find_reflection(transposed_note)
            summary += left
        else:
            vertical_reflection = False
            left = 0
        print(f"{i+1}\t hrz {horizontal_reflection}\t top {top}\t vrt {vertical_reflection}\t left {left} note {len(note[0])}x{len(note)}")
        top, left = 0, 0
        vertical_reflection = False
    print(f"sumamry {summary}")

def find_reflection(pattern):
    """
    Finds if there is a reflection in the pattern and calculates the distance to the edge of the pattern.

    Args:
    pattern (list of str): The pattern to check for reflection.

    Returns:
    tuple: (True, distance) if reflection is found, else (False, 0).
    """
    reflection = False
    pattern_size = len(pattern)
    for i in range(pattern_size-1):
        if pattern[i] == pattern[i+1]:
            reflection = True
            reflection_index = i
            edge_distance = min(i,pattern_size-(i+2))
            for x in range(1,edge_distance+1):
                if pattern[(i+1)+x] != pattern[i-x]:
                    reflection = False
                    reflection_index = None
                    break
            if reflection == True:
                break

    if reflection:
        return True, reflection_index+1
    else:
        return False, 0
    
def transpose_list_of_characters(list_of_strings):
    """
    Transposes a list of strings. 
    This means it converts a list where each element is a string into a list where each element 
    is a string formed from the nth characters of each original string.

    Args:
    list_of_strings (list of str): The list of strings to transpose.

    Returns:
    list of str: The transposed list of strings.
    """
    return [''.join(char_tuple) for char_tuple in zip(*list_of_strings)]

def runPart2(notes):
    # Part 2
    print("part 2 start")



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
        
        notes = [ note.split('\n') for note in data[:-1].split('\n\n')] # list of strings
        
        # if not part2:
        runPart1(notes)
        if part2:
            getTime()
            runPart2(notes)     

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
