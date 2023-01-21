import pdb

import sys
import os

from ast import literal_eval

'''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''


def main():
    # get input file 
    default_file = "Day13/input.txt"
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
        '''
        rule1: If both values are integers, the lower integer should come first. If the left integer is lower than the right integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.
        rule2: If both values are lists, compare the first value of each list, then the second value, and so on. If the left list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the inputs are not in the right order. If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
        Rule3: If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
        '''
        #rule1
        # If both values are integers, left < right: correct 
        # If both values are integers, left < right: wrong 
        # if left int == right ints go to next
        #rule2
        # If left [] runs out 1st: correct
        # If right [] runs out 1st: wrong
        # If both lists are = continue to next
        #Rule3
        # If left or right is an int and other is list change int to list

        isOrder = 0

        i = 0
        rounds = dict()
        while i < len(lines)-2:
            left = literal_eval(lines[i])
            right = literal_eval(lines[i+1])
            print(f"Round {int(i/3+1)}")
            pp(left,right)
            print("."*10)
            rounds[int(i/3+1)] = checkRules(left,right)
            print(rounds[int(i/3+1)])
            
            i += 3
        print(rounds)
        score = 0
        correct_rounds = []
        for v in rounds:
            if rounds[v] == 1: 
                score += v
                correct_rounds.append(v)

        print(f"correct_rounds: {correct_rounds}")
        print(f"score: {score}")
        
        arr = []
        for l in lines:
            if len(l) != 0:
                arr.append(literal_eval(l))
        arr.append([[2]])
        arr.append([[6]])
        #pdb.set_trace()
        n = len(arr)
        
        # optimize code, so if the array is already sorted, it doesn't need
        # to go through the entire process
        swapped = False
        # Traverse through all array elements
        for i in range(n-1):
            # range(n) also work but outer loop will
            # repeat one time more than needed.
            # Last i elements are already in place
            for j in range(0, n-i-1):
    
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if checkRules(arr[j],arr[j + 1]) != 1:
                    swapped = True
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            
            if not swapped:
                # if we haven't needed to make a single swap, we
                # can just exit the main loop.
                break
        print("~"*20)
        for a in arr:
            print(a)
        i1 = arr.index([[2]])+1
        i2 = arr.index([[6]])+1
        print(f"i1: {i1} * i2: {i2} = {i1 * i2}")

def rule1(left,right):
    if isinstance(left,int) and isinstance(right,int):
        if left < right:
            return 1
        elif left > right:
            return -1
    return 0

def rule2(left,right):
    if isinstance(left,list) and isinstance(right,list):
        if len(left) == 0 and len(right) > 0:
            return 1
        elif (len(left) > 0 and len(right) == 0): #\
            #or (len(left) == 0 and len(right) == 0):
            return -1
    return 0

def rule3(left,right):
    if isinstance(left,int) and isinstance(right,list):
        left = [ left ]
    if isinstance(left,list) and isinstance(right,int):
        right = [ right ]
    return [left, right]

def pp(left,right):
    print(f" left: {left}")
    print(f"right: {right}")
            

def checkRules(left,right):
    result = rule1(left,right)
    if result != 0: return result

    [left, right] = rule3(left,right)
    if isinstance(left,int): return result
    
    result = rule2(left,right)
    if result != 0: return result
    
    size = max([len(left),len(right)]) 
    for i in range(size):
        if i == len(left) and i < len(right):
            return 1
        elif i == len(right):
            return -1
        #pp(left[i],right[i])
        #pdb.set_trace()
        result = checkRules(left[i],right[i])
        if result != 0: return result
            
    return result    


if __name__ == '__main__':
    main()
