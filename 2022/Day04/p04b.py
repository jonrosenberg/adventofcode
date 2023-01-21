import pdb

import sys
import os

import re

def main():
    # get input file 
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    with open(filepath, 'r') as file:
        data = file.read() # string
        lines = data.split('\n') # list of strings
        
        total = 0
        
        for line in lines:
            # convert line to int ranges
            #pdb.set_trace()
            range1_start, range1_stop, range2_start, range2_stop = [int(x) for x in re.split("\D", line.strip())]

            range1_set = set(range(range1_start, range1_stop + 1))
            range2_set = set(range(range2_start, range2_stop + 1))
            #print(f"range1: {range1_set}; range2: {range2_set}; intersect:{range1_set & range2_set}")

            if len(range1_set & range2_set) > 0:
                #print("true")
                total += 1

            
            




        print(f"total: {total}")

if __name__ == '__main__':
    main()