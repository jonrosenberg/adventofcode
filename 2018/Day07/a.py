import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional
from collections import defaultdict, deque
import itertools

start_time = time.time()
# get input file 
print("os.path.dirname(__file__)")
print(os.path.dirname(__file__))
dirPath = os.path.dirname(__file__)
testRun = False
part2 = True

printing = False

default_file = f"{dirPath}/test.txt"

if testRun == False:
    default_file = f"{dirPath}/input.txt"
# elif part2:
#     default_file = f"{dirPath}/test2.txt"


def runPart1(lines):
    # Part 1
    print("part 1 start")
    lines.pop() # remove last '' line in input
    # # Find the order
    # order = find_order(lines)
    # print(f"Order of completion: {order}")

    # Find the order
    order = find_order(lines)
    print(f"Order of completion: {order}")


def find_order(instructions):
    # Create a graph and a set to store all unique steps
    graph = defaultdict(list)
    steps = set()
    
    # Process the instructions to fill the graph and steps set
    for instruction in instructions:
        parts = instruction.split(' ')
        step_before = parts[1]
        step_after = parts[7]
        graph[step_before].append(step_after)
        steps.update([step_before, step_after])
    
    # Count the number of incoming edges for each step
    incoming_edges = {step: 0 for step in steps}
    for step in graph:
        for next_step in graph[step]:
            incoming_edges[next_step] += 1

    # Use a priority queue to always select the next step alphabetically
    queue = deque(sorted([step for step in steps if incoming_edges[step] == 0]))

    order = []
    while queue:
        # Pop the step with no incoming edges and is smallest alphabetically
        current = queue.popleft()
        order.append(current)

        # Decrease the incoming edge count of its neighbors
        for neighbor in graph[current]:
            incoming_edges[neighbor] -= 1
            if incoming_edges[neighbor] == 0:
                queue.append(neighbor)
        
        # Keep the queue sorted
        queue = deque(sorted(queue))

    return ''.join(order)

def runPart2(lines):
    # Part 2
    print("part 2 start")
    # Find the time to complete with 5 workers
    completion_time = find_completion_time(lines, 5)
    print(f"Time to complete with 5 workers: {completion_time} seconds")
    # Find the time to complete with 2 workers (as per the revised example)
    
from collections import defaultdict, deque

def step_time(step):
    # Simplified step time for this scenario: A=1, B=2, ..., Z=26
    return ord(step) - ord('A') + 1

def find_completion_time(instructions, worker_count):
    # Create a graph and a set to store all unique steps
    graph = defaultdict(list)
    steps = set()
    
    # Process the instructions to fill the graph and steps set
    for instruction in instructions:
        parts = instruction.split(' ')
        step_before = parts[1]
        step_after = parts[7]
        graph[step_before].append(step_after)
        steps.update([step_before, step_after])

    # Count the number of incoming edges for each step
    incoming_edges = {step: 0 for step in steps}
    for step in graph:
        for next_step in graph[step]:
            incoming_edges[next_step] += 1

    # Initialize workers
    workers = [None] * worker_count  # Track the step each worker is on
    worker_time = [0] * worker_count  # Track the remaining time for each worker's step

    time = 0
    completed_steps = set()

    while True:
        # Update worker time and check for completed steps
        for i in range(worker_count):
            if workers[i] is not None:
                worker_time[i] -= 1
                if worker_time[i] == 0:
                    completed_steps.add(workers[i])
                    # Update incoming edges of the steps that depended on the completed step
                    for step in graph[workers[i]]:
                        incoming_edges[step] -= 1
                    workers[i] = None

        # Assign available workers to new steps
        for i in range(worker_count):
            if workers[i] is None:
                # Select the next step alphabetically that has no incoming edges and is not completed
                available_steps = sorted([step for step in steps if incoming_edges[step] == 0 and step not in completed_steps])
                if available_steps:
                    next_step = available_steps[0]
                    workers[i] = next_step
                    worker_time[i] = step_time(next_step)
                    steps.remove(next_step)

        # Check if all steps are completed
        if len(completed_steps) == len(incoming_edges):
            break

        time += 1

    return time






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
        
        # if not part2:
        runPart1(lines)
        if part2:
            getTime()
            runPart2(lines)     

def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
