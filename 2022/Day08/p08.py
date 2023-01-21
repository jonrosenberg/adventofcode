import pdb

import sys
import os

import re
'''
30373 5 r5  5 
25512 2 r2  4
65332 2 r2  4
33549 2 r1  3
35390 5 r5  5
wwwww
52225
 120

21
'''

def main():
    
    # get input file 
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    
    with open(filepath,'r') as file:
        
        data = file.read() # string
        lines = data.split('\n') # list of strings
        

        count = 0
        p = 0
        colsize = len(lines)
        rowsize = len(lines[0])
        while p < colsize:
            q = 0
            while q < rowsize:
                v = 'O'
                if p == 0 or q == 0 or p == colsize-1 or q == rowsize-1:
                    v = 'X'
                    count += 1
                elif visible_row(lines,p,q) or visible_col(lines,p,q):
                    v = 'X'
                    count += 1
                q += 1
            p += 1
        print(count)
                    

def visible_row(lines,p,q):
    maxleft = max([int(x) for x in lines[p][:q]]) 
    if maxleft < int(lines[p][q]):
        return True
    maxright = max([int(x) for x in lines[p][q+1:]])
    if maxright < int(lines[p][q]):
        return True
    return False

def visible_col(lines,p,q):
    i = 0
    m = 0
    while i < len(lines):
        if i == p:
            if m < int(lines[p][q]):
                return True
            m = 0
        elif m < int(lines[i][q]):
            m = int(lines[i][q])
        
        if i == len(lines)-1 and m < int(lines[p][q]):
            return True
        i += 1
    return False

if __name__ == '__main__':
    main()
