import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional


import itertools


bug = False

# get input file 
testRun = False
part2 = True

start = "AA"
plength = 7


default_file = "Day16/test.txt"

if testRun == False:
    default_file = "Day16/input.txt"
    plength = 16

minutesLeft = 30
Valve = TypeVar('Valve')
Tunnel = Tuple[str, str]

class Graph:
    def __init__(self) -> None:
        self.allValves: dict[str,Valve] = {}
        self.valves: list[str] = []
        self.travelTimeIndex: dict[str,(str,float,int,int)] = {}
        self.travelCost: dict[Tunnel,(str,float,int,int)] = {}

    def getValve(self,id:str) -> Valve:
        return self.addValves[id]

    def addValve(self,v:Valve) -> None:
        if v.id not in self.allValves.keys():
            self.allValves[v.id] = v
        if v.hasFlow and v not in self.valves:
            self.valves.append(v.id)
             
    def buildTravelCostIndex(self, current:str = start) -> None:
        route = {}
        q = Queue()
        # go through each tunnel and if hasFlow then add to trevelTimeIndex
        steps=1
        q.puts(self.allValves[current].neighbors)
        while not q.empty():
            neigbors = q.gets()
            for n in neigbors:
                t = (current,n)
                if t not in route.keys() and current != n:
                    route[t] = steps
                    q.puts(self.allValves[n].neighbors)
                    if self.allValves[n].hasFlow:
                        fr = self.allValves[n].flowRate
                        if current not in self.travelTimeIndex.keys():
                            self.travelTimeIndex[current] = []
                        self.travelTimeIndex[current].append((n,fr/steps,steps,fr))
                        self.travelCost[t] = (n,fr/steps,steps,fr)
                        
            steps += 1
            #print(f"steps {steps} {route}")

    
import collections
class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: str):
        self.elements.append(x)
    
    def puts(self, l: list[str]):
        for x in l:
            self.put(x)

    def get(self) -> str:
        return self.elements.popleft()

    def gets(self) -> list[str]:
        q = []
        while not self.empty():
            q.append(self.get())
        return q


class Valve:
    def __init__(self, id: str, flowRate: int, neighbors: list[str]) -> None:
        self.id = id
        self.flowRate:int = flowRate
        self.neighbors: list[str] = neighbors
        self.tunnels: list[Tunnel] = [ (id, n) for n in neighbors]
        self.hasFlow: bool = False
        if flowRate != 0: 
            self.hasFlow = True

    def __str__(self) -> str:
        return f"id:{self.id} node:{self.hasFlow} flowRate:{self.flowRate} tunnels:{self.neighbors}"

