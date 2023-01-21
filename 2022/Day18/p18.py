import pdb

import sys
import os
import time

import re

import bisect 

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

start_time = time.time()
# get input file 
problemNum = 18
testRun = False
part2 = True

printing = False


default_file = f"Day{problemNum}/test.txt"

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"
    

minCube = [100,100,100]
maxCube = [0,0,0]

 
# if part2:
#     checkPointCount = 715
#     if not testRun:
#         checkPointCount = 2500
#     totalShapes = 1000000000000

#Valve = TypeVar('Valve')

Cube = Tuple[int, int, int]

def getAirNeighbors(cubes:list[Cube],cube:Cube) -> list[Cube]:
    neighbors = []
    air = []

    neighbors.append((cube[0]+1,cube[1],cube[2]))
    neighbors.append((cube[0]-1,cube[1],cube[2]))
    neighbors.append((cube[0],cube[1]+1,cube[2]))
    neighbors.append((cube[0],cube[1]-1,cube[2]))
    neighbors.append((cube[0],cube[1],cube[2]+1))
    neighbors.append((cube[0],cube[1],cube[2]-1))
    for n in neighbors:
        if n not in cubes:
            air.append(n)
    return air

def getBubble(cubes:list[Cube],cube:Cube,airBubbles:list[Cube]) -> list[Cube]:
    queue = [cube]
    visited = [cube]
    if cube in airBubbles:
        bubble = []
    else:
        bubble = [cube]
    
    count = 0
    while len(queue)>0:
        cube = queue.pop()
        neighbors = getAirNeighbors(cubes,cube)
        # only keep neighbors that are air (empty)
        air = []
        #if printing:
        #    print(neighbors)
        for n in neighbors:
            if n not in visited and n not in airBubbles:
                air.append(n)
                visited.append(n) 
        # add air that doesn't reach out of cube
        for n in air:
            
            for i,p in enumerate(n):
                # not a bubble
                if p <= minCube[i] or p >= maxCube[i]:
                    return []
            if n not in cubes:  
                queue.append(n)
                bubble.append(n)
                
    # if len(bubble) > 0:
    #     print("queue")
    #     print(bubble)

    return bubble
        

def numCubesTouches(cubes:list[Cube],cube:Cube) -> int:
    touches = 0
    if (cube[0]+1,cube[1],cube[2]) in cubes: touches += 1
    if (cube[0]-1,cube[1],cube[2]) in cubes: touches += 1
    if (cube[0],cube[1]+1,cube[2]) in cubes: touches += 1
    if (cube[0],cube[1]-1,cube[2]) in cubes: touches += 1
    if (cube[0],cube[1],cube[2]+1) in cubes: touches += 1
    if (cube[0],cube[1],cube[2]-1) in cubes: touches += 1
    return touches

def main():
    global printing
    global minCube
    global maxCube

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

        cubes = []
        airBubbles = []
        surfaceArea = 0
        exteriorSurfaceArea = 0
        for line in lines:
            x,y,z = line.strip().split(",")
            cube = (int(x),int(y),int(z))
            if part2:
                for i,p in enumerate(cube):
                    if minCube[i] > p: minCube[i] = p
                    if maxCube[i] < p: maxCube[i] = p
            bisect.insort(cubes, cube)
            
            surfaceArea += 6
            numTouches = numCubesTouches(cubes,cube)
            surfaceArea -= numTouches*2

        print(minCube)
        print(maxCube)
        print(surfaceArea)
        exteriorSurfaceArea = surfaceArea
        for cube in cubes:
            if part2:
                if cube == (2,1,5):
                    printing = True
                    #pdb.set_trace()
                else: 
                    printing = False
                airNeighbors = getAirNeighbors(cubes,cube)
                for airN in airNeighbors:
                    bubble = getBubble(cubes,airN,airBubbles)
                    if len(bubble) != 0:
                        print("bubble")
                        print(len(bubble))
                        for bub in bubble:
                            if bub not in airBubbles:
                                airBubbles.append(bub)
        
                # is airbubble by checking empty neighbors dont lead to any min or max coordinates
                # get airbubble cubes and subtract any surfaces that airbubble touches
        print(f"bubbles:{len(airBubbles)}") 
        
        for ab in airBubbles:
            numWalls = numCubesTouches(cubes,ab)
            exteriorSurfaceArea -= numWalls
        print(exteriorSurfaceArea)

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
