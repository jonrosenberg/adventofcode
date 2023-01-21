import pdb

import sys
import os
import time

import re

from typing import Protocol, Iterator, Tuple, TypeVar, Optional
'''
  Decimal          SNAFU    
        1              1    
        2              2    
        3           1= 3    5-2
        4           1- 4    5-1
        5             10    
        6             11    
        7             12
        8             2= 23 2*5-2
        9             2- 24 2*5-1
       10             20    2*5
       15            1=0 30  (5-2)*5
       20            1-0 40  
     2022         1=11-2 2 31042
    12345        1-0---0 343340
314159265  1121-1110-1=0 1120411044030

SNAFU       Decimal
1=-0-2            1747
 12111             906
  2=0=             198
    21              11
  2=01             201
   111              31
 20012            1257
   112              32
 1=-1=             353
  1-12             107
    12               7
    1=               3
   122              37
2=-1=0 124030     4890
'''

start_time = time.time()
# get input file 
problemNum = 25
testRun = False
part2 = True

printing = False

default_file = f"Day{problemNum}/test.txt"

if testRun == False:
    default_file = f"Day{problemNum}/input.txt"

snafuToInt:dict[str,int] = { '=':-2, '-':-1, '0':0, '1':1, '2':2 }
intToSnafu:dict[int,str] = { 0:'0', 1:'1', 2:'2', 3:'=', 4:'-' }

def toDecimal(snafu:str) -> int:
    deci = 0
    for ri,n in enumerate(snafu):
        i = len(snafu)-(ri+1)
        deci += snafuToInt[n]*pow(5,i)
    return deci

def toSnafu(deci:int):
    snafu = ""
    remainder = 0
    while deci > 0:
        mod5 = deci % 5
        snafu = intToSnafu[mod5] + snafu
        if mod5 > 2: remainder = 1
        else: remainder = 0
        deci //= 5
        deci += remainder
    return snafu

def runPart1(lines:list[str]) -> None:
    # Part 1
    print("Part 1 start")
    total = 0
    for line in lines:
        deci = toDecimal(line.strip())
        total += deci
        print(f"snafu:{line} -> int:{deci} ")
    
    result = toSnafu(total)
    print(f"result: {result} ")
    print("Finished part 1")


def runPart2(lines:list[str]) -> None:
    # Part 2
    print("Part 2 start")
    
    #print(f"result:{result} ")
    print("Finished part 2")
    
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
        #runPart2(lines)
        
def getTime():
    print("--- %s seconds ---" % (time.time() - start_time))
         
if __name__ == '__main__':
    main()
    getTime()
