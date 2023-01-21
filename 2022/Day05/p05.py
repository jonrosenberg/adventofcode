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
 1   2   3   4   5   6   7   8   9 
 
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
        stck = []
        if filepath == "test.txt":
            # test
            stck.append(list("ZN"))
            stck.append(list("MCD"))
            stck.append(list("P"))
        elif filepath == "input.txt":
            # input
            stck.append(list("LNWTD"))
            stck.append(list("CPH"))
            stck.append(list("WPHNDGMJ"))
            stck.append(list("CWSNTQL"))
            stck.append(list("PHCN"))
            stck.append(list("THNDMWQB"))
            stck.append(list("MBRJGSL"))
            stck.append(list("ZNWGVBRT"))
            stck.append(list("WGDNPL"))
        else:
             print("File path {} does not exist. Exiting...".format(filepath))
             sys.exit()

        data = file.read() # string
        lines = data.split('\n') # list of strings
        
        for line in lines:
        
            
            # convert line to int ranges
            #pdb.set_trace()
            create_num, stack_from, stack_to = [int(x) for x in re.findall("\d+", line.strip())]
            stack_from -= 1
            stack_to -= 1
            
            i = 0
            print(line)
            print(f"1:{stck}")
            while i < create_num:
                stck[stack_to].append(stck[stack_from].pop())
                i += 1
            print(f"2:{stck}")
        top_creates = ""

        for s in stck:
            top_creates += s[-1]
        
        print(f"\n*** top_creates: {top_creates}")

if __name__ == '__main__':
    main()