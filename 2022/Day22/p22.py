import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

start_time = time.time()
# get input file 
problemNum = 22
testRun = False
# input.txt correct answer 76332
# input.txt 132032 your answer is too high
# input.txt wrap update 132096
#example 132096 -> 101004
part2 = True

printing = False

default_file = f"Day{problemNum}/test.txt"

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"

# if part2:
#     checkPointCount = 715
#     if not testRun:
#         checkPointCount = 2500
#     totalShapes = 1000000000000

#Valve = TypeVar('Valve')

Point = Tuple[int, int]

class Map:
    def __init__(self, lines) -> None:
        lines_grid = lines[:-2]
        walls, floor = [], []
        maxX = 0
        startX = re.search(r'[.#]', lines[0]).start() 
        xboarder: dict[Point,Point] = {}
        for y, line in enumerate(lines_grid):
            # Find x boarder
            xLeftB = (re.search(r'[.#]', line).start(),y)
            xRightB = (len(line)-1,y)
            xboarder[(xLeftB[0]-1,xLeftB[1])] = xRightB
            xboarder[(xRightB[0]+1,xRightB[1])] = xLeftB 
            # find max width   
            if len(line) > maxX: maxX = len(line)
            for x, c in enumerate(line):
                if c != " ": 
                    floor.append((x,y))    
                if c == "#": 
                    walls.append((x,y))
                
            
        self.trace: Trace = Trace(lines[-1],(startX,0))

        self.width:  int = maxX
        self.height: int = len(lines)-2
        self.floor: list[Point] = floor
        self.walls: list[Point] = walls  
        
        self.xboarder: dict[Point,Point] = xboarder
        getTime()
        print("parsed map")
        # self.yboarder: dict[Point,Point] = self.buildYBoarder()
        # getTime()
        # print("parsed parsed y boarder")

    def buildYBoarder(self) -> dict[Point,Point]:
        # find y boarder
        yBoarder = {}
        xTop=[None]*self.width
        for x,y in self.floor:
            if (x,y-1) not in self.floor:
                xTop[x]=(x,y)
            if (x,y+1) not in self.floor:
                yBoarder[(x,y+1)] = xTop[x]
                yBoarder[(xTop[x][0],xTop[x][1]-1)] = (x,y)
        return yBoarder
        
    def wrap(self,point:Point,facing:str) -> Point:

        if point in self.floor:
            return point
        elif (facing == ">" or facing == "<") and point in self.xboarder.keys():
            return self.xboarder[point]
        elif (facing == "^" or facing == "V") and point in self.yboarder.keys():
            return self.yboarder[point]
              

class Trace:
    def __init__(self,line,start:Point) -> None:
        self.here: Point = start
        self.directions: list[tuple[str,int]] = [ (found[0],int(found[1:])) for found in re.findall(r"[RL]\d+", "R"+line)]
        self.path: dict[Point,str] = {}
        self.path[start] = "S"
        self.facing: str = "^"
        self.moveList: list[str] = [">","V","<","^"]  
        self.move = { ">": lambda x, y: (x+1,y), 
                      "<": lambda x, y: (x-1,y), 
                      "^": lambda x, y: (x,y-1), 
                      "V": lambda x, y: (x,y+1) }
        dir = 3
        dir_step = [[0,1],[1,0],[0,-1],[-1,0]]
        # Point = map.ops[monkey.opStr](int1,int2)
    
    def fallowDirections(self,map:Map) -> None:
        if printing: draw_grid(map,path=self.path)
        if printing: print(self)
        getTime()
        print("start fallowing directions")
        for turn, steps in self.directions:
            if printing: print(f"steps:{steps} turn:{turn} ")
            self.turn(turn)  
            for i in range(steps): 
                x,y = self.here
                moved = self.move[self.facing](x,y)
                # if you hit wall: next direction
                if moved in map.walls:
                    break

                if moved not in map.floor:
                    moved = self.wrap(map,moved)
                # moved = map.wrap(moved,self.facing)
                self.path[moved] = self.facing
                
                self.here = moved
            
            # if printing: print(self)
        self.path[self.here] = "E"
        getTime()
        print("end fallowing directions")
        
    def wrap(self, map:Map, moved:Point) -> Point:
        
        self.turn("R")
        self.turn("R")
        while True:
            moved = self.step(moved)
            if moved not in map.floor:
                break
        self.turn("L")
        self.turn("L")
        moved = self.step(moved)
        return moved

    def turn(self, turn) -> None:
        if   turn == "R": self.facing = self.moveList[(self.moveList.index(self.facing) + 1) % len(self.moveList)]
        elif turn == "L": self.facing = self.moveList[(self.moveList.index(self.facing) - 1) % len(self.moveList)]

    def step(self,point) -> Point:
            
            return self.move[self.facing](point[0],point[1])

    def getPassword(self) -> int:
        col,row = self.here
        facing = self.moveList.index(self.facing)
        if printing: print(f"row:{row+1} + col:{col+1} + facint:{facing} ")
        return  (row+1)*1000 + (col+1)*4 + facing

    def __str__(self) -> str:
        return f"x,y:{self.here} {self.facing} "

     
def draw_tile(graph:Map, id, style):
    r = " "
    (x, y) = id
    
    if id in graph.floor: r = "."
    #if id in graph.xboarder.keys()   or id in graph.yboarder.keys()  : r = "*"
    #if id in graph.xboarder.values() or id in graph.yboarder.values(): r = ","
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
    
    if id in graph.walls: r = "#"
    return r

def draw_grid(graph:Map, **style):
    
    print("_" * graph.width)
    for y in range(-1,graph.height+1):
        for x in range(-1,graph.width+1):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~" * graph.width)

def runPart1(lines):
    print("Start Part 1")
    map = Map(lines)
    trace = map.trace
    trace.fallowDirections(map)
    if printing: draw_grid(map,path=trace.path)
    print("Finished Part 1")
    print(trace.getPassword())
    
    
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