class Path:
    def __init__(self, start) -> None:
        self.path:list[str] = [start]
        self.path2:list[str] = [start]
        self.releaseRate: int = 0
        self.totalReleased: int = 0 
        self.min: int = 0
        self.wait1: int = 0
        self.wait2: int = 0
        self.open: list[str] = []
        
    def nextStep(self, next) -> None:
        min = next[2] + 1
        if 30 - (self.min + min) >= 0:
            self.path.append(next[0])
            self.totalReleased += self.releaseRate*min
            self.min += min
            self.releaseRate += next[3]
    

    # def nextMin1(self, next:tuple) -> None:
    #     min = next[2] + 1
    #     if self.wait1 == 0:
    #         self.wait1 = min
    #         self.path.append(next[0])
    #     elif self.wait1 == 1: 
    #         self.releaseRate += next[3]
        
    #     if self.wait2 == 0:
    #         pass
    #     #self.totalReleased += self.releaseRate

    # def
    def doublePath(self, g:Graph, fullPath:tuple):
        fullPath = ("AA",)+fullPath
        i1 = 0
        i2 = 1
        next1, next2 = None, None
        while self.min < 26:
            if self.wait1 == 0:
                if next1: self.releaseRate += next1[3]

                if i1+2 < len(fullPath):
                    self.open.append(fullPath[i1+1])
                    next1 = g.travelCost[(fullPath[i1],fullPath[i1+2])]
                    self.path.append(next1[0])
                    self.wait1 = next1[2] + 1
                i1 += 2
                #print(f"YOU min:{self.min} rate:{self.releaseRate} totalR:{self.totalReleased} wait1:{self.wait1} wait2:{self.wait2}\n next:{next1} path:{self.path}  ")
            # elif self.wait2 == 1:
            #     self.releaseRate += next1[3]

            if self.wait2 == 0:
                if next2: self.releaseRate += next2[3]

                if i2+2 < len(fullPath):
                    self.open.append(fullPath[i2+2])
                    next2 = g.travelCost[(fullPath[i2],fullPath[i2+2])]
                    self.path2.append(next2[0])
                    self.wait2 = next2[2] + 1
                i2 += 2
                #print(f"ELE min:{self.min} rate:{self.releaseRate} totalR:{self.totalReleased} wait1:{self.wait1} wait2:{self.wait2}\n next:{next2} path:{self.path2}  ")
            # elif self.wait2 == 1:
            #     self.releaseRate += next2[3]

            self.wait1 -= 1
            self.wait2 -= 1
            self.min += 1
            
            self.totalReleased += self.releaseRate
            


    def calcPath(self, g:Graph, fullPath:list[str]):
        for i in range(len(fullPath)-1):
            c = g.travelCost[(fullPath[i],fullPath[i+1])]
            self.nextStep(c)
        self.finish()
        
    def finish(self):
        min = 30 - self.min
        self.totalReleased += self.releaseRate*min
        self.min += min
    
    def topChoices(self, choices, topNum:int = 3) -> list[str]:
        top = []
        for i in range(topNum):
            max = ("",0)
            for c in choices:
                if c[1] > max[1]:
                    max = c
            if max in choices:
                choices.remove(max)
            if max[1] > 0:
                top.append(max)
        return top
    
    def __str__(self):
        return f"released:{self.totalReleased} rate:{self.releaseRate} min:{self.min} path:{self.path} path2:{self.path2}"

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

        #parse string data and build graph
        for line in lines:
            
            valveIds = re.findall("[A-Z]{2}",line)
            flowRate = int(re.search("\d+",line).group())
            valveId = valveIds[0]
            neighbors = valveIds[1:]
        
            v = Valve(valveId, flowRate, neighbors) 
            g.addValve(v) 
            
        g.buildTravelCostIndex()
        for v in g.valves:
            g.buildTravelCostIndex(v)
        
        
        if part2:
            if testRun:
                dp = Path(start)
                goal = ('AA','JJ','DD','BB','HH','CC','EE')
                goalp1 = ('AA','JJ','BB','CC')
                goalp2 = ('AA','DD','HH','EE')
                dp.doublePath(g,goal)
                print(dp)

        else:
            if testRun:
                print(f"*** GOAL FIRST ***")
                path = Path(start)
                    
                goal = ["AA","DD","BB","JJ","HH","EE","CC"]
                print(goal)
                path.calcPath(g,goal) 

            # Get greedy first
            print(f"*** GREEDY FIRST ***")
            q = Queue()
            q.put(start)
            mp = ["AA"]
            global bug
            bug = True
            greedyP = Path(start)

            global minutesLeft
            while not q.empty():
                current = q.get()
                choices = g.travelTimeIndex[current]

                # reduce choices
                # TODO remove valves already open
                
                choices = greedyP.topChoices(choices,6)
                # print(f"len(q):{len(q.elements)} len(choices):{len(choices)} q:{q}")
                for c in choices:
                    if c[0] not in mp and minutesLeft-(c[2]+1) > 0:
                        minutesLeft-=(c[2]+1)
                        print(f"minutesLeft:{minutesLeft} p:{mp}")
                        q.put(c[0])
                        mp.append(c[0])
                        #print(f"c:{c} p:{p}")
                        
                        
            
            greedyP.calcPath(g,mp)
            print(greedyP)
            
            startP = Path(start)
            startP.calcPath(g,g.valves)
            print(startP)
            
        # Start traversing
        # # TODO - iterate on subset and build off of that
        max = 0
        permValves = g.valves.copy()
        
        if not testRun:
            if part2:
                #solvedValves = ('AA', 'VP', 'XQ', 'VM', 'GA', 'TR', 'SH', 'DO')
                solvedValves = ('AA', 'XQ', 'VP', 'GA', 'VM', 'SH', 'TR', 'QH')
            else: solvedValves = ('AA', 'XQ', 'VP', 'VM', 'TR', 'DO')
        else:
            solvedValves = ('AA', )

        for v in solvedValves:
            if v in permValves:
                permValves.remove(v)
        iter = itertools.permutations(permValves, 8)
        perms = [ i for i in iter ]

        results = []
        
        for p in perms:
            p = solvedValves + p
            cp = Path(start)
            if part2:
                cp.doublePath(g,p)
            else:
                cp.calcPath(g,p)  
            tr = cp.totalReleased
            results.append(tr)
            results += cp.path
            if max < tr:
                max = tr
                print(str(tr)+" "+str(p))
            
            if not testRun: goal = "??"
        print(f"goal:{goal}")
        print(f"max released: {max}")
        print(f"# permutations: {len(perms)}")
        
        ######### part 2 ######## 
        # input
        # tolow 2285 ('AA', 'VP', 'XQ', 'VM', 'GA', 'TR', 'SH', 'DO', 'QH', 'KI', 'VW', 'HN', 'VH', 'MN')
        # n!= 8 2285 ('AA', 'XQ', 'VP', 'GA', 'VM', 'SH', 'TR', 'QH', 'DO', 'VW', 'KI', 'VH', 'HN', 'MN', 'HI', 'DZ')
        # n!= 8 2285 ('AA', 'XQ', 'VP', 'GA', 'VM', 'SH', 'TR')('QH', 'DO', 'VW', 'KI', 'VH', 'HN', 'MN', 'HI')
        # n!= 8 2285 ('AA', 'XQ', 'VP', 'GA', 'VM', 'SH')('TR', 'QH', 'DO', 'VW', 'KI', 'VH', 'HN', 'MN')
        # n!= 8 2285 ('AA', 'XQ', 'VP', 'GA', 'VM')('SH', 'TR', 'QH', 'DO', 'VW', 'KI', 'VH', 'HN')
        # n!= 8 2269 ('AA', 'XQ', 'VP')('GA', 'VM', 'SH', 'TR', 'QH', 'DO', 'VW', 'KI')      
        # n!= 7 2196 ('AA', 'XQ', 'VP')('GA', 'VM', 'SH', 'TR', 'QH', 'KI', 'VW')
        # n!= 8 2155 ('AA', 'XQ', 'VP', 'GA', 'VM', 'SH', 'TR', 'VW', 'KI')
        # n!= 7 2065 ('AA', 'XQ', 'VP', 'GA', 'VM', 'SH', 'TR', 'VW')
        # n!= 6 1967 ('AA', 'VP', 'XQ', 'VM', 'GA', 'TR', 'VW')
        # n!= 5 1841 ('AA', 'VP', 'XQ', 'VM', 'GA', 'TR')
        # n!= 4 1566 ('AA', 'VP', 'VM', 'XQ', 'TR')
        # n!= 3 1258 ('AA', 'VP', 'XQ', 'TR')
        # n!= 2  887 ('AA', 'VP', 'TR')
        
          
        ######### part 1 ######## 
        # Test
        # n!= 6 1651 ('AA', 'DD', 'BB', 'JJ', 'HH', 'EE', 'CC')
        # n!= 5 1639 ('AA', 'DD', 'BB', 'JJ', 'HH', 'EE')
        # n!= 4 1612 ('AA', 'DD', 'BB', 'JJ', 'HH')
        # n!= 3 1423 ('AA', 'JJ', 'DD', 'HH')
        # n!= 2 1066 ('AA', 'DD', 'HH')
        
        # input
        #       1846 ('AA', 'XQ', 'VP', 'VM', 'TR', 'DO', 'KI', 'GA', 'VH', 'MN', 'DZ', 'HI')
        # n!= 6 1846 ('AA', 'XQ', 'VP', 'VM', 'TR')('DO', 'KI', 'GA', 'HN', 'DZ', 'HI')
        # n!= 6 1846 ('AA', 'XQ', 'VP')('VM', 'TR', 'DO', 'KI', 'DZ', 'HI')
        # n!= 4 1845 ('AA', 'XQ', 'VP', 'VM')('TR', 'DO', 'KI', 'HN')
        # 
        # n!= 8 2155 ('AA', 'XQ', 'VP', 'GA', 'VM', 'SH', 'TR', 'VW', 'KI')
        # n!= 7 1845 ('AA', 'XQ', 'VP', 'VM', 'TR', 'DO', 'KI', 'HN')
        # n!= 6 1829 ('AA', 'XQ', 'VP', 'VM', 'TR', 'DO', 'KI')
        # n!= 5 1756 ('AA', 'XQ', 'VP', 'VM', 'TR', 'KI')
        # n!= 4 1666 ('AA', 'XQ', 'VP', 'VM', 'TR')
        # n!= 3 1458 ('AA', 'VP', 'VM', 'TR')
        # n!= 2 1046 ('AA', 'VP', 'TR')
                
            
            
        
            

            
        
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
