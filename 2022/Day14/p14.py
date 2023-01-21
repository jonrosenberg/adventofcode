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
default_file = "Day14/input.txt"
part2 = True

T = TypeVar('T')
Location = Tuple[int, int]
forward = False

class Graph:
    def __init__(self) -> None:
        self.width = 1
        self.height = 1
        self.x_bounds = [500, 500]
        self.y_bounds = [0, 0]
        self.more_room: bool = True
        self.sand_counter: int = 0
        self.sand: list[Location] = []    
        self.walls: list[Location] = []
        self.falling: list[Location] = []

    
    def add_rock(self, rock:Location) -> bool:
        # check if this rock isn't already in the wall
        if not rock in self.walls:
            self.set_bounds(rock)
            #rock = (rock[0] - self.x_bounds[0], rock[1] - self.y_bounds[0])
            self.walls.append(rock)
            return True
        return False

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

    def passable(self, id: Location) -> bool:
        return id not in self.walls and id not in self.sand

    def step(self, id: Location) -> Location:
        (x, y) = id
        
        # down, down-left, down-right
        steps = [(x, y+1),(x-1,y+1),(x+1,y+1)]
        
        results = filter(self.passable, steps)
        results = [r for r in results]
        if len(results) != 0: return results[0]
        else: return id
    
    def __str__(self):
        return f"\n".join(self.sand)


# fill in line of rocks between two locations
def get_rock_wall(point_from: Location, point_to: Location) -> list[Location]:
    rock_wall = []
    (x1, y1) = point_from
    (x2, y2) = point_to
    # Check the x or y are the same between to locations
    if x1 != x2 and y1 != y2:
        print("Walls are not horizaontal or Vertical {} {}. Exiting...".format(point_from,point_to))
        sys.exit()
    elif x1 == x2 and y1 == y2:
        print("Wall points are the same {} {}. Exiting...".format(point_from,point_to))
        sys.exit()
    elif x1 != x2:
        if x2 < x1: x1,x2 = x2,x1 
        rock_wall = [(x,y1) for x in range(x1,x2+1)]
    elif y1 != y2:
        if y2 < y1: y1,y2 = y2,y1 
        rock_wall = [(x1,y) for y in range(y1,y2+1)]
    return rock_wall
   
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
    if 'depth' in style and id in graph.depths: r = f"{graph.depths[id]:2} "
    if id in graph.walls: r = "#"
    if id in graph.sand: r = "O"
    if id in graph.falling: r = "~"
    return r

def draw_grid(graph, **style):
    print(style.values())
    for t in style.values():
        if isinstance(t,tuple): pass

    
    print("_" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~" * graph.width)



def start_sand(graph: Graph, start: Location):

    
    sand_counter: int = 0
    
    while sand_counter == len(graph.sand):
        #time.sleep(0.2)
        #print(f"sand_counter:{sand_counter} == len(g):{len(graph.sand)}")
        #draw_grid(graph)
        
        sand = start
        
        landed: bool = False
        sand_counter += 1
        graph.falling = []
        
        while not landed:
            
            graph.falling.append(sand)
            current = sand
            sand = graph.step(current)
            
            #check if sand falls off wall
            if not graph.in_bounds(sand):
                landed = True
            #check if sand landed on wall
            if sand == current:
                if sand not in graph.sand: 
                    graph.sand.append(sand)
                    graph.sand_counter += 1
                landed = True
    return sand_counter

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
        if part2: 
            lines.append("200,174 -> 800,174")
            
        print(lines)
        g = Graph()

        # Add rocks for rock walls in lists
        wall_points = []
        for i, line in enumerate(lines):
            #= ast.literal_eval(
            wall_points.append([])
            for point_str in line.strip().split(" -> "):
                x,y = point_str.split(",")
                wall_points[i].append((int(x),int(y)))
        for w in wall_points:
            i = 0
            while i < len(w)-1:     
                wall_line = get_rock_wall(w[i],w[i+1])
                #print(f"{w[i]}->{w[i+1]}\n{wall_line}")
                
                for r in wall_line:
                    g.add_rock(r)
                    #print(f"g w:{g.width} h:{g.height} bounds:{g.x_bounds},{g.y_bounds} rock:{r}")
                    # draw_grid(g)
                    # time.sleep(0.07)
                i += 1
        
        print(g.walls)
        start = (500, 0)
        print("last grid")
        draw_grid(g, start=start)

        #sys.exit()
        start_sand(g,start)

        draw_grid(g,start=start)
        print(g.sand_counter)
        
        i = 0
        while i < 10:
            s = f"-- {i} --"
            sys.stdout.write("\r "+s+" <-")
            sys.stdout.flush()
            time.sleep(0.01)
            i += 1
        print()
        
        
      
if __name__ == '__main__':
    main()
