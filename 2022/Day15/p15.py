import pdb

import sys
import os
import time

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

#import ast

'''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
# get input file 
default_file = "Day15/test.txt"
real_file = True
y_test = 10

if real_file == True:
    default_file = "Day15/input.txt"
    y_test = 2000000
part2 = False



T = TypeVar('T')
Location = Tuple[int, int]
forward = False

class Graph:
    def __init__(self) -> None:
        self.width = 1
        self.height = 1
        self.x_bounds = [0, 0]
        self.y_bounds = [0, 0]

        self.sensors: dict[Location, Location] = {}
        self.beacons: list[Location] = []
        self.coverage: dict[int,list[Location]] = []
        self.x_min_max: list[Location] = []
        self.y_min_max: list[Location] = []


    def signal_distance(self,from_point:Location, to_point:Location) -> int:
        x1, y1 = from_point 
        x2, y2 = to_point
        x = abs(x2 - x1)
        y = abs(y2 - y1)
        # 1 = 1 + 0 or 0 + 1
        # 2 = 2 + 0 or 1 + 1
        # 3 = 2 + 1 or 2 + 1
        return x + y

    def mm_x_list(self,cm):
        for i, mm in enumerate(self.x_min_max):
            if mm[0]-1 <= cm[0] <= mm[1]+1 or mm[0]-1 <= cm[1] <= mm[1]+1 \
                or cm[0]-1 <= mm[0] <= cm[1]+1 or cm[0]-1 <= mm[1] <= cm[1]+1:
                
                print()
                xx_min = min(cm[0],mm[0])
                xx_max = max(cm[1],mm[1])
                
                print(self.x_min_max)
                
                #self.x_min_max.remove(mm)
                #if (xx_min,xx_max) not in self.x_min_max:
                #    self.x_min_max.append((xx_min,xx_max))
                self.x_min_max[i] = (xx_min,xx_max)
                print(f"{mm} :: {cm[0]},{cm[1]} -> {xx_min},{xx_max}")
                print(self.x_min_max)
                
            elif cm not in self.x_min_max:
                self.x_min_max.append(cm)
                print(self.x_min_max)
                
    def signal_coverage(self, sensor: Location, beacon: Location):
        distance = self.signal_distance(sensor,beacon)
        x, y = sensor
        y_min = y - distance
        y_max = y + distance
        x_min = x - distance
        x_max = x + distance
        
    
        #  i = d*2+1  d       i   d           i   d
        #  0    1   x:2 - abs(0 - 2) = 0  y:-(0 - 2)  2
        #  1   123  x:2 - abs(1 - 2) = 1  y:-(1 - 2)  1
        #  2  12345 x:2 - abs(2 - 2) = 2  y:-(2 - 2)  0
        #  3   123  x:2 - abs(3 - 2) = 1  y:-(3 - 2) -1
        #  4    1   x:2 - abs(4 - 2) = 0  y:-(4 - 2) -2
        

        for i, cy in enumerate(range(y_min,y_max+1)):
            d = distance - abs(i - distance)
            x_min = x - d
            x_max = x + d
            cm = (x_min,x_max)
            if cy == y_test:
                # is x in 
                # if any exist_min or exit_max next, equal or between cur_min and cur_max
                if len(self.x_min_max) == 0: self.x_min_max.append(cm)
                else: 
                    self.mm_x_list(cm)
                    print(f"***** 1st round {cy} ****")
                #print(f"{x},{y} -> {x_min} - {x_max+1}")
                # for cx in range(x_min,x_max+1):
                #     #
                #     #
                #     #
                #     if (cx,cy) not in self.coverage:
                #         #self.set_bounds((cx,cy))  
                #         self.coverage.append((cx,cy))
                # #print(f"complete")
        
        

    def set_bounds(self, rock):
        # Check min x 
        if   rock[0] < self.x_bounds[0]: 
            self.x_bounds[0] = rock[0]
        # Check max X 
        elif rock[0] > self.x_bounds[1]: 
            self.x_bounds[1] = rock[0]
        self.width = self.x_bounds[1] - self.x_bounds[0] +1
        
        # Check min Y 
        if   rock[1] < self.y_bounds[0]: 
            self.x_bounds[0] = rock[1]
        # Check max Y 
        elif rock[1] > self.y_bounds[1]: 
            self.y_bounds[1] = rock[1]
        self.height = self.y_bounds[1] - self.y_bounds[0] +1
        
    def in_bounds(self, id: Location) -> bool:
        (x, y) = id
        return 0 + self.x_bounds[0] <= x < self.width + self.x_bounds[1] and 0 + self.y_bounds[0] <= y < self.height + self.y_bounds[1]
    
    def __str__(self):
        return f"\n".join(self.sand)

   
def draw_tile(graph:Graph, id, style):
    r = "."
    (x, y) = id
    id = (x+graph.x_bounds[0], y+graph.y_bounds[0])
    
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
    if id in graph.coverage: r = "#"
    if id in graph.sensors: r = "S"
    if id in graph.beacons: r = "B"
    return r

def draw_grid(graph, **style):
    print(style.values())
    for t in style.values():
        if isinstance(t,tuple): pass

    
    print("_" * graph.width)
    for y in range(graph.height):
        s = ""
        for x in range(graph.width):
            s+=str("%s" % draw_tile(graph, (x, y), style))
        print(f"{y:2}: {s}")
    print("~" * graph.width + "~~~~~")





def main():
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
        g = Graph()
        
        #parse string data
        for line in lines:
            line_s, line_b = line.split(": closest beacon is at x=")
            
            #Add beacon location and set bounds
            line_bx, line_by = line_b.strip().split(", y=")
            beacon = (int(line_bx),int(line_by))
            if beacon not in g.beacons:
                g.set_bounds(beacon)
                g.beacons.append(beacon)
            
            #Add sensor location and set bounds
            line_sx, line_sy = line_s[12:].split(", y=")
            sensor = (int(line_sx),int(line_sy))
            if sensor not in g.sensors.keys():
                g.set_bounds(sensor)
                g.sensors[sensor]=beacon
                #pdb.set_trace()
            g.signal_coverage(sensor,beacon)
        print(g.x_min_max)
        for mm in g.x_min_max:
            print(f"***** {mm} ****")
            g.mm_x_list(mm)
            
        results = []
        for mm in g.x_min_max:
            if mm not in results:
                results.append(mm)
        #draw_grid(g)
        print(len(g.coverage))
        #count_coverage
        count = 0
        for x1,x2 in results:
            count += x2-x1
        print(count)
        
        
        
        
      
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
