import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

start_time = time.time()
# get input file 
problemNum = 17
testRun = False
part2 = True

printing = False


default_file = f"Day{problemNum}/test.txt"

checkPointCount = 816
diffCount = 35 
diffHeight = 53

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"
    checkPointCount = 1522
    diffCount = 1750
    diffHeight = 2781

totalShapes = 2022

if part2:
    checkPointCount = 715
    if not testRun:
        checkPointCount = 2500
    totalShapes = 1000000000000
    

shapePoints = []
'''
####
'''
shapePoints.append( [(2,3),(3,3),(4,3),(5,3)] )
'''
.#.
###
.#.
'''
shapePoints.append( [(3,3),(2,4),(3,4),(4,4),(3,5)] )
'''
..#
..#
###
'''
shapePoints.append( [(2,3),(3,3),(4,3),(4,4),(4,5)] )
'''
#
#
#
#
'''
shapePoints.append( [(2,3),(2,4),(2,5),(2,6)] )
'''
##
##
'''
shapePoints.append( [(2,3),(3,3),(2,4),(3,4)] )

#Valve = TypeVar('Valve')

Point = Tuple[int, int]

class Shape:
    def __init__(self, points, height) -> None:
        self.shape: list[Point] = []

        for point in points:
            x,y = point
            self.shape.append((x,y+height))

class Grid:
    def __init__(self, gas:str) -> None:
        self.leftEdge: int = 0
        self.rightEdge: int = 7
        self.bottomEdge: int = 0
        self.heighestPoint: int = 0
        
        self.gasString: str = gas
        self.gasPointer: int = 0

        self.rocks: list[Point] = [(i,0) for i in range(7)]
        self.topRocks: list[int] = [0 for i in range(7)]
        
        # for drawing
        self.width = self.rightEdge - self.leftEdge
        self.height = self.heighestPoint
        self.shape = []
    
    def moveDown(self, shape:Shape) -> bool:
        for x,y in shape.shape:
            # if y-1 < self.topRocks[x]:
            #     pdb.set_trace()
            # if y-1 == self.topRocks[x]:
            if (x,y-1) in self.rocks:
                return False
        for i,point in enumerate(shape.shape):
            x,y = point
            shape.shape[i] = (x, y-1)
        return True
    
    def pushShape(self, shape:Shape) -> bool:
        currentGas = self.gasString[self.gasPointer]
        self.gasPointer =  (self.gasPointer + 1) % len(self.gasString)
        
        if currentGas == ">": 
            currentGas = 1
        elif currentGas == "<": 
            currentGas = -1
        
        for x,y in shape.shape:
            if x+currentGas < self.leftEdge or x+currentGas >= self.rightEdge:
                return False
            elif y <= self.heighestPoint and (x+currentGas,y) in self.rocks:
                return False
        for i,point in enumerate(shape.shape):
            x,y = point
            shape.shape[i] = (x+currentGas, y)
        return True
                
        
    def addRocks(self, shape:Shape) -> None:
        for x,y in shape.shape:
            # check if new heighest point
            if y > self.heighestPoint:
                self.heighestPoint = y
            if y > self.topRocks[x]:
                self.topRocks[x] = y
            if (x,y) not in self.rocks:
                self.rocks.append((x,y))
    
    def removeRocksBelow(self, shape:Shape) -> bool:
        yLevel = []
        
        for x,y in shape.shape:
            if y not in yLevel:
                yLevel.append(y)
        for y in yLevel:
            sealedBelow = True
            for x in range(self.rightEdge):
                if (x,y) not in self.rocks and (x,y-1) not in self.rocks:
                    sealedBelow = False
                    break
            if sealedBelow:
                if printing: print(f"seal found Reduce\n{len(self.rocks)} rocks to:")
                minY = y-1
                for x,y in self.rocks:
                    if y < minY:
                        self.rocks.remove((x,y))
                if printing: print(f"{len(self.rocks)} rocks")


    def sameTopRockShape(self,topRocks:list[int]) -> bool:
        delta = self.topRocks[0] - topRocks[0]
        for i,r in enumerate(topRocks):
            if r != self.topRocks[i] - delta:
                return False
        return True

    def sameRockShape(self,rocks:list[Point]) -> bool:
        delta = self.rocks[0][1] - rocks[0][1]
        for i,r in enumerate(rocks):
            x,y = self.rocks[i]
            if r != (x,y-delta):
                return False
        return True

        
