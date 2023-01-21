import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional


start_time = time.time()
# get input file 
problemNum = 21
testRun = False
part2 = True

printing = False

default_file = f"Day{problemNum}/test.txt"

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"

class Yells:
    def __init__(self,lines:list[str]) -> None: 
        monkeys = {}
        for line in lines:
            name, yell = line.strip().split(": ")
            monkeys[name] = Monkey(name,yell)

        self.monkeys: dict[str,Monkey] = monkeys
    
    def getYell(self, name:str = "root") -> int:
        monkey = self.monkeys[name]
        if not monkey.hasNumber:
            call1, call2 = monkey.calls
            int1 = self.getYell(call1)
            int2 = self.getYell(call2)
            if name == "root":
                print(f"int1:{int1} int2:{int2} diff:{int1-int2} ")
            
            return monkey.ops[monkey.opStr](int1,int2)
        else:
            return monkey.number

    def youYell(self) -> int:
        root = self.monkeys["root"]
        call1,call2 = root.calls
        isHum1 = self.hasHumn(call1)
        print("call2")
        isHum2 = self.hasHumn(call2)
        print(f"root: {call1} + {call2} hasHumn: {call1}:{isHum1} {call2}:{isHum2} ")
        if isHum1:
            humn = call1
            notHumn = call2
        else:
            humn = call2
            notHumn = call1
        if self.monkeys[notHumn].hasNumber:
            number = self.monkeys[notHumn].number
        else: 
            number = self.getYell(notHumn)
        result = self.getYou(humn,number)
        return result

    def hasHumn(self, name:str) -> bool:
        if self.monkeys[name].name == "humn":
            self.monkeys[name].hasHumn = True
            self.monkeys[name].number = None
            self.monkeys[name].hasNumber = False
            return True
        elif self.monkeys[name].hasNumber:
            return False
        else:
            call1, call2 = self.monkeys[name].calls
            self.monkeys[name].hasHumn = self.hasHumn(call1) or self.hasHumn(call2) 
            return self.monkeys[name].hasHumn

    def getYou(self, name:str, number:int) -> int:
        monkey = self.monkeys[name]
        if name == "humn":
            return number
        call1,call2 = monkey.calls
        if self.monkeys[call1].hasHumn:
            humn = call1
            notHumn = call2
            math = monkey.backOps
            switch = False
        else:
            humn = call2
            notHumn = call1
            math = monkey.revOps
            switch = True
        if self.monkeys[notHumn].hasNumber:
            num2 = self.monkeys[notHumn].number
        else:
            num2 = self.getYell(notHumn)
        if switch:
            num2, number = number, num2  
            str1, str2 = num2, humn
        else: str1, str2 = humn, num2
        eqStr = f"{name} = {str1:5} {self.monkeys[name].opStr} {str2:5} "
        s = f"{number:19} {self.monkeys[name].backOpsStr[self.monkeys[name].opStr]} {num2} "
        number = math[monkey.opStr](number,num2)
        if printing: print( eqStr+f"{number:19} = "+s )
        return self.getYou(humn,number)

class Monkey:
    def __init__(self,name,yell) -> None:
        self.name: str = name
        
        #self.ops =      { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv }
        self.ops      = { "+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "/": lambda a, b: a / b }
        self.backOps = { "+": lambda x, b: x - b, "-": lambda x, b: x + b, "*": lambda x, b: x / b, "/": lambda x, b: x * b }
        self.revOps   = { "+": lambda a, x: x - a, "-": lambda a, x: a - x, "*": lambda a, x: x / a, "/": lambda a, x: a / x }
        self.backOpsStr =  { "-": "+", "+": "-", "/": "*", "*": "/" }
        '''
        if 1st is x and '/' -> res * n2
            x/n2 = res -> x = res * n2
            x/3 = 6 -> x/3*6   = 3*6 -> x = 18
        else 2nd is x (rev) and '/' -> n1/res
            n1/x = res -> x = n1 / res
            3/x = 6 -> (3/x)/6 = 3/6 -> x = 1/2

        if 1st is x and '-' -> res + n2
            x-3 = 6 -> x = 6+3 -> x = 9
        else 2nd is x and '-' -> n1 - res
            3-x = 6 -> x = 3-6 -> x = -3 
        '''

        if yell.isdigit():
            self.number: int = int(yell)
            self.calls: list[str] = []
            self.opStr:str = None
        else:
            name1, opStr, name2 = yell.strip().split(" ")
            self.number: int = None
            self.calls: list[str] = [name1,name2]
            # self.op = self.ops[opStr]
            self.opStr:str = opStr
    
        self.hasNumber = self.number != None
        self.hasHumn = False

    

    

def runPart1(lines):
    # Part 1
    print("Part 1 start")
    yells = Yells(lines)
    result = yells.getYell()
    print(result)
    print("Finished part 1")
    getTime()

def runPart2(lines):
    # Part 2
    print("Part 2 start")
    yells = Yells(lines)
    result = yells.youYell()
    print(f"result:{result} ")
    print("Finished part 2")
    testYells = Yells(lines)
    testYells.monkeys["humn"].number = result 
    testYells.getYell()
    print(f"result:{int(result)} ")

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
        
        runPart1(lines)
        runPart2(lines)
        
def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
