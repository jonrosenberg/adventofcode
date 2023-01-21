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
        cycle = 1
        x = 1
        check_cycles = [20,60,100,140,180,220]
        signal_strengths = dict() 
        signal_total = 0

        # run through directions list, marking grid
        for line in lines:
            
            if cycle in check_cycles:
                signal_strengths[cycle] = x * cycle
                print(f"cycle:{cycle} * x:{x} = {x * cycle}")
                
                # if cycle == 220: 
                #     print(f"*** cycle={cycle} x={x} lines[134]={line} ***")
                #     pdb.set_trace() # cycle= 220 x=19 line 134 noop
                    

            if line.strip() == "noop":
                cycle += 1
                
            elif line[:4] == "addx":
                [command, num] = line.strip().split(" ")
                if cycle+1 in check_cycles:
                    signal_strengths[cycle+1] = x * (cycle+1)
                    print(f"cycle:{cycle+1} * x:{x} = {x * (cycle+1)}")
                    
                    # if cycle+1 == 180: 
                    #     pdb.set_trace() # cycle=179 x=16 line 110
                    #     print(f"*** cycle={cycle} x={x} lines[110]={line} ***")
                cycle +=2
                x += int(num)
                #print(f"{cycle} {line} = {x}")
                
            
        print(signal_strengths)
        signal_total = sum(signal_strengths.values())
        print(f"total signal strength: {signal_total}")  
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