def draw_tile(graph:Grid, id, style):
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
    if 'path' in style and id in style['path']:   r = "@"
    if 'start' in style and id == style['start']: r = "+"
    if 'goal' in style and id == style['goal']:   r = "Z"
    if id in graph.shape: r = "O"
    if id in graph.rocks: r = "#"
    return r

def draw_grid(graph:Grid, **style):
    graph.height = graph.heighestPoint + 6
    print(style.values())
    for t in style.values():
        if isinstance(t,tuple): pass

    print("_" * graph.width)
    for y in range(graph.height,0,-1):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~" * graph.width)



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

        grid = Grid(data.strip())

        shapeCount = 0
        prevCount = 0
        prevHeighest = 0

        checkPointTopRocks = []
        
        while shapeCount < totalShapes:
            if shapeCount % int(totalShapes / 1) == 0:
                getTime()
                print(shapeCount)
            if shapeCount == checkPointCount:
                checkPointTopRocks = grid.topRocks.copy()
                checkPointAllRocks = grid.rocks.copy()
                getTime()
                print(f"checkPoint {shapeCount} count:{shapeCount} height:{grid.heighestPoint}")
                prevCount = shapeCount
                prevHeighest = grid.heighestPoint
                totalHeightEstimate = grid.heighestPoint+int((totalShapes-checkPointCount)/diffCount)*diffHeight
                print(f"####### estimatedTotalHeight:{totalHeightEstimate} ############")
                if part2:
                    shapeCount = totalShapes
                #     print("debug")
                    
                #     printing = True
                #     pdb.set_trace()
            shapeType = shapePoints[shapeCount % len(shapePoints)]
            shapeCount += 1
            currentShape = Shape(shapeType, grid.heighestPoint+1)
            movedDown = True
            if printing:
                print(f"shapeCount:{shapeCount} grid.heighestPoint={grid.heighestPoint} ")
                print("start")
                grid.shape = currentShape.shape
                draw_grid(grid)
                print(currentShape.shape)
            while movedDown:
                
                grid.pushShape(currentShape)
                if printing: 
                    print("push")
                    grid.shape = currentShape.shape
                    print(currentShape.shape)
                    draw_grid(grid)
                # if shape hits bottom add rocks
                movedDown = grid.moveDown(currentShape)
                if printing:
                    print("fall")
                    grid.shape = currentShape.shape
                    print(currentShape.shape)
                    draw_grid(grid)
                if not movedDown:
                    grid.addRocks(currentShape)
                    grid.removeRocksBelow(currentShape)
                    
            if printing:
                print("end")
                print(grid.topRocks)
                print(f"grid.heighestPoint:{grid.heighestPoint} shapeCount:{shapeCount}")

            if len(checkPointTopRocks) != 0:
                
                if grid.sameTopRockShape(checkPointTopRocks):
                    #getTime()
                    #print(f"** SAME TOP ROCKS count:{shapeCount} height:{grid.heighestPoint} rocks {len(grid.rocks)}={len(checkPointAllRocks)} ")
                    if grid.sameRockShape(checkPointAllRocks):

                        getTime()
                        
                        print(f"!!!!!! SAME All ROCKS count:{shapeCount} height:{grid.heighestPoint} diffCount:{shapeCount-prevCount} diffHeight:{grid.heighestPoint-prevHeighest} ")
                        prevCount = shapeCount
                        prevHeighest = grid.heighestPoint
                        
                            

        print(f"grid.heighestPoint:{grid.heighestPoint} shapeCount:{shapeCount}")
        # create list 2d aarrays of shape
        # create a grid 2d array
        # 
        # until stopped by rock below
        #   move 1 side direction (if unblocked)
        #   move down one
        # 
def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
