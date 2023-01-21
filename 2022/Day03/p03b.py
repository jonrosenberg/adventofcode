import pdb

import sys
import os

'''
Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.

Approach:
init var to store total
init list of ascii ord vals w/ index equal to elf code

for each knapsack:
    if len(knapsack)%1 != 0:
        print(error len(knapsack))
        sys.exit()

    split knapsack into equal two sections 

    mid = int(len(knapsack)/2)
    
    a = set(knapsack[:mid])
    b = set(knapsack[mid:])

    overlap = a.intersection(b) 

    total += list[ord(overap)]

print total
'''

def main():
    
    # print("hello world")
    
    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

    total = 0
    # init list of ascii ord vals w/ index equal to elf code
    # priority = [0] + list(range(97, 97+26)) + list(range(65, 65 + 26)) 
    with open(filepath, 'r') as file:
        data = file.read()
        lines = data.split('\n')
        i = 0
        while i < len(lines):  
            a = set(lines[i].strip())
            i += 1
            b = set(lines[i].strip())
            i += 1
            c = set(lines[++i].strip())
            i += 1
        # for each knapsack:
            overlap = a.intersection(b).intersection(c)

            val_in = ord(list(overlap)[0])

            if val_in >= 97:
                val_out = val_in - 97 + 1
            elif val_in >= 65:
                val_out = val_in - 65 + 27

            total += val_out


        print(f"total: {total}")

if __name__ == '__main__':
    main()