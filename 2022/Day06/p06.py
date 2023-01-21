import pdb

import sys
import os

import re
'''
----- Test -------
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
 ----- Input -------
        [J]         [B]     [T]    
        [M] [L]     [Q] [L] [R]    
        [G] [Q]     [W] [S] [B] [L]
[D]     [D] [T]     [M] [G] [V] [P]
[T]     [N] [N] [N] [D] [J] [G] [N]
[W] [H] [H] [S] [C] [N] [R] [W] [D]
[N] [P] [P] [W] [H] [H] [B] [N] [G]
[L] [C] [W] [C] [P] [T] [M] [Z] [W]
 1   2   3   start_marker   5   6   7   8   9 
 
LNWTD
CPH
WPHNDGMJ
CWSNTQL
PHCN
THNDMWQB
MBRJGSL
ZNWGVBRT
WGDNPL 
'''
def main():
    # get input file 
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    with open(filepath, 'r') as file:
        
        data = file.read() # string
        lines = data.split('\n') # list of strings
        
        for line in lines: 
            #pdb.set_trace()
            print(line)
            start_marker = 14
            #x= re.search("/(?:([A-Za-z])(?!.*\1)){start_marker}", line)
            i = 0
            while i < len(line)-start_marker:
                if len(set(line[i:i+start_marker])) == start_marker:
                    break
                else:
                    i += 1
            print(f"str:{line[i:i+start_marker]} end:{i+start_marker}")
            

if __name__ == '__main__':
    main()