import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional

import itertools
import collections

start_time = time.time()
# get input file 
problemNum = 19
testRun = True
part2 = False

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

Step = Tuple[int, int]
# Blueprint 1: 
#   Each ore robot costs 4 ore. 
#   Each clay robot costs 2 ore. 
#   Each obsidian robot costs 3 ore and 14 clay. 
#   Each geode robot costs 2 ore and 7 obsidian.



PATTERN = re.compile(
    r"Blueprint (\d+): "
    r"Each ore robot costs (\d+) ore. "
    r"Each clay robot costs (\d+) ore. "
    r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
    r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    # r"(\w+) has flow rate=(\d+); "
    # r"(?:tunnel leads to valve|tunnels lead to valves) (\w+(?:, \w+)*)"
)
# total min     no need to build robot
# total min-1   no need to build non-geo robot
# total min-2   no need to build cly robot

def possibleMaxGeo():
    maxGeo = 0
    minCoal = 0
    minClay = 0
    # first needs to be built bot -1
    #
    min = 24 - 1
    maxGeoBots = [i for i in range(24)] 
    for b in maxGeoBots:
        maxGeo += b
    print(f"possible maxGeo:{maxGeo}")


# bot 



class Factory:
    def __init__(self,results:list[int]) -> None:
        self.min:int = 0
        self.blueprintId:int = results[0]

        
        #robot costs or
        self.costs: list[list] =  [ (0,results[1]),                 # oreRobotOreCost
                                    (0,results[2]),                 # clayRobotOreCost
                                    (0,results[3],1,results[4]),    # obsidianRobotOreCost, obsidianRobotClayCost
                                    (0,results[5],2,results[6]) ]   # geodeRobotOreCost, geodeRobotObsidianCost
        # robots:       ore,clay,obsidian,geode
        self.robots:list[int] = [1,0,0,0]
        # resources:    ore,clay,obsidian,geode
        self.resources:list[int] = [0,0,0,0]
        '''
I do not simulate each minute individually, instead, each state corresponds to a robot to build. 
At every step in my search I just see what all the possible bots I could build are and work towards that, 
skipping all intermediate turns.

I don’t build robots I don’t need. e.g. if the geode robots cost x obsidian I will never build more than x obsidian miners.

I use DFS and store the highest amount of geodes I’ve seen so far. 
When I explore a branch I use a heuristic that calculates how much geodes I could still mine in this branch 
(current geodes + amount of geodes acquired if I built a geode miner every turn). 
If that number is lower than the best attempt so far I drop the branch since it can never obtain more geodes than that attempt.
'''
        # -- permutation structure --
        # permutate the last items in list for depth first search
        # permutated list is legth is when obs,clay,ore reach maxBots
        # 1 permut [1 oreB, 2 clayB, 3 ....,15 obsB, 16 geoB ..., 23 geoB] 
        # 2 permut [1 oreB, 2 clayB, 3 ....,15 geoB, 16 geoB ..., 23 geoB] 
        #
        
        
        # Bot 4 all bots (if clay exist then obs) (if obs exit then geo)
        #  -- Greedy first priotization --
        # bot building rate 
        # bot/min = (r1cost+r2cost)/(r1Bots + r2Bots)
        # if lowest
        
        # geoBot obs cost == max obsBots
        maxObsBots = self.costs[3][3]
        # obsBot clay cost == max clayBots
        maxClayBots = self.costs[2][3]
        # bot max ore cost for (clay,obs,geo bots)== max oreBots
        maxOreBots = max([c[1] for c in self.costs[1:]])
        
        self.maxRobots = [maxOreBots,maxClayBots,maxObsBots]
        
        self.visits:list[list[int]] = []
        self.path:collections.deque = collections.deque()
        # import math
        # nextRobot waitTime = max(math.ceil((cost-resources)/rBots)),math.ceil((cost2-r2)/r2Bots)) ) 
    def permutation(self) -> None:
        
        while self.min < 24:
            self.nextRobot(self.path)
            self.min += 1

        # botQue = [[0,0],[0,1],[1,0],[1,1],[1,2]]
        # perms = itertools.product(botTypes,repeat=15)
        
        # # https://docs.python.org/3/library/itertools.html#itertools.product        
        # # maxBots [3,2,7]
        # # 
        # list(itertools.product([0,1,2],repeat=10))
        # return None

    def nextRobot(self,path) -> Step:

        # CHECK BEGINNING OF LIST
        if len(path)+1 > 3:
            options = [3,2,1,0]
            if 1 not in path:
                options.remove(2)
                options.remove(3)
            if 2 not in path:
                options.remove(3)
            for bot in options:
                if self.visited(path+[bot]):
                    options.remove(bot)
            # priotize remaining options
        elif len(path)+1 == 2:
            # 3rd Bot 3 ore or clay or (if clay exist then obs)
            options = [2,1,0]
            if 1 not in path:
                options.remove(2)
            for bot in options:
                if self.visited(path+[bot]):
                    options.remove(bot)
        elif len(path)+1 == 1:
            # 2nd Bot 2 ore or clay
            options = [1,0]
            if self.visited(path+[1]):
                options.remove(1)

        # END OF LIST
        elif len(path)+1 == 23:
            # 2nd last bot
            options = [3]
        elif len(path)+1 == 24:
            # last bot
            options = []
            
        # check if no more options
        if len(options) == 0:
            self.visited.append(path)

        # Check if you can build GeoBot
        elif 3 in options and self.hasGeoResources():
            next = 3
        else:
            next = self.mostNeeded(options)
        return 
        # removed uneeded bots based on order and 
    
    def mostNeeded(self,options) -> list[int]:
        mostNeeded = -1
        
        for bot in options:
            if bot != 3:
                needed = self.maxRobots[bot] - self.robots[bot]
                if needed > 0 and mostNeeded < needed: 
                    mostNeeded = bot
        return mostNeeded
            
    def visited(self,path) -> bool:
        for visit in self.visits:
            if path == visit[:len(path)]:
                return True
        return False

    def gather(self) -> None:
        for i,bot in enumerate(self.robots):
            self.resources[i] += bot

    def buildRobot(self, robot:int) -> bool:
        cost = self.costs[robot]
        # costs two type resources
        if len(cost) > 2:
            if self.resources[cost[2]] < cost[3]:
                return False
            elif self.resources[cost[0]] < cost[1]:
                return False
            else:
                self.resources[cost[2]] -= cost[3]
                self.resources[cost[0]] -= cost[1]
        # costs one type resources
        elif self.resources[cost[0]] < cost[1]:
            return False
        else:
            self.resources[cost[0]] -= cost[1]

        self.robots[robot] += 1
        return True
    
    def hasGeoResources(self) -> bool:
        return self.costs[3][1] <= self.resources[0] and self.costs[3][3] <= self.resources[2]
    

    def __str__(self) -> str:
        return f"id:{self.blueprintId} min:{self.min} "+ \
            f"res:{self.resources} robots:{self.robots} maxBots:{self.maxRobots}"

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


        factories:list[Factory] = []
        for line in lines:
            match = re.match(PATTERN, line)
            results = match.groups()
            params = []
            for r in results:
                params.append(int(r))
            f = Factory(params)
            factories.append(f)
            
        
        possibleMaxGeo()
        #greedyFirst
        factory = factories[0] 
        
        next = -1
        
        while len(factory.path) != 0:
            factory.gather()
            next = 1
            if factory.buildRobot(next):
                break        
            factory.min += 1
        
        print(factory)
        #robotQue = collections.deque()
            
        
        

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
