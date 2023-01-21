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
testRun = False
part2 = True


default_file = "Day15/test.txt"
y_test = 10


if part2 and not testRun: num = 4000000
elif part2 and testRun: num = 20

if testRun == False:
    default_file = "Day15/input.txt"
    y_test = 2000000

Location = Tuple[int, int]
forward = False

class Graph:
    def __init__(self) -> None:
        self.width = 1
        self.height = 1
        if part2:
            self.x_bounds, self.y_bounds = [0, num], [0, num]
        else:
            self.x_bounds, self.y_bounds = [0, 0], [0, 0]
   

        self.sensors: list[Location] = []
        self.distances: dict[Location, int] = {}
        self.beacons: dict[Location,Location] = []
        self.x_min_max: list[Location] = []
        self.x_mm: dict[Location,Location] = {}
        self.y_mm: dict[Location,Location] = {}


    def signal_distance(self,from_point:Location, to_point:Location) -> int:
        x1, y1 = from_point 
        x2, y2 = to_point
        x = abs(x2 - x1)
        y = abs(y2 - y1)
        # 1 = 1 + 0 or 0 + 1
        # 2 = 2 + 0 or 1 + 1
        # 3 = 2 + 1 or 2 + 1
        return x + y

    def mm_x_list(self,cm) -> bool:
        for i, mm in enumerate(self.x_min_max):
            if mm[0]-1 <= cm[0] <= mm[1]+1 or mm[0]-1 <= cm[1] <= mm[1]+1 \
                or cm[0]-1 <= mm[0] <= cm[1]+1 or cm[0]-1 <= mm[1] <= cm[1]+1:
                
                xx_min = min(cm[0],mm[0])
                xx_max = max(cm[1],mm[1])
                
                
                
                #self.x_min_max.remove(mm)
                #if (xx_min,xx_max) not in self.x_min_max:
                #    self.x_min_max.append((xx_min,xx_max))
                if part2 and xx_min == 0 and xx_max == num:
                    self.x_min_max = [(0,num)]
                    # print(self.x_min_max)
                    return True
                else:
                    # print()
                    # print(self.x_min_max)
                    self.x_min_max[i] = (xx_min,xx_max)
                    # print(f"{mm} :: {cm[0]},{cm[1]} -> {xx_min},{xx_max}")
                    # print(self.x_min_max)
                
            elif cm not in self.x_min_max:
                self.x_min_max.append(cm)
                # print(self.x_min_max)
        return False

    # find first point that in area that doesn't have a signal
    def gap_coverage(self) -> Location:
        #print(self.sensors)
        #print(self.distances)
        #print(self.y_mm)
        # 
        for row in range(num):
            
            i = 0
            covered = False
            self.x_min_max = []
            while not covered and i < len(self.sensors):
                
                s = self.sensors[i]
                sd = self.distances[s]
                y_min = self.y_mm[s][0]
                d = sd - abs(row-sd-y_min)
                # print(f"i:{0} s:{s} y_min:{y_min} sd:{sd} d:{d}\nmin-max:{self.x_min_max}")
                
                if self.y_mm[s][0] <= row <= self.y_mm[s][1]:
                    x_min = s[0] - d
                    x_max = s[0] + d
                    if x_min < 0: x_min = 0
                    if x_max > num: x_max = num
                    cm = (x_min,x_max)
                    covered = x_min == 0 and x_max == num
                    if not covered:
                        if len(self.x_min_max) == 0: self.x_min_max.append(cm)
                        else:
                        #    print("start mm_x_list")
                           covered = self.mm_x_list(cm)               
                i += 1
            if not covered and len(self.x_min_max)>1:
                for cm in self.x_min_max:
                    covered = self.mm_x_list(cm)
                    if covered:
                        break
            if not covered:
                results = []
                for cm in self.x_min_max:
                    if cm not in results: results.append(cm)
                if results[0][0] == 0:
                    col = 0 + results[0][1]+1
                else: 
                    col = results[0][0] - 1
                print(f"####### FOUND {row},{col} #######")
                print(self.x_min_max)
                return (col,row)
                
        return None

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
        
        
        d = distance - abs(y_test - y_min - distance)
        x_min = x - d
        x_max = x + d
        cm = (x_min,x_max)
        cy = y_test
        if cy == y_test:
            # is x in 
            # if any exist_min or exit_max next, equal or between cur_min and cur_max
            if len(self.x_min_max) == 0: self.x_min_max.append(cm)
            else: 
                self.mm_x_list(cm)
                print(f"***** 1st round {cy} ****")

        

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

def main():
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
        g = Graph()
        
        #parse string data
        for line in lines:
            line_s, line_b = line.split(": closest beacon is at x=")
            
            #Add beacon location and set bounds
            line_bx, line_by = line_b.strip().split(", y=")
            beacon = (int(line_bx),int(line_by))
            if beacon not in g.beacons:
                if not part2: g.set_bounds(beacon)
                g.beacons.append(beacon)
            
            #Add sensor location and set bounds
            line_sx, line_sy = line_s[12:].split(", y=")
            sensor = (int(line_sx),int(line_sy))
            if sensor not in g.sensors:
                if not part2: g.set_bounds(sensor)
                else: 
                    g.distances[sensor] = g.signal_distance(sensor,beacon)
                    y_min = sensor[1] - g.distances[sensor]
                    y_max = sensor[1] + g.distances[sensor]
                    g.y_mm[sensor] = (y_min, y_max)
                    x_min = sensor[0] - g.distances[sensor]
                    x_max = sensor[0] + g.distances[sensor]
                    g.x_mm[sensor] = (x_min, x_max)
                g.sensors.append(sensor)
                
            if not part2: g.signal_coverage(sensor,beacon)
        print(g.x_min_max)
        if not part2:
            for mm in g.x_min_max:
                print(f"***** {mm} ****")
                g.mm_x_list(mm)
                
            results = []
            for mm in g.x_min_max:
                if mm not in results:
                    results.append(mm)
            count = 0
            for x1,x2 in results:
                count += x2-x1
            print(count)
        else: 
            point = g.gap_coverage()
            result = point[0] * 4000000 + point[1]
            print(result)

        
        
        
        
        
      
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
