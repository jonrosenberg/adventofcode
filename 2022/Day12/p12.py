import pdb

import sys
import os

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

'''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
T = TypeVar('T')
Location = Tuple[int, int]
forward = False

class Graph:
    def __init__(self, lines, f= True) -> None:
        self.width = len(lines[0])
        self.height = len(lines)
        self.values: list[str] = lines    
        self.depths: dict[Location, int] = {}
        for y, line in enumerate(lines):
            for x, n in enumerate(line):
                if n == "S": n = "a"
                if n == "E": n = "z"
                self.depths[(x,y)] = ord(n)-96
        self.weights: dict[Location, float] = {}
                
    def get_index(self, key = "S") -> Location:
        for y,line in enumerate(self.values):
            for x,i in enumerate(line):
                if i == key: return (x,y)
        return None

    def in_bounds(self, id: Location) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable_to_end(self, from_node: Location, to_node: Location) -> bool:
        return (self.depths[from_node] - self.depths[to_node]) > -2 

    def passable_to_start(self, from_node: Location, to_node: Location) -> bool:
        return (self.depths[from_node] - self.depths[to_node]) < 2 

    def depth(self, from_node: Location, to_node: Location) -> int:
        return self.depths.get(to_node, 1)

    def cost(self, from_node: Location, to_node: Location) -> float:
        return self.weights.get(to_node, 1)

    def neighbors(self, id: Location) -> Iterator[Location]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        n = filter(self.in_bounds, neighbors)
        results = []
        for loc in n:
            if forward and self.passable_to_end(id,loc):
                results.append(loc)
            if (not forward) and self.passable_to_start(id,loc):
                results.append(loc)

        return results
    
    def __str__(self):

        return f"\n".join(self.values)




#Location = TypeVar('Location')





import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: T):
        self.elements.append(x)
    
    def get(self) -> T:
        return self.elements.popleft()

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    if 'goal' in style and id == style['goal']:   r = " Z "
    if 'depth' in style and id in graph.depths: r = f"{graph.depths[id]:2} "
    return r


def draw_grid(graph, **style):
    #pdb.set_trace()
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)

def reconstruct_path(came_from: dict[Location, Location], start: Location, goal: Location) -> list[Location]:

    current: Location = goal
    path: list[Location] = []
    if goal not in came_from: # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def breadth_first_search(graph: Graph, start: Location, goal: Location = None):
    
    # print out what we find
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if goal != None and current == goal or (not forward and graph.depths[current] == 1): # early exit
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
                
    
    return came_from

def dijkstra_search(graph: Graph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal or (not forward and graph.depths[current] == 1):
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

def heuristic(a: Location, b: Location) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph: Graph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal or (not forward and graph.depths[current] == 1):
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far

def main():
    # get input file 
    default_file = "Day12/test.txt"
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
        
        graph = Graph(lines)
        if forward:
            goal = graph.get_index("E")
            start = graph.get_index("S")
        else:
            goal = graph.get_index("S")
            start = graph.get_index("E")

        print(graph)

        parents = breadth_first_search(graph,start,goal)
        
        print(start)
        print(goal)
        print("*************** Breadth *******************")
        
        draw_grid(graph, point_to=parents, start=start, goal=goal)
        draw_grid(graph, point_to=parents, start=start, depth=True)
        
        print("*************** dijkstra *******************")
        
        came_from, cost_so_far = dijkstra_search(graph, start, goal)
        draw_grid(graph, point_to=came_from, start=start, goal=goal)

        draw_grid(graph, path=reconstruct_path(came_from, start=start, goal=goal))

        draw_grid(graph, number=cost_so_far, start=start, goal=goal)
        print("*************** A Star *******************")
        came_from, cost_so_far = a_star_search(graph, start, goal)
        draw_grid(graph, point_to=came_from, start=start, goal=goal)
        draw_grid(graph, path=reconstruct_path(came_from, start=start, goal=goal))
        draw_grid(graph, number=cost_so_far, start=start, goal=goal)
        #pdb.set_trace()
        print()
        print(max(cost_so_far.values()))
if __name__ == '__main__':
    main()
