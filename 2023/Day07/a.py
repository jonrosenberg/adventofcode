
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

    # Example input
    # lines = ["32T3K 765", "T55J5 684", "KK677 28", "KTJJT 220", "QQQJA 483"]
    total = total_winnings(lines)
    print(f"Total winnings: {total}")

def card_value(card, p2=False):
    if p2:
       return "J23456789TQKA".index(card)
    else:
      return "23456789TJQKA".index(card)
def card_label(i):
    return "23456789TJQKA"[i]

def encode_hand_to_int(hand:str, p2=False):
    encode_hand = 0
    counts = {card: hand.count(card) for card in set(hand)}

    if p2 and 'J' in counts.keys() and counts['J'] != 5:
      num_j = counts.pop('J')
      max_key = max(counts, key=counts.get)
      counts[max_key] += num_j
       
    if 5 in counts.values():
        encode_hand += 6*10**12  # Five of a kind
    elif 4 in counts.values():
        encode_hand += 5*10**12  # Four of a kind
    elif 3 in counts.values() and 2 in counts.values():
        encode_hand += 4*10**12  # Full house
    elif 3 in counts.values():
        encode_hand += 3*10**12  # Three of a kind
    elif list(counts.values()).count(2) == 2:
        encode_hand += 2*10**12  # Two pair
    elif 2 in counts.values():
        encode_hand += 1*10**12  # One pair
    else:
        encode_hand += 0*10**12  # High card

    for i, card in enumerate(hand):
        encode_hand += card_value(card,p2)*100**(len(hand)-i-1)
    return encode_hand
def total_winnings(hands, p2=False):
    encoded_hands = {encode_hand_to_int(hand.split()[0],p2):int(hand.split()[1]) for hand in hands}
    sort_encoded_hands = sorted( list(encoded_hands.keys()))
    total_winnings = 0
    for i,k in enumerate(sort_encoded_hands,1):
        total_winnings += encoded_hands[k]*i
    
    return total_winnings
    # 246358066

def runPart2(lines):
    # Part 2
    print("part 2 start")
    total = total_winnings(lines,True)
    print(f"Total winnings: {total}")

def card_value2(card):
    return "23456789TQKAJ".index(card)


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
