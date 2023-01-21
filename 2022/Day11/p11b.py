import pdb

import sys
import os

import operator
import math
import re
'''
addx V takes 2 cycles
noop takes 1 cycle
'''

def main():
    # get input file 
    default_file = "Day11/test.txt"
    if len(sys.argv) < 2:
        filepath = default_file
    else:     
        filepath = sys.argv[1]
    print(f"~~~~~~~~~\n{filepath}\n~~~~~~~~~")
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    with open(filepath,'r') as file:
        
        data = file.read() # string
        lines = data.split('\n') # list of strings

        i = 0
        monkeys = []
        # add 7 lines of per monkey
        while i+5 < len(lines):
            monkeys.append(Monkey(lines[i:i+6]))
            i += 7
            
    
        i = 1
        
        rounds = 20
        while i <= rounds:
            count = 0
            if i % 1 == 0: print(f"!!!!!! ROUND {i:2} !!!!!!!")
            for m in monkeys:
                for item in m.items:
                    
                    print(f"i:{i} m:{m.number} item:{item}")

                    [num,item] = m.inspect(item)
                    monkeys[num].catch(item)
            
            if i % 1 == 0: 
                for m in monkeys:
                    print(m)
            i+=1

            # Driver Program to test above function
 
            # n = 315
            # print(n)
            # big_num = primeFactors(n)
            # print(big_num)
            # print(math.prod(big_num))

# A function to print all prime factors of
# a given number n
def primeFactors(n):
    result = []
    # Print the number of two's that divide n
    while n % 2 == 0:
        result.append(int(2))
        n = n / 2
         
    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3,int(math.sqrt(n))+1,2):
         
        # while i divides n , print i and divide n
        while n % i== 0:
            result.append(int(i))
            n = n / i
             
    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        result.append(int(n))

    return result


class Monkey:
    def __init__(self, lines):
        # counts the number of times the monkey inspects
        self.inspect_count = 0

        # get monkey number
        self.number = int(lines[0][7])
        # get items into list of ints 
        items = [int(x) for x in lines[1][18:].split(", ")]
        
             
        self.items = [primeFactors(item) for item in items]
        # get operation
        [op_a, op_str, op_b] = lines[2][19:].split(" ")
        op = { "+": operator.add, "-": operator.sub, "*": operator.mul }
        # TODO check if op_a or op_b are integers
        self.op_a = op_a
        self.op_str = op_str
        self.op = op[op_str]
        self.op_b = op_b
        # get test divisiable num
        self.test = int(lines[3][21:])
        self.true_to_monkey = int(lines[4][29:])
        self.false_to_monkey = int(lines[5][30:])

    def inspect(self, item):
        # run monkey operation for item
        a = item if self.op_a == "old" else primeFactors( int(self.op_a) )
        b = item if self.op_b == "old" else primeFactors( int(self.op_b) ) 
        
        if self.op_str == "*":
            item = sorted(a + b)
        elif self.op_str == "+":
            temp = math.prod(a) + math.prod(b)
            item = primeFactors(temp)

        #item = self.op(a,b)
        #item = int(item / 3)

        #remove item inspected
        self.items = self.items[1:]
        self.inspect_count += 1

        # test item and return result of which monkey to throw item to and the item
        if self.test in item:
            return [self.true_to_monkey, item]
        else:
            return [self.false_to_monkey, item]
    
    # add item to the monkey
    def catch(self, item):
        self.items.append(item)
    
    def print(self):
        return f"monkey:{self.number} inspected({self.inspect_count})\n" + \
            f" items:{self.items}\n" + \
            f" operation:{self.op_a} {self.op_str} {self.op_b}\n" + \
            f" test/{self.test} true:{self.true_to_monkey} false:{self.false_to_monkey}"

    def __str__(self):
        return f"monkey {self.number} i[{self.inspect_count:4}]"



if __name__ == '__main__':
    main()
