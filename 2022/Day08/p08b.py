import pdb

import sys
import os

'''
30373 
25512 
65332 
33549 
35390 

[00] 3 s:1 m: 
[44]
'''

def main():
    # get input file 
    default_file = "Day8/input.txt"
    if len(sys.argv) < 2:
        filepath = default_file
    else:     
        filepath = sys.argv[1]
    print(f"~~~~~~~~~\n{filepath}\n~~~~~~~~")
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    
    with open(filepath,'r') as file:
        
        data = file.read() # string
        lines = data.split('\n') # list of strings
        

        maxscenic, p, up, down, left, right = 0, 0, 0, 0, 0, 0
        colsize = len(lines)
        rowsize = len(lines[0])
        while p < colsize:
            q = 0
            while q < rowsize:
                print(f"*** [{p}{q}]{lines[p][q]} ***")
                if p == 0 or q == 0 or p == colsize-1 or q == rowsize-1:
                    score = 0
                else:
                    #count_col(start_row_index,end_row_idx,start_col_idx,matrix,current_num)
                    up = count_col(p-1,-1,q,lines,lines[p][q])
                    down = count_col(p+1,colsize,q,lines,lines[p][q])
                    left = count_row(q-1,-1,p,lines,lines[p][q])
                    right = count_row(q+1,rowsize,p,lines,lines[p][q])
                    print(f"up:{up} * down:{down} * left:{left} * right:{right}")
                    
                score = up*down*left*right
                # if score >= 8000:
                #      pdb.set_trace()
                if maxscenic < score:
                    maxscenic = score 
                print(f"score:{score} max:{maxscenic}")
                
                q += 1
            p += 1

        print(maxscenic)
                    
def count_col(s,e,col,lines,height):
    print(f"col start:{s} end:{e} col:{col}")
    scorecount = 0
    step = 1
    if s > e:
        step = -1   
    for i in range(s,e,step):
        scorecount += 1
        print(f"[{i}{col}]{lines[i][col]}t{scorecount}")
        if lines[i][col] >= height:
            return scorecount
    return scorecount

def count_row(s,e,row,lines,height):
    print(f"row start:{s} end:{e} row:{row}")
    scorecount = 0
    step = 1
    if s > e:
        step = -1   
    for i in range(s,e,step):
        scorecount += 1
        print(f"[{row}{i}]{lines[row][i]}t{scorecount}")
        if lines[row][i] >= height:
            return scorecount
    return scorecount


if __name__ == '__main__':
    main()
