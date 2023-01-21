import sys
import os
import time

import re
import pdb

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

start_time = time.time()
# get input file 
problemNum = 23
testRun = False
part2 = True

printing = False

default_file = f"Day{problemNum}/test.txt"

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"

#Valve = TypeVar('Valve')
Point = Tuple[int, int]

class Map:
    def __init__(self) -> None:
        self.elfs = []

    def update(self, elfs:list[Point]) -> None:
        xMin, yMin, xMax, yMax = elfs[0][0],elfs[0][0],elfs[0][1],elfs[0][1]
        self.elfs:list[Point] = elfs
        for x,y in elfs:
            if x < xMin: xMin = x
            elif x > xMax: xMax = x
            if y < yMin: yMin = y
            elif y > yMax: yMax = y
        self.xMin:int = xMin
        self.yMin:int = yMin
        self.xMax:int = xMax
        self.yMax:int = yMax
        self.width:int = xMax-xMin
        self.height:int = yMax-yMin

    def draw(self,elfs:list[Point]) -> None:
        self.update(elfs)
        draw_grid(self)

    def __str__(self) -> str:
        return f"x,y:{self.here} {self.facing} "

     
def draw_tile(graph:Map, id, style):
    r = "."
    (x, y) = id
    
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = ">"
        if x2 == x1 - 1: r = "<"
        if y2 == y1 + 1: r = "v"
        if y2 == y1 - 1: r = "^"
    if 'path' in style and id in style['path'].keys():   r = style['path'][id]
    if 'trace' in style and id == style['trace']: r = "+"
    if 'goal' in style and id == style['goal']:   r = "Z"
    
    if id in graph.elfs: r = "#"
    return r

def draw_grid(graph:Map, **style):
    
    print("_" * graph.width)
    for y in range(graph.yMin,graph.yMax+1):
        for x in range(graph.xMin,graph.xMax+1):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~" * graph.width)

def runPart1(lines):
    print("Start Part 1")
    ### Parse Data
    elfs = []
    map = Map()
    for y,line in enumerate(lines): 
        for x,c in enumerate(line):
            if c=="#": elfs.append( (x,y) )
    
    
    if printing: map.draw(elfs)
    # Directions [N,S,W,E]
    dir  = [[(0,-1),(-1,-1),(1,-1)], # North, NW, NE
            [(0,1),(-1,1),(1,1)],    # South, SW,SE
            [(-1,0),(-1,-1),(-1,1)], # West, NW, SW
            [(1,0),(1,-1),(1,1)]]    # East, NE, SE
    
    ## Start Rounds 10 rounds
    for r in range(100000000):
        print(r)
        moves = {}
        stopMove = []
        for i,elf in enumerate(elfs):
            x,y=elf
            hasNeighbor = False
            # LOOK part: No elfs around, don't move
            for lx,ly in set(dir[0]+dir[1]+dir[2]+dir[3]):
                if (x+lx,y+ly) in elfs:
                    hasNeighbor = True
                    neighbor = (x+lx,y+ly)
                    break
            if not hasNeighbor:    
                moves[(x,y)] = ((x,y))
            # look directions
            if i+1 != len(moves):
                # looks in order N/S/W/E
                for l in range(4):
                    li = (r+l)%4
                    move = (dir[li][0][0]+x,dir[li][0][1]+y)
                    movedir = [(dir[li][1][0]+x,dir[li][1][1]+y),(dir[li][2][0]+x,dir[li][2][1]+y)]
                    #move = tuple([sum(tup) for tup in zip(dir[li][0],(x,y))])
                    if neighbor in movedir:
                        continue
                    if  move not in elfs \
                    and movedir[1] not in elfs \
                    and movedir[2] not in elfs:
                        if move not in moves.values():
                            moves[(x,y)] = move
                        else:
                            stopMove.append(move)
                            moves[(x,y)] = (x,y) 
                        break
            # no where to go was found
            if i+1 != len(moves):
                moves[(x,y)] = ((x,y))
        # end rounds if no more movement      
        if list(moves.keys()) == list(moves.values()):
            print(f"No more moves on ROUND {r+1}")
            break

        # MOVE part: if more then one elf is in a destined position then no elf moves
        for i, elf in enumerate(elfs):
            # move elf if not jumping on same space
            if moves[elf] not in stopMove:
                elfs[i] = moves[elf]
                
        if printing: 
            print(f"ROUND {r+1}")
            map.draw(elfs)
    # Calculate bounds
    xMin, yMin, xMax, yMax = elfs[0][0],elfs[0][0],elfs[0][1],elfs[0][1]
    for x,y in elfs:
        if x < xMin: xMin = x
        elif x > xMax: xMax = x
        if y < yMin: yMin = y
        elif y > yMax: yMax = y



    count = 0
    for x in range(xMin,xMax+1):
        for y in range (yMin,yMax+1):
            if (x,y) not in elfs:
                count += 1

    print(count)
    #map.draw(elfs)

    #
    #if printing: draw_grid(map,path=trace.path)
    print("Finished Part 1")
    #print(trace.getPassword())
    
    
def runPart2(lines):
    print("Start Part 2")
    print("Finished Part 2")

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
        
        runPart1(lines)
        runPart2(lines) 

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
