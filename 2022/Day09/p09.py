import pdb

import sys
import os

import re
'''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''

def main():
    # get input file 
    default_file = "Day9/input.txt"
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

        # get size of grid
        x_size, y_size, x_start, y_start, x_end, y_end = getArea(lines)
        print(f"x_size:{x_size} y_size:{y_size} x_start:{x_start} y_start:{y_start} x_end:{x_end} y_end:{y_end}")
        grid = [ [0]*y_size for i in range(x_size)]

        head = [x_start, y_start]
        tails = [[x_start, y_start] for i in range(9)]
        grid[x_start][y_start] = 1

        #print_grid(grid)

        # run through directions list, marking grid
        for line in lines:
            # do function
            [direction, num_steps] = line.strip().split(" ")

            for i in range(int(num_steps)):
                if direction == "R":
                    head[0] += 1
                elif direction == "L":
                    head[0] -= 1
                elif direction == "U":
                    head[1] += 1
                elif direction == "D":
                    head[1] -= 1

                tail_1 = follow(head, tails[0])
                i = 0
                while i < len(tails)-1:
                    tails[i+1] = follow(tails[i], tails[i+1])    
                    i+=1
                
                # mark tail coordinates in grid
                grid[tails[8][0]][tails[8][1]] = 1
            #print(line)
            #print_grid(grid)
        count = sum(sum(grid,[]))
        print(f"total points visited by tail: {count}")  
# test grid
def follow(head,tail):
    if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
        # move tail on x-axis
        if head[0] - tail[0] > 0:
            tail[0] += 1
        elif head[0] - tail[0] < 0:
            tail[0] -= 1
        
        # move tail on y-axis
        if head[1] - tail[1] > 0:
            tail[1] += 1
        elif head[1] - tail[1] < 0:
            tail[1] -= 1
    return tail

def print_grid(grid):
    for row in grid[::-1]:
        print(row)

def getArea(lines):
    i = 0
    x, y = 0, 0
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    for line in lines:
        [direction, num_steps] = line.strip().split(" ")
        if direction == "R":
            x += int(num_steps)
            x_max = max(x,x_max)
        if direction == "L":
            x -= int(num_steps)
            x_min = min(x,x_min)
        if direction == "U":
            y += int(num_steps)
            y_max = max(y,y_max)
        if direction == "D":
            y -= int(num_steps)
            y_min = min(y,y_min)
        x_size = x_max - x_min + 1
        y_size = y_max - y_min + 1
        x_start = 0 - x_min
        y_start = 0 - y_min
        x_end = x + x_start
        y_end = y + y_start
    return x_size, y_size, x_start, y_start, x_end, y_end

if __name__ == '__main__':
    main()
