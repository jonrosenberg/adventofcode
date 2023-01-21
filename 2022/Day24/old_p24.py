import sys
import os
import time

import re
import pdb

from typing import Protocol, Iterator, Tuple, TypeVar, Optional
from collections import deque

import copy

start_time = time.time()
# get input file 
problemNum = 24
testRun = True # for input 334 is to hight and 299 is too high
part2 = False

printing = True

maxWait = 5

default_file = f"Day{problemNum}/test.txt"

minCount = 100
if testRun == False:
    default_file = f"Day{problemNum}/input.txt"
    minCount = 337
#Valve = TypeVar('Valve')
Point = Tuple[int, int]

class Map:
    def __init__(self,lines) -> None:
        # Down, Up, Right, Left
        
                   
        
        #                           Down, Up, Right, Left
        self.blizMoves:list[Point] = [(0,1),(0,-1),(1,0),(-1,0)]
        #                          Left   Up    Wait  down  Right
        self.moves:list[Point] = [(-1,0),(0,-1),(0,0),(0,1),(1,0)]
        self.greedhMoves:list[Point] = [(1,0),(0,1),(0,0)]
        self.waiting:dict[Point,int] = {}
        blizl = [[],[],[],[]]
        bliz = set()
        for y,line in enumerate(lines[1:-1]): 
            for x,c in enumerate(line[1:-1]):
                if c != ".":
                    if c == 'v': 
                        blizl[0].append((x,y))
                        bliz.add((x,y,0,1))
                    elif c == '^': 
                        blizl[1].append((x,y))
                        bliz.add((x,y,0,-1))
                    elif c == '>': 
                        blizl[2].append((x,y))
                        bliz.add((x,y,1,0))
                    elif c == '<': 
                        blizl[3].append((x,y))
                        bliz.add((x,y,-1,0))
                    
                self.waiting[(x,y)] = 0
        self.width:int = len(line[1:-1])
        self.height:int = len(lines[1:-1])                
        self.bliz:list[list[Point]] = blizl
        self.bs: set(tuple(int,int,int,int)) = bliz
        self.allBliz = set(self.bliz[0]) | set(self.bliz[1]) | set(self.bliz[2]) | set(self.bliz[3])
        self.startBliz = copy.deepcopy(bliz)
        self.ignorePaths = set([])
        self.path = []

    def moveBlizard(self) -> None:
        for p,m in enumerate(self.blizMoves):
            for q,b in enumerate(self.bliz[p]):
                self.bliz[p][q] = ((b[0]+m[0])%self.width,(b[1]+m[1])%self.height)
                self.allBliz = set(self.bliz[0]) | set(self.bliz[1]) | set(self.bliz[2]) | set(self.bliz[3])
    
    def possibleMove(self,point) -> bool:
        # not out of bounds
        if 0 > point[0] or point[0] >= self.width or 0 > point[1] or point[1] >= self.height:
            if point != (0,-1): return False
        # not in blizzard
        if point in self.allBliz:
            return False
        if str(self.path + [point]) in self.ignorePaths:
            return False
        return True

    def draw(self, **style) -> None:
        #self.update(elfs)
        draw_grid(self, **style)

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
    if 'X' in style and id == style['X']:   r = "X"
    count = 0
    if id in graph.bliz[0]: 
        r = "v"
        count += 1
    if id in graph.bliz[1]:
        r = "^"
        count += 1
    if id in graph.bliz[2]:
        r = ">"
        count += 1
    if id in graph.bliz[3]:
        r = "<"
        count += 1
    if count > 1: r = count
    return r

def draw_grid(graph:Map, **style):
    
    print("_" * graph.width)
    for y in range(-1,graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~" * graph.width)

#def depthFirstSearch():


def runPart1(lines):
    print("Start Part 1")
    ### Parse Data
    m = Map(lines)
    
    #printing = testRun
    global minCount
    minCount = minCount
    winningPath = []
    #if printing: m.draw()
    start = (0,-1)
    goal = (m.width-1,m.height-1)
    # If hit goal
    # steps < less then goal
    #   ignore that path and try again
    #
    # if it gets stuck or fails
    #   ignore that path and try again
    # 
    changing = True
    while changing:
        m.bliz = copy.deepcopy(m.startBliz)
        current = start #start
        m.path = []
        if str(m.path) in m.ignorePaths:
            break
        count = 0
        frontier = deque([current])
        #Depth first search
        while len(frontier)>0:
            current = frontier.pop()
            m.path.append(current)
            if count > minCount \
                or count+(m.width-current[0])+(m.height-current[1]) > minCount:
                # add Path to ignore list
                if str(m.path) not in m.ignorePaths:
                    m.ignorePaths.add(str(m.path))
                    print(f"FAIL ig:{len(m.ignorePaths):4} p:{m.path}")
                    if len(m.path) == 1:
                        changing = False
                # else:
                #     if printing: print(f"FAIL NOCHANGE {len(m.path)} {len(m.ignorePaths)} print:{m.path}")
                #     changing = False
                break
            # made it to goal
            #if printing: m.draw(X=current)
            if current == goal:
                print(f"GOAL count:{count+1} pSize:{len(m.path)} ipSize{len(m.ignorePaths)} path:{m.path}")
                if str(m.path) not in m.ignorePaths:
                    m.ignorePaths.add(str(m.path))
                winningPath = m.path
                # New shortest path
                if count < minCount:
                    minCount = count
                    # TODO Prune paths of all greater then minCount
                break
            
            # move blizzards
            m.moveBlizard()
            m.bs = {((x+mx)%m.width, (y+my)%m.height) for x,y,mx,my in m.bs}
            # get neighbors
            noNeighbors = True
            for mx,my in m.moves:
                next = (current[0]+mx,current[1]+my)
                if m.possibleMove(next):
                    noNeighbors = False
                    frontier.append(next)
            if noNeighbors:
                if printing and count%10==0: print(f"noNeighbors {minCount} {count:2} {len(m.ignorePaths)} {m.path} ")
                if str(m.path) not in m.ignorePaths:
                    m.ignorePaths.add(str(m.path))
                if len(m.path) == 1:
                    changing = False
                break
            #if printing: print(f"Count:{count+1} pSize:{len(m.path)} ipSize{len(m.ignorePaths)} path:{m.path}")    
            count += 1

    # if printing:
    #     m.bliz = copy.deepcopy(m.startBliz)
    #     for ex in winningPath:
    #         m.draw(X=ex)
    #         m.moveBlizard()
        
    print(winningPath)
    print(f"Min Winning steps:{minCount+1} ")


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
        #runPart2(lines) 

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
    getTime()
