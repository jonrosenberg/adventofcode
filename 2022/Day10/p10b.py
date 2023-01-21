import pdb

import sys
import os

import re
'''
addx V takes 2 cycles
noop takes 1 cycle
'''

def main():
    # get input file 
    default_file = "Day10/input.txt"
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

        # initialize counter
        cycle = 0
        x = 1
        crt = ["","","","","","",""]
        signal_total = 0
        
        print_sprite(x)
        
        # run through directions list, marking grid
        for line in lines:
            print(line)

            if line.strip() == "noop":
                
                crt_cycle(x,cycle,crt)
                pp(cycle,x,crt,line)
                cycle += 1
                
            elif line[:4] == "addx":
                [command, num] = line.strip().split(" ")
                print(f"c:{command} num:{int(num)}")
                crt_cycle(x,cycle,crt)
                pp(cycle,x,crt,line)
                cycle += 1
                crt_cycle(x,cycle,crt)
                pp(cycle,x,crt,line)
                #if cycle > 6: pdb.set_trace()
                cycle += 1
                x += int(num)
                #print_sprite(x)
                
                
                #print(f"{cycle} {line} = {x}")
            
            #if cycle > 5: sys.exit()
            
        print(f"total signal strength: {signal_total}")  

def crt_cycle(x,cycle,crt):
    cycle_x = cycle % 40
    cycle_i = int(cycle / 40)
    if cycle_i >= 6: 
        cycle_i = 6
    min_sprite = x-1
    max_sprite = x+1
    if cycle_x < min_sprite or cycle_x > max_sprite:
        crt[cycle_i] += '.'
    else:
        crt[cycle_i] += '#'
    #for line in crt:
    #    if len(line) > 0: print(line)
    return crt

def pp(cycle,x,crt,line):
    sprite = '.' * (x-1) + "###"
    print(f"During cycle {cycle:4}: {line}")
    print(f"During sprite {x:3}: {sprite}")
    for c in crt:
        if len(c) > 0: print(f"len:{len(c):3} pos:{int(cycle / 40):2}:{cycle % 40:2}: {c}")
            

def print_sprite(x):
    print('.' * (x-1) + "###")

'''
x = 16
addx -9 = 7
addx 18 = 
addx 1
addx 2
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop 
'''
if __name__ == '__main__':
    main()
