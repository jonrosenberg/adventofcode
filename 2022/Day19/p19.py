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
testRun = False
part2 = True


printing = False

default_file = f"Day{problemNum}/test.txt"

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"

Step = Tuple[int, int]

PATTERN = re.compile(
    r"Blueprint (\d+): "
    r"Each ore robot costs (\d+) ore. "
    r"Each clay robot costs (\d+) ore. "
    r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
    r"Each geode robot costs (\d+) ore and (\d+) obsidian."
)
State = TypeVar('State')
class Blueprint:
    __slots__ = ("id", "cost", "useful", "maxGeo")
 
    def __init__(self, input_string: str) -> None:
        vals = [int(i) for i in re.findall(r"\d+", input_string)]
        self.id = vals[0]
        self.cost = {
            "ore": {"ore": vals[1]},
            "clay": {"ore": vals[2]},
            "obsidian": {"ore": vals[3], "clay": vals[4]},
            "geode": {"ore": vals[5], "obsidian": vals[6]}
        }
        self.useful = {
            "ore": max(self.cost["clay"]["ore"],
                       self.cost["obsidian"]["ore"],
                       self.cost["geode"]["ore"]),
            "clay": self.cost["obsidian"]["clay"],
            "obsidian": self.cost["geode"]["obsidian"],
            "geode": float("inf")
        }
        self.maxGeo: dict[int,int] = {}

    def atMaxGeo(self,timeRemaining,state:State) -> bool:
        return  timeRemaining in self.maxGeo.keys() \
            and self.maxGeo[timeRemaining] > state.resources["geode"]
               
    def __str__(self) -> str:
        return f"id{self.id} cost:{self.cost} useful:{self.useful} "


class State:
    __slots__ = ("robots", "resources", "visited")
 
    def __init__(self, robots: dict = None, resources: dict = None,
                 visited: list = None):
        self.robots = robots.copy() if robots else {
            "ore": 1, "clay": 0, "obsidian": 0, "geode": 0
        }
        self.resources = resources.copy() if resources else {
            "ore": 0, "clay": 0, "obsidian": 0, "geode": 0
        }
        self.visited = visited.copy() if visited else []
        
 
    def affordBot(self, cost) -> bool:
        return all(self.resources[bot] >= costRes for bot, costRes in cost.items())

    def copy(self) -> "State":
        return State(self.robots, self.resources, self.visited)
 
    def __gt__(self, other):
        return self.resources["geode"] > other.resources["geode"]
 
    def __repr__(self):
        return f"{{robots: {self.robots}, resources: {self.resources}}}"
 
def chooseNext(blueprint: Blueprint, prior_states:list[State], timelimit:int = 26) -> list[tuple[int,list]]:
    timeRemaining = timelimit - len(prior_states)
    
    if timeRemaining < 0:
        return prior_states[-1].resources["geode"], prior_states
    
    current_state = prior_states[-1]
    options: list[str] = []
    
    if current_state.resources["geode"] > 0 \
        and (
            timeRemaining not in blueprint.maxGeo.keys() 
            or blueprint.maxGeo[timeRemaining] < current_state.resources["geode"]
        ):
            blueprint.maxGeo[timeRemaining] = current_state.resources["geode"]
            #print(blueprint.maxGeo)


    # add options you can afford
    for bot, cost in blueprint.cost.items():
        if current_state.robots[bot] < blueprint.useful[bot] \
        and current_state.affordBot(cost) \
        and bot not in current_state.visited:
            options.append(bot)

    
    # remove options
    if timeRemaining < 1 or blueprint.atMaxGeo(timeRemaining,current_state):
        options = []
    elif "goede" in options:
        options = ["geode"]
    else:
        # cutting off plans that build resources more than 2 phases back
        if ((timeRemaining < 2 
                # or current_state.robots["clay"] > 5 
                # or current_state.robots["obsidian"] > 3
                # or "obsidian" in options 
                ) and "ore" in options):
            options.remove("ore")
        if (( timeRemaining < 3 
        # or current_state.robots["geode"] 
        # or current_state.robots["obsidian"] > 3
        ) and "clay" in options):
            options.remove("clay")

    # create next_stat
    next_state = current_state.copy()

    # gather resouces
    for bot, numBot in next_state.robots.items():
        next_state.resources[bot] += numBot
        
    next_state.visited += options
    results = [chooseNext(blueprint, prior_states + [next_state], timelimit)]
    
    # loop through options
    for opt in options:
        next_state_opt = next_state.copy()
        next_state_opt.visited = []
        next_state_opt.robots[opt] += 1
        for res, numRes in blueprint.cost[opt].items():
                next_state_opt.resources[res] -= numRes
        result = chooseNext(blueprint, prior_states + [next_state_opt],timelimit)
        #print(f"timeleft:{timeRemaining} bots:{next_state_opt.robots} ")
        results.append(result)
    if printing and next_state.resources["geode"] > 0 and len(prior_states) == timelimit and len(options) > -1:
        print(f"min:{len(prior_states)} state:{next_state} max:{max(results)[0]} ")
    return max(results)

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
        
        blueprints = [Blueprint(bp) for bp in lines]
        
        result = 0
        for blueprint in blueprints:
            if printing: print(blueprint)
            bpResult = chooseNext(blueprint,[State()],24)
            result += bpResult[0] * blueprint.id
        print("result Part 1")
        if result:
            print(result)
        getTime()
        if part2:
            print("Part 2")
            result2 = 1
            for blueprint in blueprints[:3]:
                if printing: print(blueprint)
                bpResult = chooseNext(blueprint,[State()],32)
                print(bpResult[0])
                result2 *= bpResult[0]
                getTime()
            
            if result2:
                print(result2)


        

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
